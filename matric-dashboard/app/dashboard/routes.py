from flask import render_template, redirect, request, json
from flask_login import current_user, login_required

from app.dashboard import bp
from app.dashboard import dashboard as dash_obj

@login_required
@bp.route("/dashboard")
def dashboard():
    return render_template('dashboard/dashboard.html', dash_url=dash_obj.URL_BASE, min_height=dash_obj.MIN_HEIGHT)
