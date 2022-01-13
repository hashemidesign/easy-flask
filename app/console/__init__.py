from flask import Blueprint, abort


console = Blueprint('console', __name__)

from . import file_generator

