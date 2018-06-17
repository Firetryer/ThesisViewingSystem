from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from thesisviewing.models import User


class RegisterationForm(FlaskForm):
	id_number = StringField('ID Number', validators=[DataRequired(), Length(min = 2, max = 20)])
	first_name = StringField('First Name', validators=[DataRequired()])
	middle_name = StringField('Middle Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	course_dept = StringField('Course/Department', validators=[DataRequired()])
	year_position = StringField('Year/Position', validators=[DataRequired()])
	user_level = SelectField('Privilege', choices=[('user','User'),('admin', 'Admin')], validators=[DataRequired()])
	password = PasswordField('Password', 
		validators=[DataRequired()])
	password_confirm = PasswordField('Confirm Password', 
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Create Account')

	def validate_id_number(self, id_number):
		id_num = User.query.filter_by(id_number=id_number.data).first()
		if id_num:
			raise ValidationError('Error: That Id Number is already taken. ')
			

class LoginForm(FlaskForm):
	username = StringField('Username', 
		validators=[DataRequired()])
	password = PasswordField('Password', 
		validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField('Login')

class AddThesisForm(FlaskForm):
	thesis_code = StringField('Thesis Code', validators=[DataRequired()])
	title = StringField('Thesis Title', validators=[DataRequired()])
	keywords = StringField('Keywords', validators=[])
	tech_adviser = StringField('Tech Adviser', validators=[DataRequired()])
	class_adviser = StringField('Class Adviser', validators=[DataRequired()])
	researcher = StringField('Researcher', validators=[DataRequired()])
	abstract = TextAreaField('Abstract', validators=[DataRequired()])
	submit = SubmitField('Add Thesis')

class SearchForm(FlaskForm):
	search_words = StringField('Search')
	submit = SubmitField('Search')