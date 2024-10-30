from textual.containers import Container, Horizontal
from textual.widgets import Markdown, Button
from textual import on

from models import Project
from presentation.component import TerminalModal


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
                for label in self.project.actions.keys():
                    yield Button(label, name=label)


    @on(Button.Pressed)
    def on_pressed(self, event: Button.Pressed) -> None:
        self.app.push_screen(
            TerminalModal(
                command=self.project.actions[event.button.name].split(' '),
                path=self.project.path,
                allow_rerun=True,
            )
        )