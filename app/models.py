from app import db

class Assessments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), index=True)
    marks = db.Column(db.Integer)
    percent = db.Column(db.Float)
    worth = db.Column(db.Integer)

class Modules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), index=True)
    module_code = db.Column(db.String(1000))
    num_of_assessments = db.Column(db.Integer)
    average = db.Column(db.Integer)
    credit = db.Column(db.Integer)