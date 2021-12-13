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
        app.logger.info('user already authenticated. redirecting to dashboard.')
        return redirect(url_for('dashboard'))

    title = "Homepage"
    
    if request.method == 'POST':
        try:
            #get the value of the button clicked
            clicked_button = request.form['button']
            #check which button was clicked
            if clicked_button == 'login':
                # flash(clicked_button, 'alert alert-info')
                return redirect(url_for('login'))
            elif clicked_button == 'signup':
                # flash(clicked_button, 'alert alert-info')
                return redirect(url_for('signup'))
        except Exception as e:
            app.logger.error(e)
            flash(e, 'alert alert-danger')
    return render_template('index.html',
                            title=title)


@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        app.logger.info('user already logged in! redirected to dashboard')
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
                db.session.add(p) # add to database
                db.session.commit() # commit data
                flash('Sign up successful! Please login!', 'alert alert-success')
                return redirect(url_for('login')) #redirect to login page

            if form.errors!= {}: #if there are no errors from the validators
                for err_message in form.errors.values():
                    app.logger.info(err_message)
                    flash(f'Error! Unable to create account', "alert alert-danger")

        except Exception as e:
            app.logger.error(e)
            flash(e, 'alert alert-danger')
    return render_template('signup.html',
                            title=title,
                            header=header,
                            form=form,
                            data=data)

@app.route('/login', methods=['GET','POST'])
def login():
    app.logger.info('login route request')
    title = "Login"
    header = "Login"
    form = LoginForm()
    data = models.Students.query.all()
    if current_user.is_authenticated:
        app.logger.info('user already logged in! redirected to dashboard')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                student = models.Students.query.filter_by(username=form.username.data).first()
                if(student):
                    if check_password_hash(student.password, form.password.data):
                        # flash(student.password, 'alert alert-info')
                        login_user(student, remember=form.remember.data)
                        student.authenticated = True
                        app.logger.info('user authenticated. logging in...')
                        return redirect(url_for('dashboard'))
                    else:
                        raise Exception('Invalid username or password! Please try again!')
        except Exception as e:
            app.logger.error(e)
            flash(e, 'alert alert-danger')

    return render_template('login.html',
                            title=title,
                            header=header,
                            data =data,
                            form=form)

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    title="Account"
    header="Account"
    if request.method == 'POST':
        try:
            #get the value of the button clicked
            clicked_button = request.form['button']
            #check which button was clicked
            if clicked_button == 'change-password':
                # flash(clicked_button, 'alert alert-info')
                return redirect(url_for('edit_password'))
            elif clicked_button == 'logout':
                return redirect(url_for('logout'))
        except Exception as e:
            flash(e, 'alert alert-danger')
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
        #get the value of the button clicked
        clicked_button = request.form['button']
        # flash(clicked_button, 'alert alert-danger')
        #check which button was clicked
        try:
            if clicked_button == 'back-to-account':
                return redirect('account')
            if form.validate_on_submit():
                student = models.Students.query.filter_by(id=current_user.id).first()
                if(student): #if the user is found
                    if check_password_hash(student.password, form.old_password.data): #compare inputed old password with password on database
                        if check_password_hash(student.password, form.new_password.data): #check if the new password is the same as old password
                            raise Exception("New password is the same as old password")
                        else:
                            student.password = generate_password_hash(form.new_password.data , method='sha256')
                            db.session.commit()
                            app.logger.info('password changed successful')
                            flash('Password changed successfully', 'alert alert-success')
                            return redirect(url_for('account'))
                    else:
                        raise Exception("You have entered an incorrect old password")
        except Exception as e:
            flash(e, 'alert alert-danger')
            app.logger.warning(e)
    return render_template('edit_password.html',
                            title=title,
                            header=header,
                            form=form)


@app.route('/logout', methods=['GET','POST'])
def logout():
    app.logger.info('logout route request')
    session.clear()
    logout_user()
    app.logger.info('user logged out')
    flash('Logged out successfully!', 'alert alert-success')
    return redirect(url_for('login'))


#displays all the modules
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    app.logger.info('dashboard route request')
    title = "Dashboard"
    header = "Dashboard"
    form=ButtonForm()

    #check if request method is POST
    if request.method == 'POST':
        try:
            #get the button value
            clicked = request.form['button']
            # flash(clicked, 'alert alert-info')
            if clicked == 'add-module':
                # flash(clicked, 'alert alert-info')
                app.logger.info('user clicked add module button. redirecting to add module page...')
                return redirect(url_for('add_module'))
            else: # view module
                if 'delete-module' in clicked: # deleting the module
                    app.logger.info('user clicked delete module button...')
                    
                    module_code = clicked[14:] #get substring containing only module code
                    #get all modules
                    module = models.Modules.query.filter_by(student_id=current_user.id).filter_by(module_code=module_code).first()
                    assessments = models.Assessments.query.filter_by(module_code=module_code).filter_by(student_id=current_user.id).all()
                    for assessment in assessments:
                        db.session.delete(assessment)
                    db.session.delete(module)
                    db.session.commit()
                    flash('Module deleted successfully', 'alert alert-success')
                    app.logger.info(f'module "{module.module_code}:{module.title}" successfully deleted')
                else: # viewing the module
                    # flash(clicked, 'alert alert-info')
                    session['selected_module'] = clicked #you can use AJAX as well to pass data betwen the pages
                    app.logger.info(f'user clicked view module button: viewing module {clicked}')
                    return redirect(url_for('view_assessments'))
        except Exception as e:
            app.logger.critical(e)
            flash(e, 'alert alert-danger')

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

    if request.method == 'POST':
        flash("Request Method is POST")
        clicked = request.form['button']
        try:
            #check if back to dashboard button clicked
            if clicked == 'Back to dashboard':
                flash(clicked, 'alert alert-info')
                return redirect(url_for('dashboard'))

            # if form.validate_on_submit():
            if clicked == 'Add module':
                # get a list of all the modules
                data = current_user.modules
                # check if module code already exists
                for module in data:
                    if module.module_code == form.module_code.data:
                        raise Exception(f'Please add a different module! You have already added a module with the same code!')

                #This code will run if there are no duplicate modules
                p = models.Modules( title=form.title.data,
                                    credit = form.num_of_credits.data,
                                    num_of_assessments=form.num_of_assessments.data,
                                    completed_assessments = 0,
                                    student_id = current_user.id,
                                    module_code = form.module_code.data)
                # add to database
                db.session.add(p) 
                current_user.modules.append(p)
                db.session.commit()
                flash("Module successfully added", 'alert alert-info')
                return redirect(url_for('dashboard'))     

        except Exception as e:
            app.logger.error(e)
            flash(e, 'alert alert-danger')

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
    selected_module = session.get('selected_module', None)

    if request.method == 'POST':
        # if user clicks a button, check if the button is the back button
        clicked = request.form['button']
        # flash(clicked)
        if clicked == 'Back to modules':
            # flash(clicked, 'alert alert-info')
            return redirect(url_for('view_assessments'))
        try:
            if clicked == 'Add Assessment':
                if form.validate_on_submit(): #check if the form validates
                    #calculate percentage
                    percent = (form.score.data / form.total_marks.data)* 100

                    p = models.Assessments( title = (form.title.data).strip(),
                                            score = form.score.data,
                                            total_marks = form.total_marks.data,
                                            score_percent = percent,
                                            assessment_worth = form.assessment_worth.data,
                                            module_code= selected_module,
                                            student_id = current_user.id)
                    db.session.add(p) # add to database
                    db.session.commit()
                    
                    

                    #calulate weighted avarage and update the right module
                    weighted_average = 0 #how much of the module has been achieved
                    average = 0
                    percent_completed = 0 # total % of the completed assessment
                    num_of_completed_assessments = 0 # number of assesments taken
                    data = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()
                    
                    for assessment in data:
                        num_of_completed_assessments += 1
                        percent_completed += assessment.assessment_worth
                        worth = assessment.assessment_worth / 100
                        weighted_average += (worth * assessment.score_percent)
                        average += assessment.score_percent
                    average = average / num_of_completed_assessments
                    # flash(f'Weighted average {weighted_average}', 'alert alert-info')
                    # flash(f'Percent Completed {percent_completed}%', 'alert alert-info')
                    # flash(f'Number of completed assessements: {num_of_completed_assessments}', 'alert alert-info')
                    # flash(f'Average {average}', 'alert alert-info')

                    #update the selected module module
                    module = models.Modules.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).first()
                    module.average = average
                    module.weighted_average = weighted_average
                    module.percent_completed = percent_completed
                    module.completed_assessments = num_of_completed_assessments
                    
                    db.session.commit()
                    app.logger.info('new assessment added')
                    flash("Assessment successfully added", 'alert alert-success')
                    return redirect(url_for('view_assessments')) 
                    # flash("Module Information Successfully Updated", 'alert alert-success')
                    # #calculate targets
                    # #more than one assessment left
                    # flash(percent_completed, 'alert alert-info')
                    # worthOfFinalAssessment = 100 - percent_completed
                    # numberOfAssessmentsLeft = module.num_of_assessments - num_of_completed_assessments
                    # gradeForAFirst = ((70 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                    # gradeForATwoOne = ((60 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                    # gradeForATwoTwo = ((50 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                    # gradeForAPass = ((40 - weighted_average)/ numberOfAssessmentsLeft) / (worthOfFinalAssessment / numberOfAssessmentsLeft)*100
                    # output = f"Your current grade is {weighted_average}%."
                    # output += f"You have {numberOfAssessmentsLeft} assessments left worth a total of {worthOfFinalAssessment}%."
                    # output += f"You need {gradeForAFirst}% over the next {numberOfAssessmentsLeft} assessments to get a first"
                    # flash(output, 'alert alert-info')
        except Exception as e:
            app.logger.critical(e)
            flash(e, 'alert alert-danger')

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
                # flash(clicked, 'alert alert-info')
                #check that user can add assessment else raise exception
                student_modules = models.Modules.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all() #get module information
                count = 0 # count for the number of modules
                for m in student_modules:
                    if m.module_code == selected_module:
                        module = m
                assessments = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()
                for a in assessments:
                    count+=1
                # flash(count, 'alert alert-info')
                # flash(module.num_of_assessments, 'alert alert-info')

                if count >= module.num_of_assessments:
                    app.logger.info('user has added the maximum number of assessments for module {selected_module}')
                    raise Exception('You have added the maximum number of assessments for this module')
                else:
                    return redirect(url_for('add_assessment'))
            elif clicked == 'back-to-dashboard':
                return redirect(url_for('dashboard'))
            else: #deleting assessment
                if 'delete-assessment' in clicked:
                    # flash('deleting assessment', 'alert alert-info')
                    title = clicked[18:]
                    # flash(title, 'alert alert-info')
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
                    # flash(f'weighted_average: {weighted_average}', 'alert alert-info')
                    #update the selected module module
                    module = models.Modules.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).first()
                    # flash(module, 'alert alert-info')
                    module.weighted_average = weighted_average
                    db.session.commit()
                    app.logger.info('assessment deleted')
                    flash("Assessment successfully deleted", 'alert alert-success')

        except Exception as e:
            app.logger.warning(e)
            flash(e, 'alert alert-info')

    # data = models.Assessments.query.all()
    data = models.Assessments.query.filter_by(module_code=selected_module).filter_by(student_id=current_user.id).all()
    return render_template('view_assessments.html',
                            title=title,
                            header=header,
                            name=current_user.name,
                            module_title = module.title,
                            selected_module = selected_module,
                            data=data)


