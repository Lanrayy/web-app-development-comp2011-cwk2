from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin
from app import login

#user loader
@login.user_loader
def load_user(id):
    return Students.query.get(int(id))

# this table is the link entity between student and module
enrollment = db.Table('enrollment', db.Model.metadata,
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('module_code', db.Integer, db.ForeignKey('modules.module_code'))
)

class Students(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    username = db.Column(db.String(1000), index=True, nullable=False)
    password = db.Column(db.String(1000), nullable= False)

    # def get_id(self):
    #        return (self.user_id)


class Modules(db.Model):
    module_code = db.Column(db.String(1000), primary_key=True)
    title = db.Column(db.String(1000), index=True)
    num_of_assessments = db.Column(db.Integer)
    average = db.Column(db.Integer)
    credit = db.Column(db.Integer)
    modules = db.relationship('Students', secondary='enrollment', backref=db.backref('modules'), lazy='dynamic') #create a back reference in the students table

# # this table is the link entity between modules and assessments
# assessment = db.Table('assessment', db.Model.metadata,
#     db.Column('module_code', db.Integer, db.ForeignKey('modules.module_code'))
#     db.Column('assessment_id', db.Integer, db.ForeignKey('assessments.id'))
# )


class Assessments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), index=True)
    marks = db.Column(db.Integer)
    worth = db.Column(db.Integer)
    percent = db.Column(db.Float)
    module_code = db.Column(db.String(1000), db.ForeignKey('modules.module_code'))
    # modules = db.relationship('Modules', secondary='assessment', backref=db.backref('assessments'), lazy='dynamic')
