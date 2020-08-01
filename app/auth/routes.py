from flask import current_app, render_template, redirect, Blueprint, url_for
from app import db, login_manager
from .forms import RegisterForm, LoginForm, ResetRequestForm, PasswordResetForm
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        pass

    return render_template("register.html", form=form)


@auth.route("/login", mehtods=['GET', "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass

    return render_template('login.html', form=form)

@auth.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("auth.login"))

@auth.route("/reset-request", mehtods=['GET', "POST"])
def reset_request():
    form = ResetRequestForm()

    if form.validate_on_submit():
        pass

    return render_template("reset-request.html", form=form)

@auth.route("reset-password", methods=["GET", "POST"])
def reset_password():
    form = PasswordResetForm()

    if form.validate_on_submit():
        pass

    return render_template("reset-password.html", form=form)
