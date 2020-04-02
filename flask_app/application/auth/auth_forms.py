import re

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from ..models import User


class RegisterForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email(message="this is not a vaild email address.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat your Password', validators=[DataRequired(), EqualTo('password', message="must be same as above")])
    #recaptcha = RecaptchaField()
    submit = SubmitField("Register Now!")
    
    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_password(self, password):
        # todo-lists: password simplicity check
        pass


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    #recaptcha = RecaptchaField()
    submit = SubmitField("Login")


class ResetPasswordForm(FlaskForm):
    username = StringField('name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email(message="this is not a vaild email address.")])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat your Password', validators=[DataRequired(), EqualTo('password', message="must be same as above")])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Reset')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is None:
            raise ValidationError('Please use Your correct username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Please use Your correct Email Address.')