"""This module provides the lnxmanager CLI"""
import typer, os
from typing import Optional
from lnxmanager import __app_name__, __version__

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    pass
@app.command(name="change_dir")
def change_dir(
        path: str = typer.Argument(..., help="The path to the directory to analyse."),
        size_threshold=None
) -> None:
    """ change directory to analyse"""
    if os.path.isdir(path):
        os.chdir(path)
        typer.echo(f"you have switched to {os.getcwd()}")
    else:
        raise typer.BadParameter(f"{path} is not a valid directory")

@app.command(name="get_higher")
def switch_to_parent_dir() -> None:
    """ switch to parent directory"""
    current_dir = os.getcwd()

    if current_dir == os.path.abspath(os.sep):
        typer.echo(f"you are already at the root directory")
    else:
        os.chdir('..')
        typer.echo(f"you have switched to {os.getcwd()}")



    pass
