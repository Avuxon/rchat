from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User

def invalid_credentials(form, field):
    """ Username and pwd checker for logging in"""
    username_entered = form.username.data
    # Can't use field.data for username since it's being 
    # passed in from the password field
    password_entered = field.data

    # Check username is valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif password_entered != user_object.password:
        raise ValidationError("Username or password is incorrect")
    


class RegistrationForm(FlaskForm):
    """ Registration Form"""

    username = StringField('username_label', 
        validators=[InputRequired(message = "Username required"),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password_label',
        validators=[InputRequired(message = "Password required"),
        Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label',
            validators=[InputRequired(message = "Password required"),
            EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select a different username.")

class LoginForm(FlaskForm):
    """ Login form"""
    username = StringField('username_label', 
        validators=[InputRequired(message = "Username required")])
    # Input required will add attribute required for this string field, default username will be ""  
    password = PasswordField('password_label', 
        validators = [InputRequired(message="Password required"), invalid_credentials])
    # WT Forms automatically sends in form and field (password) to the invalid_credentials 
    # function. Putting this checker function outside is an alternative to what I did in 
    # the registration form

    submit_button = SubmitField('Login')
    

