from app import app
from flask import render_template,flash, request, redirect, url_for
from .forms import AssessmentForm, ModuleForm
# from app import db, models
import datetime

@app.route('/')
def index():
    return "Hello World!!!"



@app.route('/login-signup', methods=['GET','POST'])
def login():
    return "Login / Sign up page!!!"


@app.route('/home', methods=['GET','POST'])
def home():
    return "Home page!!!"


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

    return render_template('create_assessment.html',
                            title=title,
                            header=header,
                            form=form)