from flask import Flask
from flask_sqlalchemy import SQLAlchemy






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

# Any one of these will create the instance folder
# 2. >>> from flaskblog import app
# 3. >>> from flaskblog import db
# 4. >>> from flaskblog.models import User, Post

# This will create the site.db file
# 5. >>> db.create_all()


app.app_context().push()

from flaskblog import routes