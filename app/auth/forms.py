from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, 
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data):
            raise ValidationError("Email address assigned to an account")
        
    def validate_username(self, username):
        if User.query.filter_by(username=userame.data):
            raise ValidationError("Username unavailable")

class LoginForm(FlaskForm):
    user = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])

    def validate(self, *args, **kwargs):
        valid = super(LoginForm, self).validate(*args, **kwargs)

        if valid:
            user = User.query.filter_by(username=self.user.data).first()
            if user:
                if not user.check_password(self.password.data):
                    valid = False
            else:
                valid = False

        return valid

class ResetRequestForm(FlaskForm):
    email = StringField("Email", [DataRequired(), Email()])

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data):
            raise ValidationError("Email account isn't assigned to an account")

class PasswordResetForm(FlaskForm):
    password = PasswordField("New Password", [DataRequired()])
    confirm_password = PasswordField("Confirm New Password", [EqualTo("password", message="Passwords must match")])

    def validate_password(self, password):
        if self.user.check_password(password.data):
            raise ValidationError("Can't use old password")
