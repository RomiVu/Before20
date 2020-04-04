from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from ..models import User


class EditProfileForm(FlaskForm):
    #ecaptchaField = RecaptchaField()
    name = StringField(label='Edit Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField(label='Edit Email Address', validators=[DataRequired(), Email(message="this is not a vaild email address.")])
    about_me = TextAreaField(label='About me...', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(user, User):
            self.ori_name = user.name
            self.ori_email = user.email
            self.ori_about_me = user.about_me
        else:
            raise TypeError('Should Be a models.User instance')

    def validate_user(self, name):
        if name.data == self.ori_name:
            return
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError(f"username:{name.data} already exiseted.")

    def validate_email(self, email):
        if email.data == self.ori_email:
            return
        user = User.query.filter_by(email=email.data).first()
        if user is not None and user.name != self.ori_name:
            raise ValidationError(f"email:{email.data} already exiseted.")


class PostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired(), Length(min=1, max=80)])
    body = TextAreaField(label='Writing your post', validators=[DataRequired(),  Length(min=1, max=140)])
    submit = SubmitField("Submit")