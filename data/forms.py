from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()],
                        render_kw={"placeholder": "Login"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    password_again = PasswordField('Repeat Password',
                                   validators=[DataRequired()],
                                   render_kw={"placeholder": "Repeat Password"})
    card_id = IntegerField('Card ID',validators=[DataRequired()],
                        render_kw={"placeholder": "Your card ID here"})
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()],
                        render_kw={"placeholder": "Login"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')
