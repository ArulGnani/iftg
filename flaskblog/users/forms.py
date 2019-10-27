from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


#create an register-form 
class RegistionForm(FlaskForm):
	username = StringField('username',
							validators=[DataRequired(),Length(min=5,max=20)])
	email = StringField('email',
						validators=[DataRequired(),Email()])
	password = PasswordField('password',validators=[DataRequired()])
	confirm_password = PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('sign up')

	#validation for database check //check's for the usernaem in database 
	#if username found in db then return error  
	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('that username already exist please choice another one')
	
	#db validation for email
	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('that email id is already taken please choice another one')	
					


#create an login-form 
class LoginForm(FlaskForm):
	email = StringField('email',
						validators=[DataRequired(),Email()])
	password = PasswordField('password',validators=[DataRequired()])
	remember = BooleanField('rember me')
	submit = SubmitField('login') 

#create an updateform
class UpdateAccountForm(FlaskForm):
	username = StringField('username',
							validators=[DataRequired(),Length(min=5,max=20)])
	email = StringField('email',
						validators=[DataRequired(),Email()])
	picture = FileField('update profile picture',validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('update')

	#check for change in account name with the name in database 
	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('that username already exist please choice another one')
	
	#check for change in account name with the eamil in database
	def validate_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('that email id is already taken please choice another one')

	
#reset password form / for email  
class RequestResetForm(FlaskForm):
	email = StringField('email',validators=[DataRequired(),Email()]) 
	submit = SubmitField('request password reset')

	#check for valid email of the user
	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('invalid email. email not found')


#reset password form / for password
class ResetPasswordForm(FlaskForm):
	password = PasswordField('password',validators=[DataRequired()])
	confirm_password = PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('reset password')	


