from flask import Blueprint


admin = Blueprint('admin', __name__)

from app.web.admin import dashboard
