import os

class Config:
    # secret keys protects against modifying cookies and cross-site forgery attacks
    # you want this to be a bunch of random characters.
    #  to get a random key:
    # $ python
    # >>> import secrets
    # >>> secrets.token_hex(16)
    SECRET_KEY = os.environ.get('SECRET_KEY')


    # This line configures SQLALCHEMY to point to a SQLITE database called 'site.db'.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # these lines are for mail server configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')