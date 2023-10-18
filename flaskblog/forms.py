
# this is used to handle forms
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
# these are going to be our new forms, inherited from FlaskForm
# each element inside the form gets listed out beneath, and inherits from the wtforms elements imported above.

# the wtforms elements:
# - StringField
# - PasswordField
# - SubmitField
# - BooleanField
# 
# each element has some arguments. the main argument is the label of the form element, 
# followed by validators = [argmument1, argument2]

# the validator arguments are:
# - DataRequired (so empty fields cannot be submitted)
# - Length (so fields must be between x and y number characters)
# - Email (maybe to assure that it follows the pattern text@text.com, that it is a valid email address)
# - EqualTo (maybe to make sure something like a password is equal to a confirm_password)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')