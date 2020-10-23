"""
from flask import current_app as app, Blueprint, url_for, redirect, render_template
from flask_login import current_user
#from .forms import ProfileForm, PasswordChangeForm
from app.models import User
from app import db

user = Blueprint("user", __name__)
"""

"""
@user.route("/profile/<str:username>")
def profile(username):
    page = User.query.filter_by(username=username).first_or_404()

    return render_template("profile.html")

@user.route("/profile", methods=["GET", "POST"])
def edit_profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()

        return redirect(url_for("user.profile"))

    return render_template("edit-profile.html", form=form)

@user.route("/password", methods=["GET", "POST"])
def password():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()

        return redirect(url_for("user.profile"))

    return render_template("password.html", form=form)

"""