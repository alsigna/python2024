# python main.py goodbye --formal alex
# python main.py goodbye alex
# python main.py hello alex

import typer

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
)


@app.command(no_args_is_help=True)
def hello(name: str):
    print(f"Hello {name}")


@app.command(no_args_is_help=True)
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
