import os
import pytest
from subprocess import check_output, PIPE

from typer.testing import CliRunner

from lnxmanager import __app_name__, __version__, cli

runner = CliRunner()

# generating test_list_files
directory = '/home/ejlectron/filesystem_cloudlinux/test_data/images'
files = os.listdir(directory)
test_list_files = [os.path.join(directory, file) for file in files]


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_file_info():
    pass


def test_file_permissions_without_flags():
    directory = '/home/ejlectron/filesystem_cloudlinux/test_data/images'

    for file in os.listdir(directory):
        generate_answer_for_file_permissions_without_flags(directory + "/" + file)
        with open('file_permissions_without_flags.txt', 'r') as f:
            for line in f:
                path, permissions = line.split(":")
                result = runner.invoke(cli.app, ["show_permissions", path])
                assert "{'other rights': '" + permissions + "', 'error': 'Success'}" in result.stdout

    os.remove('file_permissions_without_flags.txt')


def generate_answer_for_file_permissions_without_flags(path):
    with open('file_permissions_without_flags.txt', 'w') as f:
        temp_raw_permissions = check_output(['ls', '-l', path], stderr=PIPE).decode('utf-8')
        f.write(path + ":" + temp_raw_permissions[7:10])