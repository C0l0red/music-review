from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError, Email
from app.models import User

class ProfileForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    email = StringField("Email", [Email()])
    
    