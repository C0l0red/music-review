from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError, Email
from app.models import User

class ProfileForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    email = StringField("Email", [Email()])
    
class PasswordChangeForm(FlaskForm):
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField("Confirm Password", [EqualTo("password")])

    def validate_password(self, password):
        if User.check_password(password.data):
            raise ValidationError("Can't use the same password")
    