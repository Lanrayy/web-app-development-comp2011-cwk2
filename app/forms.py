from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import DateField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired

# form to add modules
class ModuleForm(Form):
    title = TextField('title', validators=[DataRequired()])
    module_code = TextField('module_code', validators=[DataRequired()])
    num_of_assessments = IntegerField('num_of_assessments', validators=[DataRequired()])
    num_of_credits = IntegerField('num_of_credits', validators=[DataRequired()])

# form to add assessements
class AssessmentForm(Form):
    title = TextField('name', validators=[DataRequired()])
    score = IntegerField('score', validators=[DataRequired()])
    marks = IntegerField('marks', validators=[DataRequired()])
    worth = IntegerField('worth', validators=[DataRequired()])

