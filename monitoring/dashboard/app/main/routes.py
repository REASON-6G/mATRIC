from flask import render_template, redirect, request, json
from flask_login import current_user, login_required
from app.main import bp
from app.extensions import db
from app.models import User


@bp.route('/liveness')
def alive():
    time.sleep(2);
    return "OK"

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/reload', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("main/main.html")