from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime

student_identifier = db.Table('student_identifier',
    db.Column('class_id', db.Integer, db.ForeignKey('classes.class_id')),
    db.Column('student_id', db.Integer, db.ForeignKey('students.student_id'))
)

class Student(db.Model):
	__tablename__ = 'students'
	student_id = db.Column(db.Integer, unique=True, primary_key=True)
	rfid_id = db.Column(db.String(64), index=True, unique=True)
	student_number = db.Column(db.String(64), index=True, unique=True)
	student_name = db.Column(db.String(64), index=True, unique=True)
	student_nickname = db.Column(db.String(64), nullable=False, default='')
	curr_active = db.Column(db.Boolean, nullable=False, default=False)

class Timetable(db.Model):
	__tablename__ = 'timetable'
	time_id = db.Column(db.Integer, unique=True, primary_key=True)
	time_class_name = db.Column(db.String(128), index=True)
	time_class_id = db.Column(db.Integer, index=True)
	time_student_id = db.Column(db.Integer, index=True)
	time_time = db.Column(db.DateTime, default=datetime.now())
	active = db.Column(db.Boolean, nullable=False, default=False)
	
class Class(UserMixin, db.Model):
	__tablename__ = 'classes'
	class_id = db.Column(db.Integer, primary_key=True)
	class_name = db.Column(db.String(128), index=True)
	class_token = db.Column(db.String(128), unique=True)
	class_teacher = db.Column(db.Integer, index=True)
	password_hash = db.Column(db.String(128))
	last_seen = db.Column(db.DateTime, default=datetime.now())
	students = db.relationship("Student", 
		secondary=student_identifier,
		backref=db.backref('classes', lazy='dynamic'), lazy='dynamic')

	def get_id(self):
		return self.class_id

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avastar(self, size):
		digest = md5(self.class_token.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

	def insert(self, student):
		if not self.is_inserting(student):
			self.students.append(student)

	def uninsert(self, student):
		if self.is_inserting(student):
			self.students.remove(student)

	def is_inserting(self, student):
		return self.students.filter(
			student_identifier.c.student_id == student.student_id).count() > 0

	def get_student(self):
		return Student.query.join(
			student_identifier, student_identifier.c.student_id == Student.student_id).filter(
			student_identifier.c.class_id == self.class_id)

@login.user_loader
def load_user(id):
	return Class.query.get(int(id))