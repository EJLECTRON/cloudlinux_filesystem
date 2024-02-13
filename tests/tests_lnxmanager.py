from typer.testing import CliRunner
import os, pytest


from lnxmanager import __app_name__, __version__, cli

runner = CliRunner()

#generating test_list_files
directory = '/home/ejlectron/filesystem_cloudlinux/test_data/images'
files = os.listdir(directory)
test_list_files = [os.path.join(directory, file) for file in files]



def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_file_info():
    pass
@pytest.mark.parametrize('path', test_list_files)
def test_file_permissions(path):
    result = runner.invoke(cli.app, f'show_permissions {path} --full')

    assert 'good' in result.stdout