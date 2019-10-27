from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired ,Length


#post form 
class PostForm(FlaskForm):
	title = StringField('title',validators=[DataRequired(),Length(min=5,max=100)])
	content = TextAreaField('content',validators=[DataRequired()])
	submit = SubmitField('Post')
