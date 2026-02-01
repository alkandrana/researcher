from flask import Blueprint, render_template, request, redirect, url_for

from blueprints.productions.forms import PerformanceForm
from server import db
from models import Performance, Album

production_bp = Blueprint('production', __name__, url_prefix='/productions', template_folder='templates')

@production_bp.route('/<int:id>', methods=['GET'])
def get_performance(id):
    return render_template("productions/details.html")
@production_bp.route('/add/<int:album_id>', methods=['GET', 'POST'])
def add(album_id):
    form = PerformanceForm(request.form, album_id=album_id)
    if request.method == "POST" and form.validate_on_submit():
        new_production = Performance()
        form.populate_obj(new_production)
        db.session.add(new_production)
        db.session.commit()
        return redirect(url_for('album.get_album', id=album_id))
    return render_template('productions/form.html', form=form, action="add")

@production_bp.route('edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    production = Performance.query.get(id)
    form = PerformanceForm(obj=production)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(production)
        db.session.commit()
        print(f"{production.title} successfully updated.")
        return redirect(url_for('album.get_album', id=production.album_id))
    return render_template('productions/form.html', form=form, production_id=id, action="edit")

@production_bp.route('delete/<int:id>', methods=['POST'])
def delete(id):
    production = Performance.query.get(id)
    if production:
        db.session.delete(production)
        db.session.commit()
        print(f"{production.title} successfully deleted.")
        return redirect(url_for('album.get_album', id=production.album_id))
    return redirect(url_for('album.list_albums'))