from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

#instance of the posts package 
posts = Blueprint('posts',__name__)

#creating a new post 
@posts.route("/post/new",methods=['POST','GET'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('your post has been created','success')
		return redirect(url_for('main.home'))
	return render_template('create_update_post.html',title='new_post',
							form=form,legend="new post")


#show particular post 
@posts.route("/post/<int:post_id>",methods=['GET'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html',title= post.title,post=post)


#update post 
@posts.route("/post/<int:post_id>/update",methods=['POST','GET'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
		flash('permession deneid','danger')
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('your post has been updated','success')
		return redirect('main.home')
	return render_template('create_update_post.html',form=form,legend='update post')


#deleting a post
@posts.route('/post/<int:post_id>/delete',methods=['POST','GET'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
		flash('permession deneid','danger')
	db.session.delete(post)
	db.session.commit()
	flash('your post has been deleted','success')
	return redirect(url_for('main.home'))