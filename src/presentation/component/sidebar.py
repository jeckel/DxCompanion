from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import OptionList
from textual.widgets.option_list import Option, Separator


from models import Project


class Sidebar(Container):
    DEFAULT_CSS = """
    Sidebar {
        width: 30;
        height: 100%;
        dock: left;
        background: $primary-background;
        layer: sidebar;
        OptionList {
            margin: 1 0;
            border: none;
        }
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
        yield OptionList(
            *(Option(action.label) for action in self.project.actions)
        )
        # yield OptionList(
        #     Option("Aerilon", id="aer"),
        #     Option("Aquaria", id="aqu"),
        #     Separator(),
        #     Option("Canceron", id="can"),
        #     Option("Caprica", id="cap", disabled=True),
        #     Separator(),
        #     Option("Gemenon", id="gem"),
        #     Separator(),
        #     Option("Leonis", id="leo"),
        #     Option("Libran", id="lib"),
        #     Separator(),
        #     Option("Picon", id="pic"),
        #     Separator(),
        #     Option("Sagittaron", id="sag"),
        #     Option("Scorpia", id="sco"),
        #     Separator(),
        #     Option("Tauron", id="tau"),
        #     Separator(),
        #     Option("Virgon", id="vir"),
        # )