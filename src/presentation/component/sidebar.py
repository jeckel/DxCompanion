from textual.app import ComposeResult
from textual.containers import Container

from presentation.component.action_option_list import ActionOptionList
from presentation.composer.composer_script_option_list import ComposerScriptOptionList
from service_locator import ServiceLocator


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

    def __init__(self, **kwargs):
        self._project = ServiceLocator.context().current_project
        super().__init__(**kwargs)
        self.add_class("-hidden")

    def compose(self) -> ComposeResult:

        if len(ServiceLocator.composer_client().scripts(self._project)) > 0:
            yield ComposerScriptOptionList(self._project)
        if self._project.actions is None:
            return
        for action_group, actions in self._project.actions.items():
            if len(actions) > 0:
                yield ActionOptionList(
                    project=self._project, actions=actions, group_name=action_group
                )
                # yield ActionOptionList(project=self.project)
