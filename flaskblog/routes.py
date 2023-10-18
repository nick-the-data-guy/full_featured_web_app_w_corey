

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



from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
# this is where you import the forms you created in the forms.py file
from flaskblog.forms import RegistrationForm, LoginForm
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
@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')