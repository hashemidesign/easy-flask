from flask import Blueprint


api = Blueprint('api', __name__)

from . import permission, role, user, auth