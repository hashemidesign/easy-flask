from flask import Blueprint


pub = Blueprint('pub', __name__)

from app.web.public import general
