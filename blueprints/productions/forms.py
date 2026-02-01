from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, DateField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

from models import WorkType


class PerformanceForm(FlaskForm):
    def coerce_worktype(value):
        if value is None or value == "":
            return None
        return WorkType(value)

    title = StringField('Title', validators=[DataRequired(), Length(1, 255)])
    composer = StringField('Composer')
    type = SelectField('Work Type',
                       choices=[(wt.value, wt.name.replace("_", " ").title()) for wt in WorkType],
                       coerce=coerce_worktype,
                       validators=[DataRequired()])
    highlights = BooleanField('Highlights')
    date = DateField('Date', validators=[DataRequired()])
    album_id = HiddenField('Album ID', validators=[DataRequired()])
    submit = SubmitField('Submit')


