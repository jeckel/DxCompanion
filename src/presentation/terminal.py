import subprocess

from textual import on, work
from textual.containers import Container, Horizontal, Grid
from textual.screen import ModalScreen
from textual.widgets import Label, Button, RichLog


class TerminalModal(ModalScreen):
    BORDER_TITLE = "Composer script ?"
    TITLE = 'Terminal'
    SUB_TITLE = 'Terminal Sub'
    def __init__(self, command: str, path: str|list[str], **kwargs):
        super().__init__(**kwargs)
        self.command = command
        self.path = path

    def compose(self):
        with Container():
            with Horizontal():
                yield Label(f"Running: {" ".join(self.command)}")
                yield Button("X", id="terminal_modal_close", variant="primary")
            yield RichLog(id="terminal_command", highlight=True, markup=True)

    def on_mount(self) -> None:
        self._start()


    @work(exclusive=True, thread=True)
    async def _start(self) -> None:
        terminal: RichLog = self.query_one("#terminal_command")
        terminal.write(f"[frame]Running command [italic red]{" ".join(self.command)}[/italic red][/frame]")
        self.log(f"Running: {self.command} in {self.path}")
        with subprocess.Popen(
                self.command,
                cwd=self.path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
        ) as process:
            output = process.stdout.read().strip()
            self.log(f"Sortie: {output}")
            terminal.write(output)
        terminal.write("[italic red]Completed![/italic red]")

    @on(Button.Pressed, "#terminal_modal_close")
    def on_close(self, event: Button.Pressed) -> None:
        self.app.pop_screen()
