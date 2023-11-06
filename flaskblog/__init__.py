from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config




app=Flask(__name__)
app.config.from_object(Config)


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail=Mail(app)

# This line I needed to add to make the db.Create_all() command work.

# The new way of creating the db:

# 1. $ python

# Any one of these will create the instance folder
# 2. >>> from flaskblog import app
# 3. >>> from flaskblog import db
# 4. >>> from flaskblog.models import User, Post

# This will create the site.db file
# 5. >>> db.create_all()


app.app_context().push()

from flaskblog.users.routes import users
app.register_blueprint(users)

from flaskblog.posts.routes import posts
app.register_blueprint(posts)

from flaskblog.main.routes import main
app.register_blueprint(main)