from flask import Blueprint
from flask_login import login_required

bp = Blueprint('dashboard', __name__)

from app.dashboard import routes