import subprocess
from time import sleep

from textual.widgets import RichLog
from textual import on
from textual.message import Message
from textual.worker import Worker, WorkerState


class Terminal(RichLog):
    DEFAULT_CSS = """
        Terminal {
            padding: 1 1;
        }
    """
    command: list[str] = []
    current_worker: Worker | None = None

    def __init__(self, **kwargs):
        super().__init__(highlight=True, markup=True, **kwargs)

    def execute(self, command: list[str], path: str) -> None:
        self.command = command
        self.current_worker = self.run_worker(
            self._execute(command, path), exclusive=True, thread=True
        )

    def is_running(self) -> bool:
        return self.current_worker is not None and self.current_worker.is_running

    async def _execute(self, command: list[str], path: str) -> None:
        self.command = command
        self.clear()
        self.write(f"Path:    [bold blue]{path}[/bold blue]")
        self.write(f"Command: [bold blue]{" ".join(command)}[/bold blue]")
        self.write(
            "----------------------------------------------------------------",
            shrink=True,
        )
        self.log(f"Running: {command} in {path}")
        with subprocess.Popen(
            command,
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ) as process:
            assert process.stdout is not None
            for line in iter(process.stdout.readline, ""):
                self.write(line.strip(), shrink=True)
                sleep(0.01)
            process.wait()

            self.write(
                "----------------------------------------------------------------",
                shrink=True,
            )
            self.write(f"Return code [bold]{process.returncode}[/bold]")
            if process.returncode == 0:
                self.write("[bold green]Completed![/bold green]")
            else:
                self.write("[bold red]Completed with errors![/bold red]")

    @on(Worker.StateChanged)
    async def worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.RUNNING:
            self.post_message(self.TerminalStarted(self.command))
        if event.state == WorkerState.SUCCESS:
            self.post_message(self.TerminalCompleted(self.command))
        if event.state == WorkerState.CANCELLED or event.state == WorkerState.ERROR:
            self.post_message(self.TerminalCompleted(self.command, False))

    class TerminalStarted(Message):
        """
        Message sent when terminal execution starts
        """

        def __init__(self, command: list[str]) -> None:
            self.command = command
            super().__init__()

    class TerminalCompleted(Message):
        """
        Message sent when terminal execution completes
        """

        def __init__(self, command: list[str], success: bool = True) -> None:
            self.command = command
            self.success = success
            super().__init__()
