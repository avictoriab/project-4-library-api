from flask import Flask, jsonify, request
from database import Session
from models import Book

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "name": "Library API",
        "version": "1.0",
        "status": "running"
    })

@app.route("/books")
def get_books():
    session = Session()

    books = session.query(Book).all()

    session.close()

    return jsonify({
        "books": [
            {
            "id": book.id,
            "title": book.title,
            "author": book.author
            }
            for book in books
        ]
    })

@app.route("/books", methods=["POST"])
def create_book():
    session = Session()
    data = request.get_json()
    
    book = Book(
        title = data['title'],
        author = data['author']
    )

    session.add(book)
    session.commit()

    response = {
        "id": book.id,
        "title": book.title,
        "author": book.author
    }
    session.close()

    return jsonify(response)

@app.route("/books/<int:book_id>")
def get_book(book_id):
    session = Session()

    book = session.query(Book).filter_by(id=book_id).first()

    if book is None:
        session.close()
        return jsonify({"error": "Book not found"}), 404

    response = {
        "id": book.id,
        "title": book.title,
        "author": book.author
    }

    session.close()

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)