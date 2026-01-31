from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
class AlbumForm(FlaskForm):
    uid = StringField('Catalog Number', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    medium = StringField('Record Medium', validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('Submit')