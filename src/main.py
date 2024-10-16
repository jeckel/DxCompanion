import typer
from pydantic_core._pydantic_core import ValidationError
from textual.app import ComposeResult

from composer import run_composer
from models import Project
from presentation import MainApp
from settings import settings

from rich import print

app = typer.Typer()

@app.command()
def tui(project_path: str) -> None:
    try:
        project = Project(path=project_path)
        print(f"Composer present: {project.composer}")
    except ValidationError as e:
        print("Validation error:", e)
        exit(1)

    print(f"Launch tui for {project.name} project")
    app = MainApp(project)
    app.run()

@app.command()
def debug(project_path: str) -> None:
    try:
        project = Project(path=project_path)
        print(f"Composer present: {project.composer}")
    except ValidationError as e:
        print("Validation error:", e)
        exit(1)

    print(project.composer_json)

    from textual_terminal import Terminal

    from textual.app import App
    class TerminalApp(App):
        def compose(self) -> ComposeResult:
            #cd /home/jeckel/Workspace/10_Clients/Lamy-Liaisons/sf-ecustomer && composer cs-fix
            yield Terminal(command="cd /home/jeckel/Workspace/10_Clients/Lamy-Liaisons/sf-ecustomer && ls", id="terminal_htop")
            # yield Terminal(command="bash", id="terminal_bash")

        def on_ready(self) -> None:
            terminal_htop: Terminal = self.query_one("#terminal_htop")
            terminal_htop.start()

            # terminal_bash: Terminal = self.query_one("#terminal_bash")
            # terminal_bash.start()
    app = TerminalApp()
    app.run()


def main() -> None:
    app(prog_name=settings.__app_name__)


if __name__ == "__main__":
    main()