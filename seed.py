from app import create_app
from models.conn import db
from models.model.User import User
from models.model.room import Room

app = create_app()

with app.app_context():
    print("Starting database seeding...")

    rooms_data = [
        {"name": "Meeting Room A", "n_people_space": 10},
        {"name": "Conference Room B", "n_people_space": 25},
        {"name": "Interview Office C", "n_people_space": 4},
    ]
    
    for r_data in rooms_data:
        existing_room = Room.query.filter_by(name=r_data["name"]).first()
        if not existing_room:
            room = Room(
                name=r_data["name"],
                n_people_space=r_data["n_people_space"]
            )
            db.session.add(room)
    
    users_data = [
        {"username": "admin_test", "email": "admin@example.com"},
        {"username": "mario_rossi", "email": "mario@example.com"},
        {"username": "luigi_verdi", "email": "luigi@example.com"},
    ]
    
    for u_data in users_data:
        existing_user = User.query.filter_by(email=u_data["email"]).first()
        if not existing_user:
            user = User(
                username=u_data["username"],
                email=u_data["email"]
            )
            user.set_password("test2026")
            db.session.add(user)
    
    db.session.commit()
    print("Database seeded successfully!")