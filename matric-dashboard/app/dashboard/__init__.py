from flask import Blueprint
from flask_login import login_required

bp = Blueprint('dashboard', __name__)

def _protect_dashviews(dashboard):
    for view_func in dashboard.server.view_functions:
        if view_func.startswith(dashboard.config.url_base_pathname):
            dashboard.server.view_functions[view_func] = login_required(dashboard.server.view_functions[view_func])


from app.dashboard import routes