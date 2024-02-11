"""This module provides the lnxmanager CLI"""
import typer, os
from typing_extensions import Annotated
from subprocess import check_output, PIPE
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

#TODO: make it work
@app.command(name="change_dir")
def change_dir(
        path: str = typer.Argument(..., help="The path to the directory to analyse."),
        size_threshold=None
) -> None:
    """ change directory to analyse"""
    if os.path.isdir(path):
        os.chdir(path)
        # os.system('cd /home/ejlectron/Documents/')
        typer.echo(f"you have switched to {os.getcwd()}")
        with open("text.txt", "w") as f:
            f.write("Hello, World!")
    else:
        raise typer.BadParameter(f"{path} is not a valid directory")

#TODO: make it work
@app.command(name="get_higher")
def switch_to_parent_dir() -> None:
    """ switch to parent directory"""
    current_dir = os.getcwd()

    if current_dir == os.path.abspath(os.sep):
        typer.echo(f"you are already at the root directory")
    else:
        os.chdir('..')
        typer.echo(f"you have switched to {os.getcwd()}")

    raise typer.Exit()

#TODO: test it
@app.command(name="file_type")
def file_type(path: str = typer.Argument(..., help="The path to the file to analyse.")) -> None:
    """ get the type of file"""
    spaces = " " * 10
    if os.path.isfile(path):
        text = str(os.path.splitext(os.path.basename(path))[0]) + spaces + str(os.path.splitext(path)[1])
        typer.echo(text)
    else:
        raise typer.BadParameter(f"{path} is not a valid file")

#TODO: complete it
def get_file_info(path: str) -> tuple:
    """ get the type of file
    :param path: the path to the file: str
    :return full info about file in the following format: str
            (filename, file type, file size, basic permissions)
    """
    file_type = __get_file_type(path)
    file_size = __get_file_size(path)
    permissions = __get_full_permissions(path)


def __get_file_type(path: str) -> str:
    """ get the type of file
    :param path: the path to the file: str
    :return the type of the file: str"""
    return os.path.splitext(path)[1]


def __get_file_size(path: str) -> str:
    """ show the sizes of files in the directory
    :param path: the path to the file: str
    :return the converted size of the file with the appropriate unit (example: 3 MB): str
    """
    return __reduce_file_size(int(os.path.getsize(path)))


def __reduce_file_size(size: int) -> str:
    """ reduce the size of file
    :param size: the size of file in bytes: int
    :return the converted size of the file with the appropriate unit (example: 3 MB): str
    """
    tuple_sizes, index = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"), 0

    while size >= 1024 and index < len(tuple_sizes) - 1:
        size /= 1024
        index += 1

    return f"{size} {tuple_sizes[index]}"

#TODO: test it
def __get_full_permissions(path: str) -> dict:
    """get the permissions of file"""
    try:
        raw_permissions = check_output(['ls', '-l', path], stderr=PIPE).decode('utf-8')
        result_permissions = __process_permissions(raw_permissions)
        return result_permissions
    except PermissionError:
        return {"error": "Permission denied"}
    except FileNotFoundError:
        return {"error": "File not found"}

#TODO: test it
@app.command(name="show_permissions")
def show_permissions(
        path: str = typer.Argument(..., help="The path of the file to get permissions."),
        full: bool = typer.Option(
                        False,
                        "--full",
                        "--f",
                        help="Show the full permissions of the file.",
                        is_flag=True)
) -> None:
    """ show the permissions of file
    :param full: show the full permissions of file: bool
    :param path: the path to the file: str
    :return the permissions of the file: str
    """
    if full:
        typer.echo(__get_full_permissions(path))
    else:
        typer.echo(__get_basic_permissions(path))

#TODO: test it
def __get_basic_permissions(path: str) -> str:
    """ show the basic permissions of file
    :param path: the path to the file: str
    :return the basic permissions of the file: str
    """
    return __process_permissions(check_output(['ls', '-l', path], stderr=PIPE).decode('utf-8'))["user owner"]

#TODO: test it
def __process_permissions(permissions: str) -> dict:
    """ process the permissions of file
    :param permissions: the permissions of file: str
    :return the processed permissions of the file in the following format: dict
            {   "owner rights": str,
                "group rights": str,
                "other rights": str,
                "user owner": str,
                "group owner": str   }
    """
    result_dict = {"owner rights": "",
                   "group rights": "",
                   "other rights": "",
                   "user owner": "",
                   "group owner": ""}

    given_info = permissions.split()

    # rights
    splitted_rights = [(given_info[0][i:i + 3]) for i in range(0, len(given_info[0]) - 1, 3)]

    for right, field in zip(splitted_rights, ["owner rights", "group rights", "other rights"]):
        result_dict[field] += __decode_rights(right)

    # owners
    result_dict["user owner"] = given_info[2]
    result_dict["group owner"] = given_info[3]

    return result_dict

#TODO: test it
def __decode_rights(rights: str) -> str:
    """ decode the rights of file"""

    decoding_dict = {"r": "read",
                     "w": "write",
                     "x": "execute",
                     "-": "no permission"}

    result = ""

    for right in rights:
        result += decoding_dict[right] + " "

    return result.strip()
