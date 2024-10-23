import subprocess

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, RichLog, Static


class TerminalModal(ModalScreen[bool]):
    CSS = """
        TerminalModal {
            align: center middle;
        
            Container {
                margin: 4 8;
                Horizontal > Label {
                    padding: 0 1;
                }
                RichLog {
                    padding: 1 1;
                }
            }
        
            .modal_title {
                height: 1;
                background: $primary-background;
                width: 100%;
                padding: 0 1;
            }
            .button_container {
                height: 3;
                background: $primary-background;
                width: 100%;
                align: center middle;
                Button {
                    margin: 0 1;
                }
            }
        }
        """

    def __init__(
        self,
        command: str | list[str],
        path: str,
        use_stderr: bool = False,
        allow_rerun: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.command = command
        self.path = path
        self.modal_title = f"Running: {" ".join(self.command)}"
        self.use_stderr = use_stderr
        self.allow_rerun = allow_rerun
        self.terminal = RichLog(
            id="terminal_command",
            highlight=True,
            markup=True,
            classes="modal_container",
        )
        self._result = False

    def compose(self) -> ComposeResult:
        with Container(id="modal_container"):
            with Horizontal(classes="modal_title"):
                yield Static(self.modal_title)
            yield self.terminal
            with Horizontal(classes="button_container"):
                yield Button("Close", id="modal_close")
                if self.allow_rerun:
                    yield Button.success(" Rerun", id="modal_rerun")

    def on_mount(self) -> None:
        self._start()

    @work(exclusive=True, thread=True)
    async def _start(self) -> None:
        self.terminal.write(f"Path:    [bold blue]{self.path}[/bold blue]")
        self.terminal.write(f"Command: [bold blue]{" ".join(self.command)}[/bold blue]")
        self.terminal.write(
            "----------------------------------------------------------------",
            shrink=True,
        )
        self.log(f"Running: {self.command} in {self.path}")
        with subprocess.Popen(
            self.command,
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            stdout, stderr = process.communicate()
            if stderr and self.use_stderr:
                self.terminal.write(f"[italic]{stderr}[/italic]")
            self.terminal.write(stdout)

            self.terminal.write(
                "----------------------------------------------------------------",
                shrink=True,
            )
            self.terminal.write(f"Return code [bold]{process.returncode}[/bold]")
            if process.returncode == 0:
                self.terminal.write("[bold green]Completed![/bold green]")
                self._result = True
            else:
                self.terminal.write("[bold red]Completed with errors![/bold red]")
                self._result = False


    @on(Button.Pressed, "#modal_close")
    def on_close(self, event: Button.Pressed) -> None:
        self.dismiss(self._result)

    @on(Button.Pressed, "#modal_rerun")
    def on_rerun(self, event: Button.Pressed) -> None:
        self.terminal.clear()
        self._start()
