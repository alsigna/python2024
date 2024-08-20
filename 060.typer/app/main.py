import collect
import typer

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
)

app.add_typer(
    collect.app,
)


if __name__ == "__main__":
    app()
