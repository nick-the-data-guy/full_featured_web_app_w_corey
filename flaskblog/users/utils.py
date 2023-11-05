import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# This save_picture function gets called by the account route.
# It does a few things:

# 1. brings in the filename of the uploaded photo, gets the extension (ie. '.jpg', '.png').
# 2. creates a random string of characters (ie. '347b6fb31d60c500')
# 3. creates a new filename by joining  the string of characters to the extension (ie. '347b6fb31d60c500.jpg')
# 4. calculates the path where the picture will be saved
# 5. creates a 125x125 thumbnail of the save_picture
# 6. saves the thumbnail to the path
# 7. returns the new filename


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	output_size = (125,125)
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
