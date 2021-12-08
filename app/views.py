from app import app
from flask import render_template,flash, request, redirect, url_for
from .forms import AssessmentForm, ModuleForm, LoginForm, SignUpForm
from app import db, models #commented out to allow the use of
from flask_login import login_user
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

@app.route('/')
def index():
    return "Logged in!!!"

@app.route('/signup', methods=['GET','POST'])
def signup():
    title = "Sign up"
    header = "Sign up"
    form = SignUpForm()
    data = models.Students.query.all()
    password = form.password1.data
    # user clicks signup button
    if form.validate_on_submit():
        p = models.Students(name=form.name.data,
                            username=form.username.data,
                            password = generate_password_hash(password, method='sha256'))
        db.session.add(p) # add to database
        db.session.commit() # commit data
        flash('Succesfully submitted data')
        return redirect(url_for('login')) #redirect to signup
    if form.errors!= {}: #if there are no erros from the validators
        for err_message in form.errors.values():
            flash(f'There was an error with creating a user: {err_message}')
            return redirect(url_for('home'))

    return render_template('signup.html',
                            title=title,
                            header=header,
                            form=form,
                            data=data)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    title = "Login"
    header = "Login"
    form = LoginForm()


    student = models.Students.query.filter_by(username=form.username.data).first()

    if(student):
        if check_password_hash(student.password, form.password.data):
            flash(student.password)
            login_user(student, remember=True)
            student.authenticated = True
            return redirect(url_for('home'))

        else:
            flash('Please check your login details and try again.')
    # user clicks signup button
    return render_template('login.html',
                            title=title,
                            header=header,
                            form=form)


@app.route('/home', methods=['GET','POST'])
def home():
    title = "Home"
    header = "Home"
    data = current_user
    return render_template('home.html',
                            title=title,
                            header=header, name=current_user.name)


@app.route('/create_module', methods=['GET','POST'])
def create_module():
    title = "Create Module"
    header = "Create Module"
    form = ModuleForm()
    return render_template('create_module.html',
                            title=title,
                            header=header,
                            form=form)


@app.route('/create_assessment', methods=['GET','POST'])
def create_assessment():
    title = "Create Assessment"
    header = "Create Assessment"
    form = AssessmentForm()
    user = current_user

    if form.validate_on_submit():

    return render_template('create_assessment.html',
                            title=title,
                            header=header,
                            form=form)
