#instance of flask 
from flask import Flask
#sql database 
from flask_sqlalchemy import SQLAlchemy
#password encrypt
from flask_bcrypt import Bcrypt
#manage session of user
from flask_login import LoginManager
#send eamil 
from flask_mail import Mail
#for blueprint 
from flaskblog.config import Config


#create an instance of db
db = SQLAlchemy()
#create an instance of bcrypt 
bcrypt = Bcrypt()
#login and logout instance
login_manager = LoginManager()
#return to the login view  
login_manager.login_view = 'users.login'
#set the fkash catogery 
login_manager.login_manager_category = 'info'
#mail instace 
mail = Mail()


#create config app  
def create_app(config_class=Config):
	#instance of the app 
	app = Flask(__name__)
	#import config form config class  
	app.config.from_object(Config)

	#insating db
	db.init_app(app)
	#insating bcrypt
	bcrypt.init_app(app)
	#insating login
	login_manager.init_app(app)
	#insating mail
	mail.init_app(app)

	#importing routes 
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors

	#register blueprint packages
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app