from thesisviewing import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

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
	
	def full_name(self):
		if not self.middle_name :
			return self.first_name + ' ' + self.middle_name +  '' + self.last_name
		else: 
			return self.first_name + '' + self.last_name
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
	available = db.Column(db.Boolean, default=True)
	views = db.relationship('UserLogs', backref='thesis', lazy=True)


class UserLogs(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	id_number = db.Column(db.VARCHAR(50), db.ForeignKey('user.id_number'),nullable = False)
	thesis_code = db.Column(db.VARCHAR(100),db.ForeignKey('thesis.thesis_code'), nullable = False)
	name = db.Column(db.VARCHAR(100), nullable = False)
	date_time = db.Column(db.DateTime, nullable = False)
	user_level = db.Column(db.VARCHAR(50), nullable = False)

	def __repr__(self):
		return f"User('{self.id_number}', '{self.name}', '{self.date_time}', '{self.user_level}')"