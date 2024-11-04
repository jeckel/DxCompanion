import typer

from service_locator import ServiceContainer
from models import Project
from presentation import MainApp

app = typer.Typer()


@app.command()
def tui(project_path: str) -> None:
    ServiceContainer()
    ServiceContainer.context().project = Project.from_json(json_path=project_path)
    tui_app = MainApp()
    tui_app.run()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
