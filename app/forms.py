from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import DateField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import ValidationError

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from app import models
from werkzeug.security import generate_password_hash, check_password_hash

# form to add modules
class ModuleForm(Form):
    title = TextField('title', validators=[DataRequired()])
    module_code = TextField('module_code', validators=[DataRequired()])
    num_of_assessments = IntegerField('num_of_assessments', validators=[DataRequired()])
    num_of_credits = IntegerField('num_of_credits', validators=[DataRequired()])

# form to add assessements
class AssessmentForm(Form):
    title = TextField('title', validators=[DataRequired()])
    score = IntegerField('score', validators=[DataRequired()])
    total_marks = IntegerField('total_marks', validators=[DataRequired()])
    assessment_worth = IntegerField('assessment_worth', validators=[DataRequired()])

class SignUpForm(Form):
    name = TextField('name', validators=[DataRequired()])
    username = TextField('username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[EqualTo('password'), DataRequired()]) #makes sure password1 equals password2

    #validating that the username is unique
    def validate_username(self, username):
        student = models.Students.query.filter_by(username=username.data).first()
        if student:
            raise ValidationError('Username taken! Please choose a different username')

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ButtonForm(Form):
    submit = SubmitField('Submit')

class PasswordForm(Form):
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[EqualTo('new_password'), DataRequired()])
