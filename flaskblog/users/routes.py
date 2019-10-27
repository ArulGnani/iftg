from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistionForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


#instance of the user's package 
users = Blueprint('users',__name__)

#register route n function 
@users.route("/register",methods=['POST','GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistionForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
		user = User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('your account has been created,you can login now')
		return redirect(url_for('users.login'))				
	return render_template('register.html',title='register',form=form)

#login route n function
@users.route('/login',methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('login unsuccessful please vheck email and password')
	return render_template('login.html',title='Login',form=form)	
				
#logout route n function 
@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

#account route handels the uesr session
@users.route('/account',methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	user = User.query.filter_by(id=current_user.id).first_or_404()
	page = request.args.get('page',1,type=int)
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())#.paginate(page=page,per_page=5)
	#sample code replace it with pagination 
	total = 0
	for post in posts:
		total += 1 
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('account has been updated','success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
	return render_template('account.html',title='account',image_file=image_file,form=form,posts=posts,user=user,total=total)


#account page
@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page',1,type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())\
								.paginate(page=page,per_page=5)
	return render_template('user_post.html',posts=posts,user=user)


#password reset /email-check-> send a token for verifaction
@users.route('/reset_password',methods=['POST','GET'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('check yout enterd email.','info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html',title='reset password',form=form)


#resetting password / password-check -> reset the password 
@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('that token is invalid try again','warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
		user.password = hashed_password
		db.session.commit()
		flash('your password has reset','success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html',title='reset password',form=form)	





