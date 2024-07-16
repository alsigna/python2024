from pydantic import Field, validate_call


@validate_call
def get_show_output(
    hostname: str,
    cmd: str = Field(pattern=r"^show\s+.*"),
) -> str:
    print(f"getting {cmd} output from {hostname}")


get_show_output("r1", "show ip int br")
get_show_output("r1", "display ip int br")
