import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


#email for password reset // not a route 
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('password reset mail',sender='admin@blog.com',
					recipients=[user.email])
	msg.body = f'''to reset your password click this link below { url_for('users.reset_token',token=token,_external=True)}'''
	mail.send(msg)


#saving a picture in datebase with validation 
def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
	
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

