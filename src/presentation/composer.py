from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from rich.text import Text
from textual.screen import ModalScreen
from textual.widgets import DataTable, Button, Label
from textual_terminal import Terminal


class ComposerRequireTable(DataTable):
    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        self.add_columns(*('Package', 'Version'))

    def set_requirements(self, requirements: dict[str, str]) -> None:
        for package, version in requirements.items():
            styled_row = (
                Text(str(package), justify="left"),
                Text(str(version), style="italic #03AC13", justify="right")
            )
            self.add_row(*styled_row)

class ComposerScriptButton(Button):
    def __init__(self, script_name: str, **kwargs):
        self.script_name = script_name
        super().__init__(f"Bouton {script_name}", id=f"composer-button-{script_name}", **kwargs)
        self.script_name = script_name

class ComposerScripts(Container):
    BORDER_TITLE = "Composer Scripts"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # @on(Button.Pressed)
    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     # todo check button instance of ComposerScriptButton
    #     self.log(f'composer {event.button.script_name}')
    #     pass

class ComposerScriptModal(ModalScreen):
    BORDER_TITLE = "Composer script ?"
    def __init__(self, script: str, **kwargs):
        super().__init__(**kwargs)
        self.script = script

    def compose(self):
        with Container():
            yield Label(f"Running script {self.script} in a terminal")
            yield Button.success("Close", id="composer_modal_close")
            yield Terminal(command="htop", id="terminal_composer_script", default_colors="textual")

    def on_mount(self) -> None:
        self.log('on ready')
        terminal: Terminal = self.query_one("#terminal_composer_script")
        terminal.start()

    @on(Button.Pressed, "#composer_modal_close")
    def on_close(self, event: Button.Pressed) -> None:
        self.app.pop_screen()
