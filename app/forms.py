from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import DateField
from wtforms import SubmitField
from wtforms import PasswordField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo

# form to add modules
class ModuleForm(Form):
    title = TextField('title', validators=[DataRequired()])
    module_code = TextField('module_code', validators=[DataRequired()])
    num_of_assessments = IntegerField('num_of_assessments', validators=[DataRequired()])
    num_of_credits = IntegerField('num_of_credits', validators=[DataRequired()])

# form to add assessements
class AssessmentForm(Form):
    title = TextField('name', validators=[DataRequired()])
    marks = IntegerField('marks', validators=[DataRequired()])
    worth = IntegerField('worth', validators=[DataRequired()])
    percent = IntegerField('percent', validators=[DataRequired()])

class SignUpForm(Form):
    name = TextField('name', validators=[DataRequired()])
    username = TextField('username', validators=[DataRequired()])
    password1 = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[EqualTo('password1'), DataRequired()]) #makes sure password1 equals password2

class LoginForm(Form):
    username = TextField('name', validators=[DataRequired()])
    password = PasswordField('score', validators=[DataRequired()])
