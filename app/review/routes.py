from flask import current_app as app, Blueprint, url_for, render_template, redirect
from flask_login import current_user
from app import db
from .forms import AlbumReviewForm, ArtistReviewForm, SongReviewForm

review = Blueprint("review", __name__)

@review.route("/song/new", methods=['GET', "POST"])
def create_song_review():
    form = SongReviewForm()

    if form.validate_on_submit():
        pass

    return render_template("create-song-review.html", form=form)

@review.route("/album/new", methods=['GET', "POST"])
def create_album_review():
    form = AlbumReviewForm()

    if form.validate_on_submit():
        pass

    return render_template('create-album-review.html', form=form)

@review.route('/artist/new', methods=["GET", "POST"])
def create_artist_review():
    form = ArtistReviewForm()

    if form.validate_on_submit():
        pass

    return render_template("create-artist-review.html", form=form)