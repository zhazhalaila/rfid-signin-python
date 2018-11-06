from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Student, Class


class ModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
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

if __name__ == '__main__':
	unittest.main(verbosity=2)