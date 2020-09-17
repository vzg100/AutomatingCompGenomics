from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Equalto

class RegistrationForm(FlaskForm):
	"""docstring for RegistrationForm"""
	username = StringField("username", validators=[DataRequired(), Length(min=2, max=25)])
	email = StringField("email", validators=[DataRequired(), Email()])
	password = 	PasswordField("password", validators=[DataRequired(), Length(min=8)])
	confirm_password = PasswordField("Confirm password", validators=[DataRequired(), Equalto("password")])