from models.conn import db

class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    rooms = db.relationship('Room', backref='room_type', lazy=True)

    def __repr__(self):
        return f'<Room type {self.name}>'