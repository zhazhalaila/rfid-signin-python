from datetime import datetime, timedelta
import unittest, random
from app import app, db
from app.models import Student, Class, Timetable

class ModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		c = Class(class_name='test1', class_token='test1', class_teacher='test1')
		c.set_password('test1')
		self.assertFalse(c.check_password('test'))
		self.assertTrue(c.check_password('test1'))

	def test_insert(self):
		s = Student(student_name='lalala')
		c = Class(class_name='test2')
		db.session.add(s)
		db.session.add(c)
		self.assertEqual(c.students.all(), [])

		c.insert(s)
		db.session.commit()
		self.assertTrue(c.is_inserting(s))
		self.assertEqual(c.students.count(), 1)
		self.assertEqual(c.students.first().student_name, 'lalala')

		c.uninsert(s)
		db.session.commit()
		self.assertFalse(c.is_inserting(s))
		self.assertEqual(c.students.count(), 0)
		
	def test_get_students(self):
		s1 = Student(student_name="s_1")
		s2 = Student(student_name="s_2")
		s3 = Student(student_name="s_3")
		s4 = Student(student_name="s_4")
		db.session.add_all([s1, s2, s3, s4])
		
		c = Class(class_name="test3")
		db.session.add(c)
		c.insert(s1)
		c.insert(s2)
		c.insert(s3)
		c.insert(s4)
		db.session.commit()
		
		f1 = c.get_student().all()
		self.assertEqual(f1, [s1, s2, s3, s4])

	def test_generate_class(self):
		fake_class = Class(class_name="LAST", class_token="LAST")
		fake_class.set_password("password")
		db.session.add(fake_class)
		names = self.get_name()
		for i in range(0, 50):
			s = Student(student_name=names[i])
			db.session.add(s)
			fake_class.insert(s)
		db.session.commit()
		length = len(fake_class.get_student().all())
		self.assertEqual(length, 50)
		self.assertEqual(self.generate_timetable(), 1000)

	def generate_timetable(self):
		fake_class = Class.query.filter_by(class_name="LAST").first()
		class_name = fake_class.class_name
		class_id = fake_class.class_id
		names = self.get_name()
		for i in range(0, 20):
			year = 2018
			month = random.randint(8, 12)
			day = random.randint(1, 28)
			hour = random.randint(7, 21)
			for j in range(0, 50):
				student = Student.query.filter_by(student_name=names[j]).first()
				active = random.randint(0, 1)
				t = Timetable(time_class_name=class_name, time_class_id=class_id, time_student_id=student.student_id, 
					time_time=self.generate_random_time(year,month,day,hour), active=active)
				db.session.add(t)
			length = len(Timetable.query.filter_by(time_class_name=class_name).all())
		return length

	def get_name(self):
		file = open("name.txt", "rb")
		names = []

		for line in file.readlines():
			names.append(line.strip().decode())
		return names

	def generate_random_time(self, year, month, day, hour):
		minute = random.randint(0, 59)
		second = random.randint(0, 59)
		date = datetime(year, month, day, hour, minute, second)
		return date

if __name__ == '__main__':
	unittest.main(verbosity=2) #test