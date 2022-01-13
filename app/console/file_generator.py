import click

from app.core.placeholders.api_placeholder import api_placeholder
from app.core.placeholders.model_placeholder import model_placeholder
from app.core.placeholders.repository_placeholder import repository_placeholder
from . import console
from app import base_dir
from ..utils.directories import exists_or_create_directory


@console.cli.command("create-api")
@click.option('--name', '-n', required=True, type=str)
@click.option('--version', '-v', default='v1', type=str)
@click.option('--rep', is_flag=True)
def create_api(name, version, rep):
    # flask console create-api name v1
    filename = f"{name}.py"
    temp_path = base_dir + f'/api/{version}/' + filename
    exists_or_create_directory(temp_path)

    if rep:
        print("create repository")

    api_placeholder(temp_path)


@console.cli.command("create-repository")
@click.option('--name', '-n', required=True, type=str)
def create_repository(name):
    filename = f"{name}_repository.py"
    temp_path = base_dir + f'/repositories/' + filename
    exists_or_create_directory(temp_path)
    repository_placeholder(temp_path, name)


@console.cli.command("create-model")
@click.option('--name', '-n', required=True, type=str)
@click.option('--version', '-v', default='v1', type=str)
@click.option('--api', is_flag=True)
@click.option('--rep', is_flag=True)
def create_model(name, version, api, rep):
    # flask create-api name v1
    filename = f"{name}.py"
    temp_path = base_dir + f'/models/' + filename
    exists_or_create_directory(temp_path)
    model_placeholder(temp_path, name)

    if api:
        filename = f"{name}.py"
        temp_path = base_dir + f'/api/{version}/' + filename
        exists_or_create_directory(temp_path)
        if rep:
            api_placeholder(temp_path, name=name, repo=True)
        else:
            api_placeholder(temp_path, name)

    if rep:
        filename = f"{name}_repository.py"
        temp_path = base_dir + f'/repositories/' + filename
        exists_or_create_directory(temp_path)
        repository_placeholder(temp_path, name)
