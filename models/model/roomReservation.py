from models.conn import db

reservation_participants = db.Table('reservation_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('reservation_id', db.Integer, db.ForeignKey('room_reservation.id'), primary_key=True)
)

class RoomReservation(db.Model):
    __tablename__ = 'room_reservation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    detail = db.Column(db.Text, nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    admin = db.relationship('User', foreign_keys=[admin_id], backref=db.backref('admin_reservations', lazy=True))    
    room = db.relationship('Room', backref=db.backref('reservations', lazy=True))

    participants = db.relationship(
        'User', 
        secondary=reservation_participants, 
        backref=db.backref('participating_reservations', lazy=True)
    )

    def __repr__(self):
        return f'<Room Reservation:{self.name} in the {self.room}, Person Presenting:{self.user}>'