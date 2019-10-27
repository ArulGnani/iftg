#database 
from datetime import datetime
from flaskblog import db,login_manager
from flask_login import UserMixin
#password reset
from itsdangerous import TimedJSONWebSignatureSerializer as serilazer
from flask import current_app 

#get the user id from db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#user db
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    
    #password reset -via email
    #function to verify the user //call's its self valid for 10min 
    def get_reset_token(self,expires_sec=600):
        s = serilazer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id }).decode('UTF-8')

    #function to verify the user's request // static-methods it call's its self but token is 
    #passed insted of self
    @staticmethod
    def verify_reset_token(token):
        s = serilazer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


    


#posts db
class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100),nullable=False)
	date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content = db.Column(db.Text,nullable=False)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return f"post('{self.title}','{self.title}')"	
