from flask import current_app as app, Blueprint, url_for, render_template, redirect
from flask_login import current_user
from app import db
from .forms import AlbumReviewForm, ArtistReviewForm, SongReviewForm
from app.models import Artist, Album, Genre, Song

review = Blueprint("review", __name__)

@review.route("/songs")
def songs():
    query = Song.query.all()

    return render_template("song-reviews.html", query=query)

@review.route("/albums")
def albums():
    query = Album.query.all()

    return render_template('album-reviews.html', query=query)

@review.route("/artists")
def artists():
    query = Artist.query.all()

    return render_template("artist-reviews.html", query=query)


@review.route("/song/new", methods=['GET', "POST"])
def create_song_review():
    form = SongReviewForm()

    if form.validate_on_submit():
        new_song_review = Song()
        form.populate_obj(new_song_review)
        db.session.add(new_song_review)
        db.session.commit()

        return redirect(url_for("review.songs"))

    return render_template("create-song-review.html", form=form)

@review.route("/album/new", methods=['GET', "POST"])
def create_album_review():
    form = AlbumReviewForm()

    if form.validate_on_submit():
        new_album_review = Album()
        form.populate_obj(new_album_review)
        db.session.add(new_album_review)
        db.session.commit()

        return redirect(url_for("review.albums"))

    return render_template('create-album-review.html', form=form)

@review.route('/artist/new', methods=["GET", "POST"])
def create_artist_review():
    form = ArtistReviewForm()

    if form.validate_on_submit():
        new_artist_review = Artist
        form.populate_obj(new_artist_review)
        db.session.add(new_artist_review)
        db.session.commit()

        return redirect(url_for("review.artists"))

    return render_template("create-artist-review.html", form=form)