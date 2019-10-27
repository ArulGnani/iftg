#every package has its own routes / forms / db / templates
from flask import render_template,request,Blueprint
from flaskblog.models import Post,User

#instance of the main package
main = Blueprint('main',__name__)

#every route should have the instance of the main package
#so instance.route('/route_name/')
#home route n function
@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=4)
	return render_template("home.html",posts=posts)


#about route n function
@main.route("/about")
def about():
	users = User.query.all()
	pst = Post.query.all()
	total_post = len(pst)
	total_user = len(users)	
	return render_template("about.html",title='about',total_user=total_user,total_post=total_post)

#list all the registred user's
@main.route('/members')
def members():
	users = User.query.all()
	return render_template("members.html",title="members",users=users)