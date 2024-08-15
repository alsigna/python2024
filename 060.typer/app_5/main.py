import collect
import typer

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
)

app.add_typer(
    typer_instance=collect.app,
    name="collect",
    help="собрать вывод с устройств",
)


if __name__ == "__main__":
    app()
