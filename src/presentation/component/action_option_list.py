from textual import on
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from models import Project, ShellCommand, NonShellCommand, CommandType
from models.project import ProjectAction
from .message import TerminalCommandRequested
from .terminal_modal import TerminalModal


class ActionOptionList(OptionList):
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


class ActionList(OptionList):
    def __init__(self, title: str, actions: list[CommandType], **kwargs):
        self._actions: list[CommandType] = actions
        super().__init__(*(Option(action.label) for action in self._actions), **kwargs)
        self.border_title = title

    @on(OptionList.OptionSelected)
    def on_script_selected(self, event: OptionList.OptionSelected) -> None:
        action = self._actions[event.option_index]
        self.app.push_screen(
            TerminalModal(
                command=action,
                allow_rerun=True,
            ),
        )
