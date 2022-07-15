import re

from flask import jsonify, request
from app import app, db
import json
from flask_login import current_user, login_user, logout_user,login_required 
from models import User, Booking, Coaches
from datetime import date

@app.route('/')
def index():
    return jsonify({"success": True})


@app.route('/home')
def home():
    return jsonify({ "log_in as " : "admin or user"})


@app.route('/register', methods=['POST'])

def register():
    body = json.loads(request.data)
    try:
        user = User.query.filter_by(username=body.get('username')).first()
    except:
        user = None
    if user:
        return jsonify({"username":"taken"})
    try:
        email = User.query.filter_by(email=body.get('email')).first()
    except:
        email = None
    if email:
        return jsonify({"email":"taken"})


    user = User(username=body.get('username'),email = body.get('email'))


    user.set_pwd_hash(body.get('password'))
    db.session.add(user)
    db.session.commit()
    return body

@app.route('/login', methods=['POST'])
def login():
    body = json.loads(request.data)

    user = User.query.filter_by(username=body.get('username')).first()
    if user:
        correct = user.check_pwd_hash(body.get('password'))
        if correct :
            login_user(user)
            return jsonify({"login" : "successfull"})
    return jsonify({"login":"failed"})


@app.route('/booking',methods=['POST'])
@login_required
def bookP():
    body = json.loads(request.data)
    date_= body.get('date').split(":")
    coach_id = body.get('coach_id')
    seat_id = body.get('seat_id')
    dateO = date(int(date_[2]),int(date_[1]),int(date_[0]))

    
    book_check = Booking.query.filter_by(date=dateO,seat_id=seat_id,coach_id=coach_id).first()

    if book_check:
        print(book_check.seat_id,book_check.coach_id)
        # if book_check.seat_id == seat_id and book_check.coach_id == coach_id :
        #     #print(book_check.seat_id,book_check.coach_id)
        return jsonify({"already" : "booked"})  
    else:
    
        coach = Coaches.query.filter_by(coach_id=coach_id).first()
        if not coach :
            return jsonify({"coach":"not found"})
        seats = coach.no_of_seats
        print(seats)
        if seat_id > seats:
            return jsonify({"seat":"not_found"})

        booking = Booking(booking_slot=current_user.id,date=dateO,coach_id=coach_id,seat_id=seat_id,user_id=current_user.id)
        db.session.add(booking)
        db.session.commit()
        return jsonify({"booking" : "successful"})

@app.route('/edit_coach',methods=['POST']) #for adding coach {operation:"create,"type:"...",no_of_seats:int}
                                            #for updating  {coach_id:int,type:"...",no_of_seats:int}

@login_required
def coach():
    if not current_user.is_admin:
        return jsonify({"access":"denied"})
    body = json.loads(request.data)
    op = body.get('operation')
    if op == "create" :
        new_coach = Coaches(type=body.get('type'),no_of_seats=body.get('seats'))
        db.session.add(new_coach)
        db.session.commit()

        return jsonify({"coach":"created"})
    if op == "read":
        output={}
        coach = Coaches.query.all()
        for c in coach:
            id=c.coach_id
            type=c.type
            seats=c.no_of_seats
            output[f"coach id : {id} , Type : {type}"]=f"Total seats : {seats}"
        return output


        if coach :
            return {"coach_id":coach.coach_id, "type":coach.type,"No. of Seats":coach.no_of_seats}
        return {"coach ":"not found"}
    if op == "update" :
        coach = Coaches.query.filter_by(coach_id=body.get('coach_id')).first()
        print(body)
        if "type" in body.keys():
            coach.type = body.get('type')

        if "seats" in body.keys():
            coach.no_of_seats = body.get('seats')

        db.session.commit()

        return jsonify({"coach":"updated"})


    if op =="delete":
        coach = Coaches.query.filter_by(coach_id=body.get('coach_id')).first()
        db.session.delete(coach)
        #or Coaches.query.filter_by(coach_id=body.get('coach_id')).delete()
        db.session.commit()

        return jsonify({"coach":"deleted"})
    
    return jsonify({"booking" : "successful"})


@app.route('/booking/<dateI>',methods=['GET'])
@login_required
def getstatus(dateI):
    date_=dateI.split(':')
    dateO = date(int(date_[2]),int(date_[1]),int(date_[0]))
    #booking = Booking.query.filter_by(user_id=1).all()
   # print(dateO,booking)
    output={}
    coach=Coaches.query.all()
    for c in coach:
        id=c.coach_id
        type=c.type
        seats=c.no_of_seats
        booking=Booking.query.filter_by(coach_id=id,date=dateO).all()
        booked=[]
        for j in booking:
            booked.append(j.seat_id)

        output[f"coach id : {id} , Type : {type}"]=f"Total seats : {seats} , booked : {booked}"
    return output
@app.route('/logout',methods = ['POST'])
def logout():
    logout_user()
    return jsonify({'logout':'success'})

@app.before_request
def before_request():
    booking  = Booking.query.all()
    for book in booking :
        if book.date = "0"
            #delete

    

