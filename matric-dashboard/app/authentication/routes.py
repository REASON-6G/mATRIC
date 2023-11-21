from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse
from app.extensions import db, login_manager
from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.authentication import bp
from app.authentication.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm

@bp.route('/register', methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        def _exist():
            if User.query.filter_by(username=form.username.data).first() is not None:
                form.username.errors.append("Username already registered")
                return True
            elif User.query.filter_by(email=form.email.data).first() is not None:
                form.email.errors.append("Email already registered")
                return True
            else:
                return False

        if _exist():
            return render_template('authentication/register.html', title='Register', form=form)

        user: User = User(username=form.username.data,  password = form.password.data, email=form.email.data,)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            return flash('Database error:' + e, 'error')
        
        flash(f'User {user.username} is now registered', 'success')
        return redirect(url_for('authentication.login'))

    return render_template('authentication/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    admin = db.session.query(User).filter(User.permissionlevel==2).first()
    if admin:
        current_app.logger.info("Administrator(s) found.")
    else:
        current_app.logger.info("No administrators found. Creating one now.")
        user: User = User(username="admin", password="admin", email="admin@email.co.uk", active = True, level=2)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            return flash('Database error:' + e, 'error')
        
    if current_user.is_authenticated:
        current_app.logger.info(f'The user is already authenticated')
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Check that the user exists in the Portal database
        user: User = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.checkPassword(form.password.data):
            current_app.logger.info(f'Invalid username or password')
            flash('Invalid username or password', 'error')
            return redirect(url_for('authentication.login'))
        if user.active:
            login_user(user, remember=form.rememberMe.data)
            current_app.logger.info(f'User {user.username} ({user.id}) logged in')
            nextPage = request.args.get('next')
            if not nextPage or urlparse(nextPage).netloc != '':
                nextPage = url_for('main.index')
            return redirect(nextPage)
        else:
            current_app.logger.info('User has not been set to active yet.')
            flash('User has not been set to active yet', 'error')

    return render_template('authentication/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    current_app.logger.info(f'User logged out')
    return redirect(url_for('main.index'))
    
@login_manager.user_loader
def load_user(id: str) -> User:
    return User.query.get(id)