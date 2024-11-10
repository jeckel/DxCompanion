from textual.app import ComposeResult
from textual.containers import Container

from presentation.component.action_option_list import ActionOptionList, ActionList
from service_locator import ServiceLocator


class Sidebar(Container):
    DEFAULT_CSS = """
    Sidebar {
        width: 30;
        height: 100%;
        dock: left;
        background: $background;
        layer: sidebar;
        padding-top: 1;
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
        for (
            package_manager
        ) in ServiceLocator.context().current_project.package_managers:
            pm = ServiceLocator.package_manager()[package_manager]
            commands = pm.custom_commands()
            if len(commands) > 0:
                yield ActionList(title=pm.label, actions=list(commands.values()))

        if self._project.actions is None:
            return
        for action_group, actions in self._project.actions.items():
            if len(actions) > 0:
                yield ActionOptionList(
                    project=self._project, actions=actions, group_name=action_group
                )
                # yield ActionOptionList(project=self.project)
