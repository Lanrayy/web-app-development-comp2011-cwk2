from app import app, db, models
from flask import render_template,flash, request, redirect, url_for, session
from .forms import AssessmentForm, ModuleForm, LoginForm, SignUpForm, ButtonForm, PasswordForm
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import logging


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    app.logger.info('index route request')
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    title = "Homepage"
    form=ButtonForm()
    if request.method == 'POST':
        try:
            #get the value of the button clicked
            clicked_button = request.form['button']
            #check which button was clicked
            if clicked_button == 'login':
                flash(clicked_button)
                return redirect(url_for('login'))
            elif clicked_button == 'signup':
                flash(clicked_button)
                return redirect(url_for('signup'))
        except:
            flash("Error! Unable to perform action. Try again", "danger")
    return render_template('index.html',
                            title=title)


@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        app.logger.info('user already logged in! redireted to dashboard')
        return redirect(url_for('dashboard'))
    app.logger.info('signup route request')
    logout_user()
    title = "Sign up"
    header = "Sign up"
    form = SignUpForm()
    data = models.Students.query.all()
    if request.method == 'POST':
        try:
            password = form.password.data
            # user clicks signup button
            if form.validate_on_submit():
                p = models.Students(name=form.name.data,
                                    username=form.username.data,
                                    password = generate_password_hash(password, method='sha256'))
                # db.session.add(p) # add to database
                # db.session.commit() # commit data
                flash('Succesfully submitted data')
                # return redirect(url_for('login')) #redirect to signup

            if form.errors!= {}: #if there are no erros from the validators
                for err_message in form.errors.values():
                    app.logger.info('error! Unable to create account')
                    flash(f'Error! Unable to create account')
                    # return redirect(url_for('dashboard'))
        except Exception as e:
            flash(e)
    return render_template('signup.html',
                            title=title,
                            header=header,
                            form=form,
                            data=data)

@app.route('/login', methods=['GET','POST'])
def login():
    app.logger.info('login route request')
    if current_user.is_authenticated:
        app.logger.info('user already logged in! redireted to dashboard')
        return redirect(url_for('dashboard'))

    title = "Login"
    header = "Login"
    form = LoginForm()
    data = models.Students.query.all()

    student = models.Students.query.filter_by(username=form.username.data).first()

    if(student):
        if check_password_hash(student.password, form.password.data):
            flash(student.password)
            login_user(student, remember=True)
            student.authenticated = True

            app.logger.info('user authenticated. logging in...')
            return redirect(url_for('dashboard'))

        else:
            app.logger.error('invalid username or password! user not authenticated!')
            flash('Please check your login details and try again.')
    # user clicks signup button
    return render_template('login.html',
                            title=title,
                            header=header,
                            data =data,
                            form=form)

@app.route('/account', methods=['GET','POST'])
def account():
    title="Account"
    header="Account"
    if request.method == 'POST':
        try:
            #get the value of the button clicked
            clicked_button = request.form['button']
            #check which button was clicked
            if clicked_button == 'change-password':
                flash(clicked_button)
                return redirect(url_for('edit_password'))
        except Exception as e:
            app.logger.warning(e)
    return render_template('account.html',
                            title=title,
                            header=header)


@app.route('/edit_password', methods=['GET','POST'])
def edit_password():
    title="Edit password"
    header="Edit password"
    form=PasswordForm()
    if request.method == 'POST':
        try:
            #get the value of the button clicked
            clicked_button = request.form['button']
            flash(clicked_button)
            #check which button was clicked
            if clicked_button == 'Change Password':
                flash(clicked_button)
                student = models.Students.query.filter_by(id=current_user.id).first()

                if(student): #if the user is found
                    if check_password_hash(student.password, form.old_password.data): #compare inputed old password with password on database
                        if check_password_hash(student.password, form.new_password.data): #check if the new password is the same as old password
                            raise Exception("New password is the same as old password")
                        else:
                            student.password = form.new_password.data
                             # return redirect(url_for('account'))
                    else:
                         raise Exception("You have entered an incorrect old password")

        except Exception as e:
            flash(e, 'alert alert-danger')
            app.logger.warning('e')
    return render_template('edit_password.html',
                            title=title,
                            header=header,
                            form=form)


@app.route('/logout', methods=['GET','POST'])
def logout():
    app.logger.info('logout route request')
    title="Log out"
    header="Log out"
    form=LoginForm()
    session.clear()
    logout_user()
    app.logger.info('user logged out')
    # user clicks signup button
    return redirect(url_for('login'))




#displays all the modules
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    app.logger.info('dashboard route request')
    title = "Dashboard"
    header = "Dashboard"
    form=ButtonForm()
    # flash(selected_module)
    #check if request methos is POST
    if request.method == 'POST':
        try:
            #get the button value & convert it to an integer
            clicked = request.form['button']
            flash(clicked)
            flash('delete-module' in clicked)
            if clicked == 'add-module':
                flash(clicked)
                app.logger.info('user clicked add module button. redirecting to add module page...')
                return redirect(url_for('add_module'))
            else: # view module
                if 'delete-module' in clicked: # deleting the module
                    app.logger.info('user clicked delete module button...')
                    flash('deleting module')
                    module_code = clicked[14:]
                    #get all modules
                    module = models.Modules.query.filter_by(student_id=current_user.id).filter_by(module_code=module_code).first()
                    assessments = models.Assessments.query.filter_by(module_code=module_code).filter_by(student_id=current_user.id).all()
                    for assessment in assessments:
                        db.session.delete(assessment)
                    db.session.delete(module)
                    db.session.commit()
                    app.logger.info(f'module "{module.module_code} {module.title}" successfully deleted')
                else: # viewing the module
                    flash(clicked)
                    session['selected_module'] = clicked #you can use AJAX as well to pass data betwen the pages
                    app.logger.info(f'user clicked view module button: viewing module {clicked}')
                    return redirect(url_for('view_assessments'))
        except:
            app.logger.critical(e)
            flash("Error! Unable to perform action. Try again", "danger")

    data = models.Modules.query.filter_by(student_id=current_user.id).all()
    return render_template('dashboard.html',
                            title=title,
                            header=header,
                            name=current_user.name,
                            id = current_user.id,
                            form=form,
                            data=data)

@app.route('/add_module', methods=['GET','POST'])
@login_required
def add_module():
    app.logger.info('add module route request')
    title = "Add Module"
    header = "Add Module"
    form = ModuleForm()
    user = current_user

    if request.method == 'POST':
        try:
            #check if back to dashboard button clicked
            if form.validate_on_submit():
                #get a list of all the modules
                data = current_user.modules
                #check if module code already exists
                for module in data:
                    if module.module_code == form.module_code.data:
                        app.logger.info(f'unable to add module! module already exists!')
                        flash("Unable to add! Module already exists! Please add a different module", "danger")
                        {module.title}
                        return redirect(url_for('add_module'))

                #This code will run if there are no duplicate modules
                p = models.Modules( title=form.title.data,
                                    credit = form.num_of_credits.data,
                                    num_of_assessments=form.num_of_assessments.data,
                                    student_id = current_user.id,
                                    module_code = form.module_code.data)
                db.session.add(p) # add to database
                current_user.modules.append(p)
                db.session.commit()
                flash("Successfully added")

            clicked = request.form['button']
            if clicked == 'back-to-dashboard':
                flash(clicked)
                return redirect(url_for('dashboard'))
        except Exception as e:
            app.logger.critical(e)
            flash(e)

    return render_template('add_module.html',
                            title=title,
                            header=header,
                            form=form)

@app.route('/add_assessment', methods=['GET','POST'])
@login_required
def add_assessment():
    app.logger.info('add assessment request')
    title = "Add Assessment"
    header = "Add Assessment"
    form = AssessmentForm()
    user = current_user
    selected_module = session.get('selected_module', None)

    if request.method == 'POST':
        try:
            if form.validate_on_submit(): #check if the form validates
                if form.score.data > form.total_marks.data:#check marks is less than worth
                    app.logger.error('Marks greater than worth')
                    raise Exception('Your score is greater than total marks')

                #calculate percentage
                percent = (form.score.data / form.total_marks.data)* 100

                p = models.Assessments( title = form.title.data,
                                        score = form.score.data,
                                        total_marks = form.total_marks.data,
                                        score_percent = percent,
                                        assessment_worth = form.assessment_worth.data,
                                        module_code= selected_module,
                                        student_id = current_user.id)
                db.session.add(p) # add to database
                db.session.commit()
                flash("Successfully added")

                #calulate weighted avarage and update the right module
                weighted_average = 0
                sumofTakenAssessments = 0
                num_of_assessments = 0 # number of assesments taken
                data = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()
                for assessment in data:
                    num_of_assessments += 1
                    sumofTakenAssessments += assessment.assessment_worth
                    worth = assessment.assessment_worth / 100
                    weighted_average += (worth * assessment.score_percent)
                flash(weighted_average)

                #update the selected module module
                module = models.Modules.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).first()
                module.average = weighted_average
                db.session.commit()
                flash("Module Information Successfully Updated")

                #calculate targets
                #more than one assessment left
                flash(sumofTakenAssessments)
                worthOfFinalAssessment = 100 - sumofTakenAssessments
                numberOfAssessmentsLeft = module.num_of_assessments - num_of_assessments
                gradeForAFirst = ((70 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                gradeForATwoOne = ((60 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                gradeForATwoTwo = ((50 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                gradeForAPass = ((40 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                output = f"Your current grade is {weighted_average}%."
                output += f"You have {numberOfAssessmentsLeft} assessments left worth a total of {worthOfFinalAssessment}%."
                output += f"You need {gradeForAFirst}% over the next {numberOfAssessmentsLeft} assessments to get a first"


                flash(output)
            # if user clicks a button, check if the button is the back button
            clicked = request.form['back_button']
            if clicked == 'back-to-module':
                flash(clicked)
                return redirect(url_for('view_assessments'))
        except Exception as e:
            app.logger.critical(e)
            flash(e)

    return render_template('add_assessment.html',
                            title=title,
                            header=header,
                            form=form,
                            selected_module = selected_module,
                            student_id = current_user.name)

@app.route('/view_assessments', methods=['GET','POST'])
@login_required
def view_assessments():
    app.logger.info('view assessment route request')
    title = "View"
    header = "View"
    selected_module = session.get('selected_module', None)
    module =  models.Modules.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).first()
    module_title = module.title
    if request.method == 'POST':
        try:
            #get the button value & convert it to an integer
            clicked = request.form['button']
            if clicked == 'add-assessment':
                flash(clicked)
                #check that user can add assessment else raise exception
                student_modules = models.Modules.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all() #get module information
                count = 0 # count for the number of modules
                for m in student_modules:
                    if m.module_code == selected_module:
                        module = m
                assessments = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()
                for a in assessments:
                    count+=1
                flash(count)
                flash(module.num_of_assessments)

                if count >= module.num_of_assessments:
                    app.logger.info('user has added the maximum number of assessments for module {selected_module}')
                    raise Exception('You have added the maximum number of assessment for this module')
                else:
                    return redirect(url_for('add_assessment'))
            elif clicked == 'back-to-dashboard':
                return redirect(url_for('dashboard'))
            else:#deleting assessment
                if 'delete-assessment' in clicked:
                    flash('deleting assessment')
                    title = clicked[18:]
                    flash(title)
                    assessments = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()
                    for assessment in assessments:
                        if(title == assessment.title):
                            db.session.delete(assessment)
                    db.session.commit()
                    #update the module's average
                    assessments = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()
                    weighted_average = 0
                    for assessment in assessments:
                        worth = assessment.assessment_worth / 100
                        weighted_average += (worth * assessment.score_percent)
                    flash(f'weighted_average: {weighted_average}')
                    #update the selected module module
                    module = models.Modules.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).first()
                    flash(module)
                    module.average = weighted_average
                    db.session.commit()
                    flash("Module Information Successfully Updated")

        except Exception as e:
            app.logger.critical(e)
            flash(e)

    # data = models.Assessments.query.all()
    data = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()

    return render_template('view_assessments.html',
                            title=title,
                            header=header,
                            name=current_user.name,
                            module_title = module.title,
                            selected_module = selected_module,
                            data=data)


