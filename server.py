import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# Order is very finicky in this section
app = Flask(__name__)
app.secret_key = '2e89284079e0a7bf53361aabf6ecd467cb0f322f300da85b337485f2ceb68bed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
from blueprints.albums.album import album_bp
app.register_blueprint(album_bp)




# with app.app_context():
  #   if not os.path.exists('site.db'):
    #     db.create_all()

@app.route("/")
def index():
    return render_template('index.html')