import os

class Config:
	#to send and get clint side form
	SECRET_KEY = '7386736194510175531'
	#config the database 
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	
	#email service 
	#server setting 
	MAIL_SERVER = 'smtp.gmail.com'
	#server port setting 
	MAIL_PORT = 587
	#no sure about this 
	MAIL_USE_TLS = True
	#email from env variable
	MAIL_USERNAME = os.environ.get('EMAIL')
	#email password from env variable
	MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
	
