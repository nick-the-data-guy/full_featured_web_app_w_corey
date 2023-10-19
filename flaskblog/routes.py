

# NOTE:

# In the tutorial, you are asked to pull data out of the SQLite db using SQLAlchemy code
# rather than SQL. The code presented in the tutorial is:
# >>> user = User.query.get(1) 

# This will generate an error.

# The way around this is to use this code:

# >>> user = db.session.get(User,1)


# NOTE:

# If you want to try to pull data out of your tables using the python interpreter, do this:

# $ python
# >>> from flaskblog import User
# >>> User.query.all()

# This will retrieve all records from the User table.

import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
# this is where you import the forms you created in the forms.py file
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required


posts = [
	
        {
			'author': 'Nick White',
			'title': 'Blog Post 1',
			'content': 'First Post content',
			'date_posted': 'April 20, 2018'

        },

        {
			'author': 'Your Mom',
			'title': 'Your Mom Went To college',
			'content': 'haha haaha',
			'date_posted': 'April 16, 2019'

        }



]






################
## home route ##
################
@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html", posts=posts)



#################
## about route ##
#################
@app.route("/about")
def about():
	return render_template("about.html", title='About')




########################
## registration route ##
########################
@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user= User(username = form.username.data, email = form.email.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in.', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)




##################
## log in route ##
##################
@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password.', 'danger')
	return render_template('login.html', title='Login', form=form)



###################
## log out route ##
###################
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))



###################
## account route ##
###################

# This save_picture function gets called by the account route below.
# It does a few things:

# 1. brings in the filename of the uploaded photo, gets the extension (ie. '.jpg', '.png').
# 2. creates a random string of characters (ie. '347b6fb31d60c500')
# 3. creates a new filename by joining  the string of characters to the extension (ie. '347b6fb31d60c500.jpg')
# 4. calculates the path where the picture will be saved
# 5. creates a 125x125 thumbnail of the save_picture
# 6. saves the thumbnail to the path
# 7. returns the new filename


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	output_size = (125,125)
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn



@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email	
	image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)