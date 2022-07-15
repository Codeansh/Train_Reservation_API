from enum import unique
from app import db,login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60),unique=True)
    email = db.Column(db.String(120),nullable=False,unique=True)
    password_hash = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    booking_slots = db.relationship('Booking', backref='', lazy='dynamic')

    def set_pwd_hash(self,password):
        self.password_hash = generate_password_hash(password)
    def check_pwd_hash(self,password):
        if check_password_hash(self.password_hash,password):
            return True
        return False


class Booking(db.Model):
    booking_slot = db.Column(db.Integer)
    date = db.Column(db.Date,primary_key=True)
    coach_id = db.Column(db.Integer,primary_key=True)
    seat_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Coaches(db.Model):
    coach_id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(60), nullable=False)
    no_of_seats = db.Column(db.Integer,nullable=False)

db.create_all()