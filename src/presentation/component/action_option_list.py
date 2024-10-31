from textual import on
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from models import Project
from models.project import ProjectAction
from .terminal import ShellCommand, NonShellCommand, CommandType
from .message import TerminalCommandRequested


class ActionOptionList(OptionList):
    # BORDER_TITLE = "Commands"

    # def __init__(self, project: Project, **kwargs):
    def __init__(
        self,
        project: Project,
        actions: list[ProjectAction],
        group_name: str = "Commands",
        **kwargs
    ):
        self._project: Project = project
        self._actions: list[ProjectAction] = actions
        super().__init__(*(Option(action.label) for action in self._actions), **kwargs)
        self.border_title = group_name

    @on(OptionList.OptionSelected)
    def on_script_selected(self, event: OptionList.OptionSelected) -> None:
        action = self._actions[event.option_index]
        command: CommandType = (
            ShellCommand(path=self._project.path, command=action.command)
            if action.use_shell
            else NonShellCommand(
                path=self._project.path, command=action.command.split(" ")
            )
        )
        self.post_message(TerminalCommandRequested(command=command))
