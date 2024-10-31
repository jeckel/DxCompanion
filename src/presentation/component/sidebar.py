from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import OptionList
from textual.widgets.option_list import Option, Separator


from models import Project
from presentation.composer.composer_script_option_list import ComposerScriptOptionList
from service_locator import ServiceContainer


class Sidebar(Container):
    DEFAULT_CSS = """
    Sidebar {
        width: 30;
        height: 100%;
        dock: left;
        background: $background;
        layer: sidebar;
    }

    Sidebar.-hidden {
        display: none;
    }
    """

    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(**kwargs)
        self.add_class("-hidden")

    def compose(self) -> ComposeResult:

        if len(ServiceContainer.composer_client().scripts(self.project)) > 0:
            yield ComposerScriptOptionList(self.project)

        yield OptionList(*(Option(action.label) for action in self.project.actions))
