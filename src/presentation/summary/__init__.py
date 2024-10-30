from textual.containers import Container, Horizontal
from textual.widgets import Markdown, Button
from textual import on

from models import Project
from models.project import ProjectAction
from presentation.component import (
    TerminalModal,
    Terminal,
    ShellCommand,
    NonShellCommand,
)


# service: Service = Provide[Container.service]
class ProjectSummaryContainer(Container):
    BORDER_TITLE = "Project's summary"
    DEFAULT_CSS = """
        ProjectSummaryContainer {
            border-title-color: $accent;
            border: $primary-background round;
            content-align: center middle;
            Markdown {
                height: auto;
            }

            #summary-actions {
                height: 3;
            }
        }
    """

    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(**kwargs)

    def compose(self):
        yield Markdown(
            f"""
# Project : {self.project.project_name}
"""
        )
        if len(self.project.actions) > 0:
            with Horizontal(id="summary-actions"):
                for action in self.project.actions:
                    yield ProjectActionButton(action)

    @on(Button.Pressed)
    def on_pressed(self, event: Button.Pressed) -> None:
        if not isinstance(event.button, ProjectActionButton):
            return
        action = event.button.action
        if action.use_shell:
            self.app.push_screen(
                TerminalModal(
                    command=ShellCommand(path=self.project.path, command=action.command)
                )
            )
        else:
            self.app.push_screen(
                TerminalModal(
                    command=NonShellCommand(
                        self.project.path, action.command.split(" ")
                    )
                )
            )


class ProjectActionButton(Button):
    def __init__(self, action: ProjectAction, **kwargs):
        self.action = action
        super().__init__(label=action.label, name=action.label, **kwargs)
