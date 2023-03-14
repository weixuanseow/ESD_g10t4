# Import Flask’s version of SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

# initialize a connection to the database and keep this in the db variable and use this to interact with the database.
class bookings(db.Model):
    __tablename__ = 'bookings'


    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    user = db.Column(db.String(255))

    def __init__(self, isbn13, title, price, availability):
        self.id = id
        self.slot = slot
        self.available = available

    def json(self):
        return {"id": self.id, "slot": self.slot, "available": self.available}


# Get all booking slots
@app.route("/bookings")
def get_all():
    booking_list = bookings.query.all()
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

# Update a booking slot to unavailable
@app.route('/bookings/<int:id>/unavailable', methods=['PUT'])
def mark_slot_unavailable(id):
    booking = bookings.query.get_or_404(id)
    booking.available = False
    db.session.commit()
    return jsonify({'message': 'Booking slot updated to unavailable'})

# Update a booking slot to available
@app.route('/mark_available/<int:booking_id>', methods=['PUT'])
def mark_available(booking_id):
    booking = bookings.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    booking.available = True
    booking.user = None
    db.session.commit()
    return jsonify({'message': 'Booking slot marked as available'})

# Query available booking slot from current time 
from datetime import datetime, timedelta
@app.route('/available_slots')
def get_available_slots():
    # get current time 
    now = datetime.utcnow()
    print(now)

    # query the database for available booking slots
    booking_list = bookings.query.filter(bookings.slot >= now,
                                            bookings.available == True).all()

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


# We run our application behind an if guard. 
if __name__ == '__main__':
    app.run(port=5000, debug=True)

# ----------------------------------------------------------------
# @app.route('/bookings/<int:id>', methods=['DELETE'])
# def delete_booking(id):
#     cursor = conn.cursor()
#     query = 'DELETE FROM bookings WHERE id = %s'
#     cursor.execute(query, (id,))
#     conn.commit()
#     cursor.close()
#     return jsonify({'message': 'Booking deleted successfully'})


# @app.route('/bookings/<int:', methods=['POST'])
# def add_booking(id, slot):
#     slot = request.json['slot']
#     # Format datetime object into string for SQL table
#     # Convert JSON date string to datetime object
#     json_date = datetime.datetime.strptime(slot, '%Y-%m-%dT%H:%M:%S.%fZ')
#     # Format datetime object into string for SQL table
#     slot = json_date.strftime('%Y-%m-%d %H:%M:%S')

#     available = request.json['available']
    
#     # Insert the booking slot into the bookings table
#     cursor = mydb.cursor()
#     sql = "INSERT INTO bookings (slot, user, available) VALUES (%s, %s, %s)"
#     values = (slot, user, available)
#     cursor.execute(sql, values)
#     mydb.commit()
#     return jsonify({'message': 'Booking slot added successfully'})

# if __name__ == '__main__':
#     app.run(debug=True)



