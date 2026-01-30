from server import db
class Record(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    composer = db.Column(db.String, nullable=False)
    orchestra = db.Column(db.String, nullable=False)
    conductor = db.Column(db.String, nullable=False)
    interpreters = db.relationship('Interpreter', backref='performance')
    def __repr__(self):
        return f"Record: {self.title} by {self.composer}"
class Interpreter(db.Model):
    name = db.Column(db.String, primary_key=True)
    role = db.Column(db.String, nullable=False)
    record_id = db.Column(db.String, db.ForeignKey('record.id'), nullable=False)
    def __repr__(self):
        return f"Interpreter: {self.name} as {self.role}"