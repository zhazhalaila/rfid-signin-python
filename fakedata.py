from app import db
from app.models import Student, Class, Timetable
from datetime import datetime
import random

def generateRandomTime(year, month, day, hour):
	minute = random.randint(0, 59)
	second = random.randint(0, 59)
	date = datetime(year, month, day, hour, minute, second)
	return date

def generate_class(names):
	fake_class = Class(class_name="TEST", class_token="TEST", class_teacher="Hello")
	fake_class.set_password("password")
	db.session.add(fake_class)

	for i in range(0, 50):
		student_number = '00' + str(i)
		s = Student(student_name=names[i], student_number=student_number)
		db.session.add(s)
		fake_class.insert(s)
	db.session.commit()

def generateTimetable(names):
	fake_class = Class.query.filter_by(class_name="TEST").first()
	class_name = fake_class.class_name
	class_id = fake_class.class_id
	for i in range(0, 20):
		year = 2018
		month = random.randint(8, 12)
		day = random.randint(1, 28)
		hour = random.randint(7, 21)
		for j in range(0, 50):
			student = Student.query.filter_by(student_name=names[j]).first()
			active = random.randint(0, 1)
			t = Timetable(time_class_name=class_name, time_class_id=class_id, time_student_id=student.student_id, 
				time_time=generateRandomTime(year,month,day,hour), active=active)
			db.session.add(t)
	db.session.commit()

file = open("name.txt", "rb")
names = []

for line in file.readlines():
	names.append(line.strip().decode())

generate_class(names)
generateTimetable(names)