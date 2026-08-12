from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from routes.auth import token_required

from database import Session
from models import Book
from schemas import BookSchema

books = Blueprint("books", __name__)

@books.route("/books")
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

@books.route("/books", methods=["POST"])
@token_required
def create_book(user):
    session = Session()
    data = request.get_json()

    try: 
        book_data = BookSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400 
    
    book = Book(
        title = book_data.title,
        author = book_data.author
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

@books.route("/books/<int:book_id>")
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

@books.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    session = Session()

    book = session.query(Book).filter_by(id=book_id).first()

    if book is None:
        session.close()
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    try: 
        book_data = BookSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400 

    book.title = book_data.title
    book.author = book_data.author

    session.commit()

    response = {
        "id": book.id,
        "title": book.title,
        "author": book.author
    }

    session.close()

    return jsonify(response)

@books.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    session = Session()
    
    book = session.query(Book).filter_by(id=book_id).first()

    if book is None:
        session.close()
        return jsonify({"error": "Book not found"}), 404

    session.delete(book)

    session.commit()

    session.close()

    return jsonify("message:" "Book deleted")

