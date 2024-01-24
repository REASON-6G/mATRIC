from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired


class GrafanaURLForm(FlaskForm):
    url = StringField('Grafana Dashboard Public URL:', validators=[DataRequired()])
    submit = SubmitField('Submit')