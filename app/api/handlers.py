from flask import jsonify, request
from datetime import datetime, timedelta
from app import app, db
from app.models import Class, Student, Timetable
from app.api import bp

@bp.route('/api/student_history')
def student_history():
	name = request.args.get('name')
	student = Student.query.filter_by(student_name=name).first_or_404()
	history = Timetable.query.filter_by(time_student_id=student.student_id).all()
	json_list = []
	for i in range(0, len(history)):
		dict_format = {}
		dict_format['class_name'] = history[i].time_class_name
		dict_format['time'] = history[i].time_time.strftime('%Y-%m-%d %H:%M:%S')
		dict_format['active'] = history[i].active
		json_list.append(dict_format)
	return jsonify({'history': json_list})

@bp.route('/api/class_history')
def class_history():
	class_name = request.args.get('name')
	class_ = Class.query.filter_by(class_name=class_name).first_or_404()
	print(class_)
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
		try:
			dict_format['time'] = log_info.time_time.strftime('%Y-%m-%d %H:%M:%S')
		except:
			pass
		try:
			dict_format['active'] = log_info.active
		except:
			dict_format['active'] = False
		history.append(dict_format)
	return jsonify({'history': history})