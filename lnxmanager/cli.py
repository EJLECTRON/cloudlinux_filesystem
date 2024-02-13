"""This module provides the lnxmanager CLI"""
import typer, os
from typing_extensions import Annotated
from typing import Optional
from subprocess import check_output, PIPE

from decimal import Decimal

from lnxmanager import __app_name__, __version__

help = "Welcome to lnxmanager! A simple CLI to manage your Linux system."
app = typer.Typer(help=help)


def _version_callback(value: bool) -> None:
    """ show the application's version and exit
    :param value: the value of the version option: bool
    """
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
            is_eager=True
        )
) -> None:
    """The main function of the CLI
    :param version: show the application's version and exit: bool
    """
    pass

#TODO: make it work
@app.command(name="change_dir")
def change_dir(
        path: str = typer.Argument(..., help="The path to the directory to analyse."),
        size_threshold=None
) -> None:
    """ change directory to analyse
    :param path: the path to the directory: str
    :param size_threshold: the size threshold to filter the files: int"""
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


#TODO: complete it
@app.command(name="file_info")
def get_file_info(path: str) -> None:
    """ get the type of file
    :param path: the path to the object: str
    :return full info about file in the following format: str
            (filename, file type, file size, basic permissions)
    """
    file_type = __get_file_type(path)
    file_size = __get_file_size(path)
    read_permission, write_permission, execute_permission = get_basic_permissions(path).split("   ")

    typer.echo(f"Info about {path}\n"
               f"•file name: {file_type[0]}\n"
               f"•file extension: {file_type[1]}\n"
               f"•file size: {file_size}\n"
               f"•permissions for owner user: read:{read_permission}, write:{write_permission}, execute:{execute_permission}")

    raise typer.Exit()



#TODO: test it
def __get_file_type(path: str) -> tuple:
    """ get the type of file
    :param path: the path to the object: str
    :return name and extension of the file: tuple"""
    filename, file_extension = os.path.basename(path).split('.')
    return filename, file_extension


def __get_file_size(path: str) -> str:
    """ show the sizes of files in the directory
    :param path: the path to the object: str
    :return the converted size of the file with the appropriate unit (example: 3 MB): str
    """
    print(os.path.getsize(path))
    return __reduce_file_size(int(os.path.getsize(path)))


def __reduce_file_size(size: int) -> str:
    """ reduce the size of file
    :param size: the size of file in bytes: int
    :return the converted size of the file with the appropriate unit (example: 3 MB): str
    """
    tuple_sizes, index = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"), 0

    presice_num = Decimal(size) / 1000

    while presice_num >= 1024 and index < len(tuple_sizes) - 1:
        presice_num /= 1024
        index += 1

    return f"{str(presice_num)} {tuple_sizes[index]}"

#TODO: test it
def get_full_permissions(path: str) -> None:
    """get the permissions of the object
    :params: path: the path to the object: str
    :return: """
    result = {}

    if os.path.isfile(path):
        result = get_full_permissions_for_file(path)
    elif os.path.isdir(path):
        result = get_full_permissions_for_dir(path)

    if result['error'] != "Success":
        typer.echo(f"An error has occurred: {result['error']}")
    else:
        typer.echo('good')
        #typer.echo(result)

    typer.Exit()


def get_full_permissions_for_file(path: str) -> dict:
    """ get permissions for file
    :param path: the path to the object: str """
    try:
        raw_permissions = check_output(['ls', '-l', path], stderr=PIPE).decode('utf-8')
        result = __process_permissions(raw_permissions)
        result['error'] = "Success"
        return result
    except PermissionError:
        return {"error": "Permission denied"}
    except FileNotFoundError:
        return {"error": "File not found"}
    
#TODO: make it
def get_full_permissions_for_dir(path: str) -> dict:
    return {'error': "Success"}


def get_basic_permissions(path: str) -> str:
    """ show the basic permissions of file
    :param path: the path to the object: str
    :return the basic permissions of the file: str
    """

    return __process_permissions(check_output(['ls', '-l', path], stderr=PIPE).decode('utf-8'))["owner rights"]


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
    :param path: the path to the object: str
    :return the permissions of the file: str
    """
    if not os.path.exists(path):
        raise typer.BadParameter("File doesn't exist")

    if full:
        typer.echo(get_full_permissions(path))
    else:
        typer.echo(get_basic_permissions(path))

    typer.Exit()


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
    print(given_info)

    # rights
    splitted_rights = [(given_info[0][i:i + 3]) for i in range(1, len(given_info[0]) - 1, 3)]
    print(splitted_rights)

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

    result, index = "", 0

    for right in rights:
        if right != "-":
            result += decoding_dict[right] + "   "
        else:
            result += decoding_dict[right] + f" to {list(decoding_dict.values())[index]}" + "   "

        index += 1

    return result.strip()
