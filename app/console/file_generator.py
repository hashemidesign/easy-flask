import click
from app import base_dir
from app.console import console
from app.console.placeholders.api_placeholder import api_placeholder
from app.console.placeholders.model_placeholder import model_placeholder
from app.helpers.directories import exists_or_create_directory


@console.cli.command("create")
@click.option('--name', '-n', required=True, type=str)
@click.option('--model', is_flag=True)
def create_api(name, model):
    # flask console create name
    filename = f"{name}.py"
    
    api_path = base_dir + f'/api/' + filename
    exists_or_create_directory(api_path)
    api_placeholder(api_path, name)

    if model:
        model_path = base_dir + f'/models/' + filename
        exists_or_create_directory(model_path)
        model_placeholder(model_path, name)
