import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from forms import

app = Flask(__name__)
app.config['SECRET_KEY'] = '2e89284079e0a7bf53361aabf6ecd467cb0f322f300da85b337485f2ceb68bed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
from models import Record, Interpreter

with app.app_context():
    if not os.path.exists('site.db'):
        db.create_all()

operas = [
    {
        'composer': 'Gioacchino Rossini',
        'title': 'Il barbiere di Siviglia',
        'orchestra': 'Metropolitan Opera Orchestra and Chorus',
        'conductor': 'Erich Leinsdorf'
    },
    {
        'composer': 'Gioacchino Rossini',
        'title': 'La Cenerentola',
        'orchestra': 'The Orchestra of the Royal Opera House',
        'conductor': 'Carlo Rizzi'
    }
]
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/books")
def about():
    return render_template('books.html', operas=operas, title='List of Recordings')
