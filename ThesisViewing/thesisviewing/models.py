from thesisviewing import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id_number = db.Column(db.VARCHAR(50), unique = True, primary_key = True)
	first_name = db.Column(db.VARCHAR(50), nullable = False)
	middle_name = db.Column(db.VARCHAR(50), nullable = True)
	last_name = db.Column(db.VARCHAR(50), nullable = False)
	course_dept = db.Column(db.VARCHAR(100), nullable = False)
	year_position = db.Column(db.VARCHAR(50), nullable = False)
	user_level = db.Column(db.VARCHAR(50), nullable = False)
	password = db.Column(db.VARCHAR(100), nullable = False)
	logs = db.relationship('UserLogs', backref='user', lazy=True)
	
	def __repr__(self):
		return f"User('{self.id_number}', '{self.course_dept}')"
	def full_name(self):
		return self.first_name + ' ' + self.middle_name +  '' + self.last_name
	def get_id(self):
		return self.id_number
	def is_admin(self):
		return self.user_level == 'admin'

class Thesis(db.Model):
	thesis_code = db.Column(db.VARCHAR(50), primary_key = True)
	title = db.Column(db.VARCHAR(50))
	keywords = db.Column(db.VARCHAR(50))
	tech_adviser = db.Column(db.VARCHAR(50))
	class_adviser = db.Column(db.VARCHAR(50))
	researcher = db.Column(db.VARCHAR(50))
	abstract = db.Column(db.VARCHAR(200))

	def __repr__(self):
		return f"User('{self.thesis_code}', '{self.title}', '{self.abstract}', '{self.keywords}')"

class UserLogs(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.VARCHAR(50), db.ForeignKey('user.id_number'),nullable = False)
	name = db.Column(db.VARCHAR(100), nullable = False)
	date_time = db.Column(db.DateTime, nullable = False)
	user_level = db.Column(db.VARCHAR(50), nullable = False)

	def __repr__(self):
		return f"User('{self.username}', '{self.name}', '{self.date_time}', '{self.user_level}')"