import os
import pytest

from click.testing import CliRunner

from cookiecutter.cli import main
from cookiecutter import utils

runner = CliRunner()


def remove_dir(request, path):
    """
    Remove fake project directories created during the tests.
    """
    def fin_remove_fake_project_dir():
        if os.path.isdir(path):
            utils.rmtree(path)
    request.addfinalizer(fin_remove_fake_project_dir)


@pytest.fixture
def remove_fake_project_dir(request):
    """
    Removes the fake-project directory after running tests.
    """
    remove_dir(request, 'fake-project')


@pytest.fixture
def remove_fake_project_2_dir(request):
    """
    Removes the fake-project-2 directory after running tests.
    """
    remove_dir(request, 'fake-project-2')


@pytest.fixture
def make_fake_project_dir(request):
    """
    Create the fake project directory created during the tests.
    """
    if not os.path.isdir('fake-project'):
        os.makedirs('fake-project')


def test_cli_version():
    result = runner.invoke(main, ['-V'])
    assert result.exit_code == 0
    assert result.output.startswith('Cookiecutter')


@pytest.mark.usefixtures('make_fake_project_dir', 'remove_fake_project_dir')
def test_cli_error_on_existing_output_directory():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input'])
    assert result.exit_code != 0
    expected_error_msg = 'Error: "fake-project" directory already exists\n'
    assert result.output == expected_error_msg


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_verbose():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input', '-v'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


@pytest.mark.usefixtures('remove_fake_project_2_dir')
def test_cli_extra_context():
    result = runner.invoke(main, [
        'tests/fake-repo-pre/',
        '--no-input',
        '-s', 'repo_name=fake-project-2'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project-2')
