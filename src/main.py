import typer
from pydantic_core._pydantic_core import ValidationError
from rich import print

from composer_utils import composer_updatable
from service_locator import Container
from models import Project
from presentation import MainApp

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

    print(composer_updatable(project))


def main() -> None:
    container = Container()
    app()


if __name__ == "__main__":
    main()
