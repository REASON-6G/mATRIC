from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User



class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    oldpassword = PasswordField('Previous Password: ', validators=[DataRequired()])
    password = PasswordField(
        'New Password: ', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password: ', validators=[DataRequired()])
    submit = SubmitField('Change Password')
