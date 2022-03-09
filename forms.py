from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class IdSubmitForm(FlaskForm):
    id_post = StringField('Id',
            validators=[DataRequired(), Length(min = 1, max = 3)])
    submit = SubmitField('Submit')


class CreatePostForm(FlaskForm):
    user_id = StringField('user_Id', validators=[DataRequired(), Length(min = 1, max = 3)])
    title = StringField('title', validators=[DataRequired(), Length(min = 1, max = 25)])
    body = StringField('body', validators=[DataRequired(), Length(min = 1, max = 150)])
    submit = SubmitField('Submit')

class ModifyForm(FlaskForm):
    id_post = StringField('id_post',
            validators=[DataRequired(), Length(min = 1, max = 3)])
    modify = SubmitField('Modify')

class ModifyPostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min = 1, max = 25)])
    body = StringField('body', validators=[DataRequired(), Length(min = 1, max = 150)])
    submit = SubmitField('Submit')

