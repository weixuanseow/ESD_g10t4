# Import Flask’s version of SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Query available booking slot from current time 
from datetime import datetime, timedelta

app = Flask(__name__)
# specify the database URL. Here we use the mysql+mysqlconnector prefix to tell SQLAlchemy which database engine and connector we are using. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/bookings'
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
conn = mysql.connector.connect(**mysql_config)

# --------------------------- object classes------------------------------------------------------------------------
class VisitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Consultation(db.Model):
    __tablename__ = 'consultation'


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

class Xray(db.Model):
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

class Orthopaedics(db.Model):
    __tablename__ = 'orthopaedics'


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

class Physiotherapy(db.Model):
    __tablename__ = 'physiotherapy'


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



@app.route("/visit_type", methods=['GET'])
def get_all(visit_type):
    visit_types = VisitType.query.all()
    if len(booking_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [booking.json() for booking in visit_types]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no booking slot."
        }
    ), 404

# Update a booking slot to unavailable 
@app.route('/<visit_type>/mark_unavailable/<int:bid>', methods=['PUT'])
def mark_slot_unavailable(visit_type,bid):
    booking = visit_type.query.get_or_404(bid)
    booking.available = False
    db.session.commit()
    return jsonify({'message': 'Booking slot updated to unavailable'})

# Update a booking slot to available
@app.route('/<visit_type>/mark_available/<int:bid>', methods=['PUT'])
def mark_available(visit_type,bid):
    booking = visit_type.query.get_or_404(bid)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    booking.available = True
    booking.user = None
    db.session.commit()
    return jsonify({'message': 'Booking slot marked as available'})

# Query available booking slot from current time 
from datetime import datetime, timedelta
@app.route('/<visit_type>/available_slots', methods=['GET'])
def get_available_slots(visit_type):
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = visit_type.query.filter(visit_type.slot >= now,
                                            visit_type.available == True).all()
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

# Query unavailable booking slot - booked 
from datetime import datetime, timedelta
@app.route('/<visit_type>/unavailable_slots', methods=['GET'])
def get_unavailable_slots(visit_type):
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = visit_type.query.filter(visit_type.available == False).all()
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

# ----------------------------------------------------------------
# Delete the booking slot from the database
@app.route('/<visit_type>/delete/<int:bid>', methods=['DELETE'])
def delete_booking(visit_type,bid):
    cursor = conn.cursor()
    query = 'DELETE FROM ' + visit_type +' WHERE id = %s'
    cursor.execute(query, (bid,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Booking deleted successfully'})

# Add booking slot back into the database
@app.route('/<visit_type>/add/<int:bid>', methods=['POST'])
def add_booking(bid, slot):
    slot = request.json['slot']
    # Format datetime object into string for SQL table
    # Convert JSON date string to datetime object
    json_date = datetime.datetime.strptime(slot, '%Y-%m-%dT%H:%M:%S.%fZ')
    # Format datetime object into string for SQL table
    slot = json_date.strftime('%Y-%m-%d %H:%M:%S')

    available = request.json['available']
    
    # Insert the booking slot into the bookings table
    cursor = mydb.cursor()
    sql = "INSERT INTO bookings (slot, user, available) VALUES (%s, %s, %s)"
    values = (slot, user, available)
    cursor.execute(sql, values)
    mydb.commit()
    return jsonify({'message': 'Booking slot added successfully'})













# We run our application behind an if guard. 
if __name__ == '__main__':
    app.run(port=5000, debug=True)
