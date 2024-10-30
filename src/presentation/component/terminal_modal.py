from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Static

from presentation.component.terminal import Terminal


class TerminalModal(ModalScreen[bool]):
    CSS = """
        TerminalModal {
            align: center middle;

            Container {
                margin: 4 8;
                Horizontal > Label {
                    padding: 0 1;
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
        allow_rerun: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.command = command
        self.path = path
        self.modal_title = f"Running: {" ".join(self.command)}"
        self.allow_rerun = allow_rerun
        self.terminal = Terminal(
            id="terminal_command",
            classes="modal_container",
        )
        self._result = False

    def compose(self) -> ComposeResult:
        with Container(id="modal_container"):
            with Horizontal(classes="modal_title"):
                yield Static(self.modal_title)
            yield self.terminal
            with Horizontal(classes="button_container", id="modal_button_container"):
                yield Button("Close", id="modal_close")
                if self.allow_rerun:
                    yield Button.success(" Rerun", id="modal_rerun")

    def on_mount(self) -> None:
        self.terminal.execute(command=self.command, path=self.path)

    @on(Button.Pressed, "#modal_close")
    def on_close(self, event: Button.Pressed) -> None:
        self.dismiss(self._result)

    @on(Button.Pressed, "#modal_rerun")
    def on_rerun(self, event: Button.Pressed) -> None:
        self.terminal.execute(command=self.command, path=self.path)


    @on(Terminal.TerminalCompleted)
    def on_terminal_completed(self, event: Terminal.TerminalCompleted) -> None:
        self.query_one("#modal_button_container").loading = False


    @on(Terminal.TerminalStarted)
    def on_terminal_started(self, event: Terminal.TerminalStarted) -> None:
        self.query_one("#modal_button_container").loading = True
