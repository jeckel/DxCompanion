import typer
from dependency_injector import providers

from service_locator import Container
from models import Project
from presentation import MainApp

app = typer.Typer()


@app.command()
def tui(project_path: str) -> None:
    project = Project.from_json(json_path=project_path)
    container = Container()
    # container.project.override(providers.Singleton(Project, value=project))
    tui_app = MainApp(project)
    tui_app.run()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
