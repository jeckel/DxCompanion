import typer
from pydantic_core._pydantic_core import ValidationError

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
    # run_composer('outdated', project, ['--no-ansi', '--ignore-platform-reqs'])
    # run_composer('outdated', project, ['--dry-run', '--no-ansi'])

def main() -> None:
    app(prog_name=settings.__app_name__)


if __name__ == "__main__":
    main()