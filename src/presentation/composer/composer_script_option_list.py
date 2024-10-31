from textual import on
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from models import Project
from service_locator import ServiceContainer
from .composer_message import ComposerCommandRequested


class ComposerScriptOptionList(OptionList):
    BORDER_TITLE = "Composer Scripts"

    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(
            *(
                Option(script)
                for script in ServiceContainer.composer_client().scripts(self.project)
            ),
            **kwargs
        )

    @on(OptionList.OptionSelected)
    def on_script_selected(self, event: OptionList.OptionSelected) -> None:
        self.post_message(ComposerCommandRequested(event.option.prompt))
