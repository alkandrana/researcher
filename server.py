import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RecordForm

# from forms import

app = Flask(__name__)
app.secret_key = '2e89284079e0a7bf53361aabf6ecd467cb0f322f300da85b337485f2ceb68bed'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
from models import Record, Interpreter

with app.app_context():
    if not os.path.exists('site.db'):
        db.create_all()

# operas = {
#     'RCA-2505-2 RG': {
#         'composer': 'Gioacchino Rossini',
#         'title': 'Il barbiere di Siviglia',
#         'orchestra': 'Metropolitan Opera Orchestra and Chorus',
#         'conductor': 'Erich Leinsdorf'
#     },
#     'TELDEC-4509-94553-2': {
#         'composer': 'Gioacchino Rossini',
#         'title': 'La Cenerentola',
#         'orchestra': 'The Orchestra of the Royal Opera House',
#         'conductor': 'Carlo Rizzi'
#     }
# }
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/records")
def list_records():
    print("Listing Records")
    records = Record.query.all()
    print(records)
    return render_template(
        'records.html',
        operas=records,
        title='List of Recordings')

@app.route("/record/<string:record_id>")
def display_record(record_id):
    record = Record.query.get(record_id)
    return f"<h1> { record['title'] } </h1> <p>Composer: {record['composer'] } </p>"

@app.route("/add", methods=['GET', 'POST'])
def add_record():
    record_form = RecordForm()
    if request.method == 'POST' and record_form.validate_on_submit():
        # extract object properties
        id = record_form.id.data
        title = record_form.title.data
        composer = record_form.composer.data
        orchestra = record_form.orchestra.data
        conductor = record_form.conductor.data
        new_record = Record(id=id, title=title, composer=composer, orchestra=orchestra, conductor=conductor)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('list_records', message = 'Record successfully created.'))
    return render_template("add.html", form=record_form)