from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import User, Role
from flask.ext.pagedown.fields import PageDownField

class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    name = StringField('Real name', validators = [Length(0, 64)])
    location = StringField('Location', validators = [Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
class EditProfileAdminForm(Form):
    email = StringField('Email', validators = [Required(), Length(1, 64), Email()])
    username = StringField('Username', validators = [
               Required(), Length(1, 64), Regexp('^[a-zA-Z][a-zA-Z0-9_.]*$', 0, 
                                                 'Username must have only letters, '
                                                 'numbers, dots or underscoresd')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About_me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
           User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self, field):
        if field.data != self.user.username and  \
           User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

            