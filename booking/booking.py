# Import Flask’s version of SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Query available booking slot from current time 
from datetime import datetime, timedelta

app = Flask(__name__)
# specify the database URL. Here we use the mysql+mysqlconnector prefix to tell SQLAlchemy which database engine and connector we are using. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/bookings'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/bookings'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  disable modification tracking
db = SQLAlchemy(app)
CORS(app)

import mysql.connector
# Configure MySQL connection
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'bookings',
    'port': 8889
}
# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'bookings',
#     'port': 3306
# }
conn = mysql.connector.connect(**mysql_config)

# --------------------------- object classes------------------------------------------------------------------------


class mri(db.Model):
    __tablename__ = 'mri'


    bid = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    pid = db.Column(db.String(255))

    def __init__(self, bid, slot, available, pid):
        self.bid = bid
        self.slot = slot
        self.available = available
        self.pid = pid


    def json(self):
        return {"bid": self.bid, "slot": self.slot, "available": self.available, 'pid':self.pid}

class xray(db.Model):
    __tablename__ = 'xray'


    bid = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    pid = db.Column(db.String(255))

    def __init__(self, bid, slot, available, pid):
        self.bid = bid
        self.slot = slot
        self.available = available
        self.pid = pid


    def json(self):
        return {"bid": self.bid, "slot": self.slot, "available": self.available, 'pid':self.pid}

class ctscan(db.Model):
    __tablename__ = 'ctscan'


    bid = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    pid = db.Column(db.String(255))

    def __init__(self, bid, slot, available, pid):
        self.bid = bid
        self.slot = slot
        self.available = available
        self.pid = pid


    def json(self):
        return {"bid": self.bid, "slot": self.slot, "available": self.available, 'pid':self.pid}

class bloodtest(db.Model):
    __tablename__ = 'bloodtest'


    bid = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    pid = db.Column(db.String(255))

    def __init__(self, bid, slot, available, pid):
        self.bid = bid
        self.slot = slot
        self.available = available
        self.pid = pid


    def json(self):
        return {"bid": self.bid, "slot": self.slot, "available": self.available, 'pid':self.pid}

# ----------------------------Functions ----------------------------------------------------------------------------

# Get all booking slots------------------------------------------------------------
@app.route("/mri/all", methods=['GET'])
def get_all_mri():

    booking_list = mri.query.all()
    if len(booking_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [booking.json() for booking in booking_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no booking slot."
        }
    ), 404

@app.route("/xray/all", methods=['GET'])
def get_all_xray():

    booking_list = xray.query.all()
    if len(booking_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [booking.json() for booking in booking_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no booking slot."
        }
    ), 404

@app.route("/bloodtest/all", methods=['GET'])
def get_all_bloodtest():

    booking_list = bloodtest.query.all()
    if len(booking_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [booking.json() for booking in booking_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no booking slot."
        }
    ), 404

@app.route("/ctscan/all", methods=['GET'])
def get_all_ctscan():

    booking_list = ctscan.query.all()
    if len(booking_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [booking.json() for booking in booking_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no booking slot."
        }
    ), 404
#------------------------------------------------------------------------------------------------------------------------
# Update a booking slot to unavailable 
@app.route('/mri/mark_unavailable/<int:bid>', methods=['PUT'])
def mark_slot_unavailable_mri(bid):
    booking = mri.query.get_or_404(bid)
    booking.available = False
    db.session.commit()
    return jsonify({
        'code': 200,
        'message': 'Booking slot updated to unavailable'
        })

@app.route('/xray/mark_unavailable/<int:bid>', methods=['PUT'])
def mark_slot_unavailable_xray(bid):
    booking = xray.query.get_or_404(bid)
    booking.available = False
    db.session.commit()
    return jsonify({
    'code': 200,
    'message': 'Booking slot updated to unavailable'
    })

@app.route('/bloodtest/mark_unavailable/<int:bid>', methods=['PUT'])
def mark_slot_unavailable_bloodtest(bid):
    booking = bloodtest.query.get_or_404(bid)
    booking.available = False
    db.session.commit()
    return jsonify({
    'code': 200,
    'message': 'Booking slot updated to unavailable'
    })

@app.route('/ctscan/mark_unavailable/<int:bid>', methods=['PUT'])
def mark_slot_unavailable_ctscan(bid):
    booking = ctscan.query.get_or_404(bid)
    booking.available = False
    db.session.commit()
    return jsonify({
    'code': 200,
    'message': 'Booking slot updated to unavailable'
    })
#------------------------------------------------------------------------------------------------------------------------
# Update a booking slot to available
@app.route('/mri/mark_available/<int:bid>', methods=['PUT'])
def mark_slot_available_mri(bid):
    booking = mri.query.get(bid)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    booking.available = True
    booking.user = None
    db.session.commit()
    return jsonify({
    'code': 200,
    'message': 'Booking slot updated to available'
    })

@app.route('/xray/mark_available/<int:bid>', methods=['PUT'])
def mark_slot_available_xray(bid):
    booking = xray.query.get(bid)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    booking.available = True
    booking.user = None
    db.session.commit()
    return jsonify({
    'code': 200,
    'message': 'Booking slot updated to unavailable'
    })

@app.route('/bloodtest/mark_available/<int:bid>', methods=['PUT'])
def mark_slot_available_bloodtest(bid):
    booking = bloodtest.query.get(bid)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    booking.available = True
    booking.user = None
    db.session.commit()
    return jsonify({
    'code': 200,
    'message': 'Booking slot updated to unavailable'
    })

@app.route('/ctscan/mark_available/<int:bid>', methods=['PUT'])
def mark_slot_available_ctscan(bid):
    booking = ctscan.query.get(bid)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    booking.available = True
    booking.user = None
    db.session.commit()
    return jsonify({
    'code': 200,
    'message': 'Booking slot updated to unavailable'
    })
#------------------------------------------------------------------------------------------------------------------------
# Query available booking slot from current time 
from datetime import datetime, timedelta
@app.route('/mri/available_slots', methods=['GET'])
def get_available_slots_mri():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = mri.query.filter(mri.slot >= now,
                                            mri.available == True).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no booking slot."
            }
        ), 404

@app.route('/xray/available_slots', methods=['GET'])
def get_available_slots_xray():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = xray.query.filter(xray.slot >= now,
                                            xray.available == True).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no booking slot."
            }
        ), 404

@app.route('/bloodtest/available_slots', methods=['GET'])
def get_available_slots_bloodtest():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = bloodtest.query.filter(bloodtest.slot >= now,
                                            bloodtest.available == True).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no booking slot."
            }
        ), 404

@app.route('/ctscan/available_slots', methods=['GET'])
def get_available_slots_ctscan():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = ctscan.query.filter(ctscan.slot >= now,
                                            ctscan.available == True).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no booking slot."
            }
        ), 404
#------------------------------------------------------------------------------------------------------------------------
# Query unavailable booking slot - booked 
from datetime import datetime, timedelta
@app.route('/mri/unavailable_slots', methods=['GET'])
def get_unavailable_slots_mri():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = mri.query.filter(mri.available == False).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no unavailable booking slot."
            }
        ), 404

@app.route('/xray/unavailable_slots', methods=['GET'])
def get_unavailable_slots_xray():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = xray.query.filter(xray.available == False).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no unavailable booking slot."
            }
        ), 404

@app.route('/bloodtest/unavailable_slots', methods=['GET'])
def get_unavailable_slots_bloodtest():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = bloodtest.query.filter(bloodtest.available == False).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no unavailable booking slot."
            }
        ), 404

@app.route('/ctscan/unavailable_slots', methods=['GET'])
def get_unavailable_slots_ctscan():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = ctscan.query.filter(ctscan.available == False).all()
    print(booking_list)
    if len(booking_list):
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                        "bookings": [booking.json() for booking in booking_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no unavailable booking slot."
            }
        ), 404
# ----------------------------------------------------------------
# # Delete the booking slot from the database
# @app.route('/bookings/<int:id>', methods=['DELETE'])
# def delete_booking(id):
#     cursor = conn.cursor()
#     query = 'DELETE FROM bookings WHERE id = %s'
#     cursor.execute(query, (id,))
#     conn.commit()
#     cursor.close()
#     return jsonify({'message': 'Booking deleted successfully'})

# # Add booking slot back into the database
# @app.route('/bookings/<int:id>', methods=['POST'])
# def add_booking(id, slot):
#     slot = request.json['slot']
#     # Format datetime object into string for SQL table
#     # Convert JSON date string to datetime object
#     json_date = datetime.datetime.strptime(slot, '%Y-%m-%dT%H:%M:%S.%fZ')
#     # Format datetime object into string for SQL table
#     slot = json_date.strftime('%Y-%m-%d %H:%M:%S')

#     available = request.json['available']
    
    # # Insert the booking slot into the bookings table
    # cursor = mydb.cursor()
    # sql = "INSERT INTO bookings (slot, user, available) VALUES (%s, %s, %s)"
    # values = (slot, user, available)
    # cursor.execute(sql, values)
    # mydb.commit()
    # return jsonify({'message': 'Booking slot added successfully'})













# We run our application behind an if guard. 
if __name__ == '__main__':
    app.run(port=5000, debug=True)