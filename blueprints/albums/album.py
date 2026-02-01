from flask import Blueprint, render_template, request, redirect, url_for
from blueprints.albums.forms import AlbumForm
from server import db
from models import Album

album_bp = Blueprint('album', __name__, url_prefix='/albums', template_folder='templates')

@album_bp.route("/")
def list_albums():
    message = request.args.get('message')
    record_form = AlbumForm()
    albums = Album.query.all()
    return render_template("list.html", albums=albums, title="Album List", form=record_form, message=message)

@album_bp.route("/<int:id>")
def get_album(id):  # route and function parameter must match
    print(id)
    album = Album.query.get(id)
    return render_template("details.html", album=album)

@album_bp.route("/add", methods=["POST"])
def add_album():
    record_form = AlbumForm(request.form)
    if record_form.validate_on_submit():
        new_album = Album()
        record_form.populate_obj(new_album)
        # create new album object
        print(new_album)
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('album.list_albums',
                                message = 'Record successfully created.'))
    return render_template("form.html", form=record_form)

@album_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def update_album(id):
    album = Album.query.get(id)
    form = AlbumForm(obj=album)
    print(form.uid.data)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(album)
        db.session.commit()
        print(f"{album.title} successfully updated.")
        return redirect(url_for('album.list_albums',
                                message = 'Record successfully updated.'))
    return render_template("form.html", form=form, album=album, action="edit")

@album_bp.route("/delete/<int:id>", methods=["POST"])
def delete_album(id):
    album = Album.query.get(id)
    message = ""
    if album:
        db.session.delete(album)
        db.session.commit()
        message = f"{album.title} successfully deleted."
    return redirect(url_for('album.list_albums', message = message))