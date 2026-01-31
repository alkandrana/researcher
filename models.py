import enum
from sqlalchemy import Enum, UniqueConstraint, Index
from server import db

class Role(enum.Enum):
    character = "character"
    singer = "singer"
    conductor = "conductor"
    ensemble = "ensemble"
    instrument = "instrument"
    chorus = "chorus"
    soloist = "soloist"
    narrator = "narrator"
    other = "other"

class WorkType(enum.Enum):
    opera = "opera"
    symphony = "symphony"
    concerto = "concerto"
    chamber = "chamber"
    recital = "recital"
    sacred = "sacred"
    other = "other"

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    medium = db.Column(db.String(20), nullable=False)
    performances = db.relationship('Performance', backref='album')
    def __repr__(self):
        return f"Album: {self.title}"

class Performance(db.Model):
    __tablename__ = "performances"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    composer = db.Column(db.String, nullable=False, default="Anonymous")
    type = db.Column(Enum(WorkType, native_enum=False, validate_strings=True), nullable=False)
    highlights = db.Column(db.Boolean, nullable=False, default=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    tracks = db.relationship('Track', backref='performance', cascade="all, delete-orphan")
    credits = db.relationship('Credit', back_populates='performance', cascade="all, delete-orphan")
    def __repr__(self):
        return f"Work: {self.title} by {self.composer}"


    
class Credit(db.Model):
    __tablename__ = "credits"
    __table_args__ = (
        UniqueConstraint(
            'performance_id', 'actor_id', 'role', 'detail',
        name="uq_credit_performance_actor_role_detail"
        ),
        Index("ix_credit_perf_role", "performance_id", "role"),
    )

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    performance_id = db.Column(db.Integer, db.ForeignKey('performances.id'), nullable=False)
    role = db.Column(Enum(Role, native_enum=False, validate_strings=True), nullable=False)
    # "Figaro", "Rosina", "piano", "violin", etc.
    detail = db.Column(db.String(255), nullable=True)
    voice = db.Column(db.String(50), nullable=True) # optional
    instrument = db.Column(db.String(100), nullable=True) # optional
    performance = db.relationship("Performance", back_populates="credits")
    actor = db.relationship("Actor", back_populates="credits")
    def __repr__(self):
        return f"Contributor: {self.name} as {self.role}"

class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    voice = db.Column(db.String, nullable=False, default="tenor")
    credits = db.relationship('Credit', back_populates='actor', cascade="all, delete-orphan")
    def __repr__(self):
        return f"{self.name} ({self.voice})"

class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    performances = db.relationship('Performance', backref='location')
class Track(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    performance_id = db.Column(db.Integer, db.ForeignKey('performances.id'), nullable=False)
    def __repr__(self):
        return f"Track {self.sequence}: {self.title}"