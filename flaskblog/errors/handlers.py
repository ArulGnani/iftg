from flask import Blueprint, render_template

errors = Blueprint('errors',__name__)

#handle's all page not found or 404 errors
@errors.app_errorhandler(404)
def error_404(error):
	return render_template('errors/404.html'),404

#handle's all permission denied or 403
@errors.app_errorhandler(403)
def error_404(error):
	return render_template('errors/403.html'),403	

#handle's all server error or 500
@errors.app_errorhandler(500)
def error_404(error):
	return render_template('errors/500.html'),500