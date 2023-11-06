from datetime import datetime

# This is the original Serializer from the original code, which no longer works as of Nov 1 2023
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# This is the new Serializer.
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# A sqlalchemy class is the same as a table in a normal relational database.
# These are also known as models.

class User(db.Model, UserMixin):
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

	# This get_reset_token() section is the original code, which no longer works as of Nov 1 2023.
	# The working section is right below.
	# def get_reset_token(self, expires_sec=1800):
	# 	s = Serializer(app.config['SECRET_KEY'], expires_sec)
	# 	return s.dumps({'user_id': self.id}).decode('utf-8')	
	# #######################################################

	# This is the working get_reset_token().
	def get_reset_token(self):
		s = Serializer(current_app.secret_key)
		return s.dumps({'user_id': self.id})
	# ########################################


	# This verify_reset_token() section is the original code, which no longer works as of Nov 1 2023.
	# @staticmethod
	# def verify_reset_token(token):
	# 	s = Serializer(app.config['SECRET_KEY'])
	# 	try:
	# 		user_id = s.loads(token)['user_id']
	# 	except:
	# 		return None
    # 	return User.query.get(user_id)
	# ###########################################


	# this is the working verify_reset_token().
	@staticmethod
	def verify_reset_token(token):
		s=Serializer(current_app.secret_key)
		try:
			user_id=s.loads(token, max_age=1800)['user_id']
		except:
			return None
		return User.query.get(user_id)
	# ##########################################################

	def __repr__(self):
		return f"User('{self.username}',{self.email}',{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"

