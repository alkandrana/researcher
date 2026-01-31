from flask import Blueprint, render_template, request, redirect, url_for
from .forms import AlbumForm
from server import db
from models import Album

album = Blueprint('album', __name__, url_prefix='/albums', template_folder='templates')

@album.route("/")
def list_albums():
    albums = Album.query.all()
    print(albums)
    return render_template("records.html", albums=albums, title="Album List")

@album.route("/<int:id>")
def get_album(id):  # route and function parameter must match
    print(id)
    album = Album.query.get(id)
    return render_template("details.html", album=album)

@album.route("/add", methods=["GET", "POST"])
def add_album():
    record_form = AlbumForm()
    if request.method == 'POST' and record_form.validate_on_submit():
        # extract object properties
        uid = record_form.uid.data
        title = record_form.title.data
        medium = record_form.medium.data
        # create new album object
        new_record = Album(uid=uid, title=title, medium=medium)
        print(new_record)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('album.list_albums', message = 'Record successfully created.'))
    return render_template("add.html", form=record_form)

@album.route("/edit/<int:id>", methods=["GET", "POST"])
def update_album(album_id):
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('title')