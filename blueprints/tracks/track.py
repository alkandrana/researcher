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
        db.session.add(track)
        db.session.commit()
        print(f"{track.title} successfully created.")
        return redirect(url_for("album.get_album", id=track.performance.album_id))
    return render_template("tracks/form.html", form=form)

