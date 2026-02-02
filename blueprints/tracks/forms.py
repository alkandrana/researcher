from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput


class TrackForm(FlaskForm):
    sequence = IntegerField("Track Number", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    type = StringField("Type", validators=[Length(max=50)])
    length = StringField("Length", validators=[Length(max=8)])
    performance_id = IntegerField("Performance ID", widget=HiddenInput())
    submit = SubmitField("Create")