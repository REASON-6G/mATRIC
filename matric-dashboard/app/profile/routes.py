from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.profile import bp
from app.profile.forms import ResetPasswordRequestForm, ResetPasswordForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():

    form = ResetPasswordForm()
    if form.validate_on_submit():
        oldpassword = form.oldpassword.data
        newpassword = form.password.data
        newpassword2 = form.password2.data
        if current_user.checkPassword(oldpassword):
            if newpassword == newpassword2:
                try:
                    current_user.setPassword(newpassword)
                    db.session.commit()
                    flash("Password updated successfully.",'success')
                    current_app.logger.info("Password updated successfully")
                except:
                    db.session.rollback()
                    flash("Password could not be updated.",'error')
                    current_app.logger.error("Password could not be updated.")
            else:
                    flash("New password and repeat password must match",'error')
                    current_app.logger.error("New password and repeat password must match.")
        else:
            flash("Incorrect previous password.",'error')
            current_app.logger.error("Incorrect previous password.")
                
            
    return render_template('profile/profile.html', title='User Profile', id=current_user.id,
                           username=current_user.username, email= current_user.email, form = form,
                           permissionlevel = current_user.permissionlevel, active = current_user.active)



