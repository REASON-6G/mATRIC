from flask_wtf import FlaskForm
from wtforms import SubmitField

#used in routes.py 
class ValidateUserForm(FlaskForm):
    submit = SubmitField('Validate User')
    
class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete User')
