from flask import current_app as app, Blueprint, url_for, render_template, redirect
from flask_login import current_user
from app import db
from .forms import AlbumReviewForm, ArtistReviewForm, SongReviewForm
from app.models import ArtistReview, AlbumReview, Genre, SongReview

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
        new_song_review = SongReview()
        form.populate_obj(new_song_review)
        db.session.add(new_song_review)
        db.session.commit()

        return redirect(url_for("review.songs"))

    return render_template("create-song-review.html", form=form)

@review.route("/album/new", methods=['GET', "POST"])
def create_album_review():
    form = AlbumReviewForm()

    if form.validate_on_submit():
        new_album_review = AlbumReview()
        form.populate_obj(new_album_review)
        db.session.add(new_album_review)
        db.session.commit()

        return redirect(url_for("review.albums"))

    return render_template('create-album-review.html', form=form)

@review.route('/artist/new', methods=["GET", "POST"])
def create_artist_review():
    form = ArtistReviewForm()

    if form.validate_on_submit():
        new_artist_review = ArtistReview()
        form.populate_obj(new_artist_review)
        db.session.add(new_artist_review)
        db.session.commit()

        return redirect(url_for("review.artists"))

    return render_template("create-artist-review.html", form=form)

@review.route('/songs/<str:name>/edit', methods=["GET", "POST"])
def edit_song_review(name):
    review = SongReview.query.filter_by(name=name).first_or_404()

    form = SongReviewForm(data=review)

    if form.validate_on_submit():
        form.populate_obj(review)
        db.session.commit()

        return redirect(url_for("review.songs", name=review))

    return render_template('edit-song-review.html', form=form)

@review.route('/albums/<str:name>/edit', methods=["GET", "POST"])
def edit_album_review(name):
    review = AlbumReview.query.filter_by(name=name).first_or_404()

    form = AlbumReviewForm(data=review)

    if form.validate_on_submit():
        form.populate_obj(review)
        db.session.commit()

        return redirect(url_for("review.albums", name=review))

    return render_template("edit-album-review.html", name=review)

@review.route("/artist/<str:name>/edit", methods=["GET", "POST"])
def edit_artist_review(name):
    review = ArtistReview.query.filter_by(name=name).first_or_404()

    form = ArtistReviewForm(data=review)

    if form.validate_on_submit():
        form.populate_obj(review)
        db.session.commit()

        return redirect(url_for("review.artists", name=review))

    return render_template("edit-artist-review.html", form=form)