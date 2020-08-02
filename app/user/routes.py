from flask import current_app as app, Blueprint, url_for, redirect, render_template
from flask_login import current_user
from .forms import ProfileForm

user = Blueprint("user", __name__)

@user.route("/profile", methods=["GET", "POST"])
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        pass

    return render_template("profile.html", form=form)

