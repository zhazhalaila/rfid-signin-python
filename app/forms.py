from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class RegisterClass(FlaskForm):
	className = StringField(validators=[DataRequired()])
	classToken = StringField(validators=[DataRequired()])
	classTeacher = StringField(validators=[DataRequired()])
	classPassword = StringField(validators=[DataRequired()])
	classRepeatPassword = StringField(validators=[DataRequired(), EqualTo('classPassword')])
	submit = SubmitField('注册')

	def validate_token(self, classToken):
		class_ = Class.query.filter_by(classToken=classToken.data).first()
		if class_is is not None:
			raise ValidationError('请输入不同的课程代码')

class InsertStudent(FlaskForm):
	rfidId = StringField(validators=[DataRequired()])
	studentNumber = StringField(validators=[DataRequired()])
	studentName = StringField(validators=[DataRequired()])

class LogIn(FlaskForm):
	token = StringField(validators=[DataRequired()])
	password = StringField(validators=[DataRequired()])