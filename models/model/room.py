from models.conn import db

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    n_people_space = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<Room:{self.name}, Number of people fitting:{self.n_people_space}>'