from flask import Blueprint


console = Blueprint('console', __name__)

from . import file_generator, db_commands
