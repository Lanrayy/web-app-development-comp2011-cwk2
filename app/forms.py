from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import DateField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import ValidationError

from wtforms.validators import InputRequired,EqualTo, NumberRange, Length, Required
from app import models
from flask import flash, session
from flask_login import current_user

# form to add modules
class ModuleForm(Form):
    title = TextField('title', validators=[InputRequired()])
    module_code = TextField('module_code', validators=[InputRequired()])
    num_of_assessments = IntegerField('num_of_assessments', validators=[InputRequired(), NumberRange(min=0 , max=100,
                                                            message='Must be between 0 and 1000000') ])
    num_of_credits = IntegerField('num_of_credits', validators=[InputRequired()])

    #validating score is not greater than total marks
    def validate_assessments(self, field):
        flash('Validating num of assessments')
        # flash(type(self.num_of_assessments.data))

# form to add assessements
class AssessmentForm(Form):
    title = TextField('title', validators=[InputRequired()])
    score = IntegerField('score', validators=[InputRequired()])
    total_marks = IntegerField('total_marks', validators=[InputRequired()])
    assessment_worth = IntegerField('assessment_worth',
                                    validators=[
                                                InputRequired(), 
                                                NumberRange(min=0 , max=100,
                                                            message='Must be between 0 and 100')])

    #validating assessment name is unique
    def validate_title(self, title):
        module_code = session['selected_module']
        assessment = models.Assessments.query.filter_by(student_id=current_user.id).filter_by(module_code=module_code).filter_by(title=title.data).first()
        if assessment:
            raise ValidationError('Try Again! You have already added an assessment with this title for this module!')
    #validating score is not greater than total marks
    def validate_score(self, score):
        if self.score.data > self.total_marks.data:
            raise ValidationError('Your score is greater than total marks')

    


class SignUpForm(Form):
    name = TextField('name', validators=[InputRequired()])
    username = TextField('username', validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField('password1', validators=[InputRequired()])
    password2 = PasswordField('password2', validators=[EqualTo('password'), InputRequired()]) #makes sure password1 equals password2

    #validating that the username is unique
    def validate_username(self, username):
        flash('Validating User Name')
        student = models.Students.query.filter_by(username=username.data).first()
        if student:
            raise ValidationError('Username taken! Please choose a different username')

class LoginForm(Form):
    username = TextField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')

class ButtonForm(Form):
    submit = SubmitField('Submit')

class PasswordForm(Form):
    old_password = PasswordField('old_password', validators=[InputRequired()])
    new_password = PasswordField('new_password', validators=[InputRequired()])
    confirm_password = PasswordField('confirm_password', validators=[EqualTo('new_password', "Password fields do not match"), InputRequired()])
