from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
class RecordForm(FlaskForm):
    id = StringField('Catalog Number', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    composer = StringField('Composer', validators=[DataRequired()])
    orchestra = StringField('Orchestra', validators=[DataRequired()])
    conductor = StringField('Conductor', validators=[DataRequired()])
    submit = SubmitField('Submit')

class InterpreterForm(FlaskForm):
    name = StringField('Interpreter Name', validators=[DataRequired()])
    role = StringField('Character Name', validators=[DataRequired()])
    performance = StringField('Performance', validators=[DataRequired()])