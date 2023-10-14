from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

# this is where you import the forms you created in the forms.py file
from forms import RegistrationForm, LoginForm




app=Flask(__name__)

# secret keys protects against modifying cookies and cross-site forgery attacks
# you want this to be a bunch of random characters.
#  to get a random key:
# $ python
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = 'ef931caa57f5dcc01a77ba311507ade0'


# This line configures SQLALCHEMY to point to a SQLITE database called 'site.db'.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db=SQLAlchemy(app)



# This line I needed to add to make the db.Create_all() command work.

# The new way of creating the db:

# 1. $ python
# 2. >>> from flaskblog import app
# 3. >>> from flaskblog import db
# 4. db.create_all()

# This will create the instance folder and site.db file.
app.app_context().push()

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




# A sqlalchemy class is the same as a table in a normal relational database.
# These are also known as models.

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	# This line creates a relationship between User and Post, where an alias called 'author' is created to 
	# join a user to a post.
	# When post.author is called, it will look at the post, figure out that there is a foreign key user_id 
	# which calls back to to a user, and the return function for user executes. 
	posts=db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}',{self.email}',{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}',{self.date_posted}')"



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




if __name__ == "__main__":
	app.run(debug=True)