from flask import render_template, redirect, request, json
from flask_login import current_user, login_required
from app.models import Dashboard
from app.dashboard import bp
from app.extensions import db

@login_required
@bp.route("/dashboard")
def dashboard():


    dash = db.session.query(Dashboard).filter(Dashboard.id==1).first()
    
    
    
    return render_template('dashboard/dashboard.html', url = dash.url)
