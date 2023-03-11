from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# class Patient(db.Model):
#     __tablename__ = 'patient'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     diagnosis = db.Column(db.String(200))
#     prescription = db.Column(db.String(200))
    
#     def __init__(self, name, age, diagnosis, prescription):
#         self.name = name
#         self.age = age
#         self.diagnosis = diagnosis
#         self.prescription = prescription
        
        
        
    
#     isbn13 = db.Column(db.String(13), primary_key=True)
#     title = db.Column(db.String(64), nullable=False)
#     price = db.Column(db.Float(precision=2), nullable=False)
#     availability = db.Column(db.Integer)

#     def __init__(self, isbn13, title, price, availability):
#         self.isbn13 = isbn13
#         self.title = title
#         self.price = price
#         self.availability = availability

#     def json(self):
#         return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}

# @app.route("/book")
# def get_all():
#     booklist = Book.query.all()
#     if len(booklist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "books": [book.json() for book in booklist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no books."
#         }
#     ), 404


# @app.route("/book/<string:isbn13>")
# def find_by_isbn13(isbn13):
#     book = Book.query.filter_by(isbn13=isbn13).first()
#     if book:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": book.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Book not found."
#         }
#     ), 404


# @app.route("/book/<string:isbn13>", methods=['POST'])
# def create_book(isbn13):
#     if (Book.query.filter_by(isbn13=isbn13).first()):
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "Book already exists."
#             }
#         ), 400

#     data = request.get_json()
#     book = Book(isbn13, **data)

#     try:
#         db.session.add(book)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "An error occurred creating the book."
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": book.json()
#         }
#     ), 201




# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
