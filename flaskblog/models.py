from datetime import datetime
from flaskblog import db


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
