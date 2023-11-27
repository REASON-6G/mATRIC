from flask import Blueprint

bp = Blueprint('manage_users', __name__)

from app.manage_users import routes
