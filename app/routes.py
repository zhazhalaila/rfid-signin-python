from flask import render_template, flash, redirect, url_for, jsonify
from app import app, db
from app.forms import RegisterClass, LogIn, InsertStudent
from datetime import datetime, timedelta
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Class, Student, Timetable
from werkzeug.urls import url_parse
from flask import request
import redis, os

r = redis.from_url(os.environ['REDISCLOUD_URL'])
current_class = []
no_duplicate = []

def get_current_classes():
	classes = list(r.hgetall("simultaneously").values())
	curr_time = datetime.now()
	for class_ in classes:
		curr_class = Class.query.filter_by(class_id=class_.decode('utf-8')).first_or_404()
		last_seen = curr_class.last_seen
		if curr_time - last_seen > timedelta(minutes=1):
			r.hdel("simultaneously", class_)


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.now()
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
	current_class.append(current_user.class_id)
	no_duplicate = list(set(current_class))
	print(no_duplicate)
	for i in no_duplicate:
		r.hset("simultaneously", i, i)
	currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	r.set('curr_token', current_user.class_token)
	return render_template('index.html', currentTime=currentTime)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LogIn()
	if form.validate_on_submit():
		class_ = Class.query.filter_by(class_token=form.token.data).first()
		if class_ is None or not class_.check_password(form.password.data):
			return redirect(url_for('index'))
		login_user(class_, remember=True)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
		return redirect(url_for('index'))
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterClass()
	if form.validate_on_submit():
		class_ = Class(class_name=form.className.data, class_token=form.classToken.data,
				class_teacher=form.classTeacher.data)
		class_.set_password(form.classPassword.data)
		db.session.add(class_)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/class/<class_name>')
@login_required
def get_class(class_name):
	class_ = Class.query.filter_by(class_name=class_name).first_or_404()
	students = class_.get_student().all()
	items = []
	today_str = datetime.now().strftime('%Y-%m-%d')
	print(today_str)
	today_format = datetime.strptime(today_str, "%Y-%m-%d")
	for student in students:
		curr_log_info = Timetable.query.filter_by(time_class_id=class_.class_id).filter_by(
			time_student_id = student.student_id
			).filter(
			Timetable.time_time > today_format
			).filter(
			Timetable.time_time < today_format + timedelta(hours=24)
			).first()
		if curr_log_info is None:
			active = False
		else:
			active = curr_log_info.active
		items.append((student, active))
	currentTime = class_.last_seen
	return render_template('class.html', class_=class_, currentTime=currentTime, items=items)

@app.route('/class/<class_name>/submit')
@login_required
def post_result(class_name):
	class_ = Class.query.filter_by(class_name=class_name).first_or_404()
	students = class_.get_student().all()
	today_str = datetime.now().strftime('%Y-%m-%d')
	today_format = datetime.strptime(today_str, "%Y-%m-%d")
	for student in students:
		curr_log_info = Timetable.query.filter_by(time_class_id=class_.class_id).filter_by(
			time_student_id = student.student_id
			).filter(
			Timetable.time_time > today_format
			).filter(
			Timetable.time_time < today_format + timedelta(hours=24)
			).first()
		if curr_log_info is None:
			write_log_info = Timetable(time_class_name=class_.class_name,
				time_class_id=class_.class_id,
				time_student_id=student.student_id,
				time_time=datetime.now(),
				active=False)
			db.session.add(write_log_info)
			db.session.commit()
	return redirect(url_for('get_class', class_name=current_user.class_name))

@app.route('/insert/<class_name>', methods=['GET', 'POST'])
@login_required
def insert_student(class_name):
	form = InsertStudent()
	class_ = Class.query.filter_by(class_name=class_name).first_or_404()
	if form.validate():
		student = Student.query.filter_by(student_name=form.studentName.data).first()
		if student is None:
			student = Student(rfid_id=form.rfidId.data, student_number=form.studentNumber.data, student_name=form.studentName.data)
			db.session.add(student)
		class_.insert(student)
		db.session.commit()
		return redirect(url_for('get_class', class_name=current_user.class_name))
	return render_template('addStudent.html', form=form)

@app.route('/signin')
def signin():
	get_current_classes()
	classes = list(r.hgetall("simultaneously").values())
	rfid_id = request.args.get('rfid_id')
	for class_ in reversed(classes):
		curr_class = Class.query.filter_by(class_id=class_.decode('utf-8')).first_or_404()
		students = curr_class.get_student().all()
		for student in students:
			if student.rfid_id == rfid_id:
				log_info = Timetable(time_class_name=curr_class.class_name,
					time_class_id=curr_class.class_id,
					time_student_id=student.student_id,
					time_time=datetime.now(),
					active=True)
				db.session.add(log_info)
				db.session.commit()
				return student.student_name
	return rfid_id

@app.route('/online')
def online():
	get_current_classes()
	online_class = []
	for i in r.hgetall("simultaneously").values():
		class_ = Class.query.filter_by(class_id=i.decode('utf-8')).first_or_404()
		online_class.append(class_)
	return render_template('onlineclass.html', online_class=online_class)

@app.route('/student/search')
def student_search():
	return render_template('student_search.html')

@app.route('/api/student_history')
def student_history():
	name = request.args.get('name')
	student = Student.query.filter_by(student_name=name).first_or_404()
	history = Timetable.query.filter_by(time_student_id=student.student_id).all()
	print(history)
	json_list = []
	for i in range(0, len(history)):
		dict_format = {}
		dict_format['class_name'] = history[i].time_class_name
		dict_format['time'] = history[i].time_time.strftime('%Y-%m-%d %H:%M:%S')
		dict_format['active'] = history[i].active
		json_list.append(dict_format)
	print(json_list)
	return jsonify({'history': json_list})

@app.route('/class/search')
def class_search():
	return render_template('class_search.html')

@app.route('/api/class_history')
def class_history():
	class_name = request.args.get('name')
	class_ = Class.query.filter_by(class_name=class_name).first_or_404()
	students = class_.get_student().all()
	time = request.args.get('time')
	time_format = datetime.strptime(time, "%Y-%m-%d")
	history = []
	for student in students:
		log_info = Timetable.query.filter_by(time_class_id=class_.class_id).filter_by(
			time_student_id = student.student_id
			).filter(
			Timetable.time_time > time_format
			).filter(
			Timetable.time_time < time_format + timedelta(hours=24)
			).first()
		dict_format = {}
		dict_format['name'] = student.student_name
		dict_format['time'] = log_info.time_time.strftime('%Y-%m-%d %H:%M:%S')
		dict_format['active'] = log_info.active
		history.append(dict_format)
	return jsonify({'history': history})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))