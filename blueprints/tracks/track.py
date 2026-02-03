from os import abort

from flask import Blueprint, request, redirect, url_for, render_template

from blueprints.tracks.forms import TrackForm
from server import db
from models import Track

track_bp = Blueprint('track', __name__, url_prefix='/tracks', template_folder='templates')

@track_bp.route('/add/<int:performance_id>', methods=['GET', 'POST'])
def add(performance_id):
    form = TrackForm(request.form, performance_id=performance_id)
    if request.method == 'POST' and form.validate():
        track = Track()
        form.populate_obj(track)
        try:
            db.session.add(track)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            abort()
        else:
            print(f"{track.title} successfully created.")
            return redirect(url_for("album.get_album", id=track.performance.album_id))
    return render_template(
        "tracks/form.html",
                           form=form,
                           action_url=url_for("track.add", performance_id=performance_id)
    )

@track_bp.route('/edit/<int:track_id>', methods=['GET', 'POST'])
def edit(track_id):
    track = Track.query.get(track_id)
    form = TrackForm(obj=track)
    if request.method == 'POST' and form.validate():
        form.populate_obj(track)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            abort()
        else:
            print(f"{track.title} successfully updated.")
            return redirect(url_for("album.get_album", id=track.performance.album_id))
    return render_template(
        "tracks/form.html",
        form=form,
        action_url=url_for("track.edit", track_id=track_id)
    )

@track_bp.route('/delete/<int:track_id>', methods=['POST'])
def delete(track_id):
    track = Track.query.get(track_id)
    if track:
        album_id = track.performance.album_id
        try:
            db.session.delete(track)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            abort()
        else:
            print(f"{track.title} successfully deleted.")
            return redirect(url_for("album.get_album", id=album_id))
    return redirect(url_for("album.list_albums"))
