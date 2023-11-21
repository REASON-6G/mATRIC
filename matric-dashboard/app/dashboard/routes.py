from flask import render_template

from app.dashboard import bp
from app.dashboard import dashboard as dash_obj


@bp.route("/dashboard")
def dash_app_1():
    return render_template('dashboard/dashboard.html', dash_url=dash_obj.URL_BASE, min_height=dash_app_1_obj.MIN_HEIGHT)
