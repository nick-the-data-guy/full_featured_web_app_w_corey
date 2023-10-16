

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



from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.models import User, Post
# this is where you import the forms you created in the forms.py file
from flaskblog.forms import RegistrationForm, LoginForm


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
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)




#################
## login route ##
#################
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password.', 'danger')
	return render_template('login.html', title='Login', form=form)

