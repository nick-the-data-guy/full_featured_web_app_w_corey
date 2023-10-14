
# this is used to handle forms
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField

from wtforms.validators import DataRequired, Length, Email, EqualTo

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





class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')