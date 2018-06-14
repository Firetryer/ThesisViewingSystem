from flask import render_template, url_for, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required
from thesisviewing import app, db, bcrypt
from thesisviewing.models import User, Thesis, UserLogs
from thesisviewing.forms import RegisterationForm, LoginForm


@app.route("/")
@app.route("/dash")
@app.route("/home")
def homepage():
	if not current_user.is_authenticated:
		flash("Please Log In To Access")
		return redirect(url_for('login')) 
	return render_template('thesis_viewing.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('homepage'))
	form = RegisterationForm()
	if form.validate_on_submit():

		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(
			id_number=form.id_number.data, 
			first_name=form.first_name.data,
			middle_name=form.middle_name.data,
			last_name=form.last_name.data,
			course_dept=form.course_dept.data,
			year_position=form.year_position.data,
			user_level=form.user_level.data,
			password=hashed_password
			)
		db.session.add(user)
		db.session.commit()
		flash(f'Account Created! You may now log in!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form=form)

@app.route("/login",  methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('homepage'))
	if form.validate_on_submit():
		user = User.query.filter_by(id_number=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			print(user.get_id())
			return redirect(url_for('view_thesis'))
		else:
			flash('Login Failed. Check Username or Password','danger')
	return render_template('login.html', title = 'login', form=form)

@app.route("/view_thesis")
def view_thesis():
	if not current_user.is_authenticated:
		flash("Login To Access Thesis Directory")
		return redirect(url_for('login')) 
	return render_template('thesis_viewing.html')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('homepage'))




@app.route("/admin_dashboard")
def admin_dash():
	if not current_user.is_admin:
		flash(" Warning: Only admins accounts are allowed in the Admin Dashboard.")
		return redirect(url_for('view_thesis')) 
	return render_template('/admin_pages/admin_landing.html')

@app.route("/admin_dashboard/logs")
def admin_logs():
	if not current_user.is_admin:
		flash(" Warning: Only admins accounts are allowed in the Admin Dashboard.")
		return redirect(url_for('view_thesis')) 
	return render_template('/admin_pages/logs.html')

@app.route("/admin_dashboard/thesis_controls")
def admin_thesis():
	if not current_user.is_admin:
		flash(" Warning: Only admins accounts are allowed in the Admin Dashboard.")
		return redirect(url_for('view_thesis')) 
	return render_template('/admin_pages/thesis_controls.html')
