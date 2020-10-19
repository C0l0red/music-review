from flask import current_app as app, render_template, redirect, Blueprint, url_for
from app import db, login_manager
#from .forms import RegisterForm, LoginForm, ResetRequestForm, PasswordResetForm
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User
#from app.utils import reset_email
import jwt

auth = Blueprint("auth", __name__)



"""
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth.route("/login", mehtods=['GET', "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data)
        login_user(user)
        
        return redirect(url_for('review.home'))

    return render_template('login.html', form=form)

@auth.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("auth.login"))

@auth.route("/reset-request", mehtods=['GET', "POST"])
def reset_request():
    form = ResetRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)

        reset_email(user)
        return redirect("reset_request")

    return render_template("reset-request.html", form=form)

@auth.route("reset-password/<str:token>", methods=["GET", "POST"])
def reset_password(token):
    form = PasswordResetForm()
    username = jwt.decode(token, app.secret_key)
    user = User.query.filter_by(username=username).first_or_404()

    form.user = user
    if form.validate_on_submit():
        user.set_password(form.password)
        db.sesion.commit()
        
        return redirect(url_for("auth.login"))

    return render_template("reset-password.html", form=form)
"""