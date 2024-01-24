from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.models import Dashboard
from app.settings import bp
from app.settings.forms import GrafanaURLForm


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    dash = db.session.query(Dashboard).filter(Dashboard.id==1).first()
    
    dashboard_url = dash.url

    form = GrafanaURLForm()
    if form.validate_on_submit():
        current_app.logger.info(f'Submitting data')
        grafanaurl = form.url.data
        current_app.logger.info(f'Submitting data' + grafanaurl)

        try:
            dash.setURL(grafanaurl)
            db.session.commit()
        except SQLAlchemyError as e:
            return flash('Database error:' + e, 'error')    
        dashboard_url = grafanaurl
                
            
    return render_template('settings/settings.html', title='Settings', dashboard_url = dashboard_url, form=form)