import typer

from settings import settings

app = typer.Typer()

@app.command()
def tui() -> None:
    print("Launch tui")
    # app = LegbaApp()
    # app.run()

def main() -> None:
    app(prog_name=settings.__app_name__)


if __name__ == "__main__":
    main()