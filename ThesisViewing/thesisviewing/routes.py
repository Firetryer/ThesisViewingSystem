from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from thesisviewing import app, db, bcrypt
from thesisviewing.models import User, Thesis, UserLogs
from thesisviewing.forms import RegisterationForm, LoginForm, AddThesisForm



@app.route("/")
@app.route("/home")
@login_required
def homepage():
	return redirect(url_for('view_thesis')) 



@app.route("/view_thesis")
@login_required
def view_thesis():
	thesis = Thesis.query.all()
	return render_template('thesis_viewing.html', post=thesis)




#Admin Pages Below

@app.route("/admin_dashboard")
@login_required
def admin_dash():
	if not current_user.is_admin:
		flash(" Warning: Only admins accounts are allowed in the Admin Dashboard.")
		return redirect(url_for('view_thesis')) 
	return render_template('/admin_pages/admin_landing.html')

@app.route("/admin_dashboard/logs")
@login_required
def admin_logs():
	if not current_user.is_admin:
		flash(" Warning: Only admins accounts are allowed in the Admin Dashboard.")
		return redirect(url_for('view_thesis')) 
	return render_template('/admin_pages/logs.html')

@app.route("/admin_dashboard/thesis_controls")
@login_required
def admin_thesis():
	if not current_user.is_admin:
		flash(" Warning: Only admins accounts are allowed in the Admin Dashboard.")
		return redirect(url_for('view_thesis')) 
	return render_template('/admin_pages/thesis_controls.html')

@app.route("/admin_dashboard/add_thesis", methods=['GET', 'POST'])
@login_required
def admin_add_thesis():
	if not current_user.is_admin:
		flash(" Warning: Only admins accounts are allowed in the Admin Dashboard.")
		return redirect(url_for('view_thesis')) 

	form = AddThesisForm()
	if form.validate_on_submit():
		post = Thesis(
			thesis_code = form.thesis_code.data,
			title = form.title.data,
			keywords = form.keywords.data,
			tech_adviser = form.tech_adviser.data,
			class_adviser = form.class_adviser.data,
			researcher = form.researcher.data,
			abstract = form.abstract.data
			)
		db.session.add(post)
		db.session.commit()
		flash('New Thesis Has Been Added to the Database.', 'success')
		return redirect(url_for('admin_add_thesis'))
	return render_template('/admin_pages/add_thesis.html', title='Add Thesis', form=form)


# Login, Register, Logout Below

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('homepage'))

@app.route("/login",  methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('homepage'))
	if form.validate_on_submit():
		user = User.query.filter_by(id_number=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('view_thesis'))
		else:
			flash('Login Failed. Check Username or Password','danger')
	return render_template('login.html', title = 'login', form=form)


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
