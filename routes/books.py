from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from routes.auth import token_required
from database import Session
from models import Book
from schemas import BookSchema


books = Blueprint("books", __name__)


def book_to_dict(book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "user_id": book.user_id
    }


@books.route("/books")
def get_books():
    session = Session()

    try:
        books = session.query(Book).all()

        if not books:
            return jsonify({"message": "There are no books"}), 200

        response = {
            "books": [book_to_dict(book) for book in books]
        }
    finally:
        session.close()

    return jsonify(response), 200



@books.route("/books", methods=["POST"])
@token_required
def create_book(user):
    data = request.get_json()

    try: 
        book_data = BookSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400 

    session = Session()

    try:
        book = Book(
            title = book_data.title,
            author = book_data.author,
            user_id = user.id
        )

        session.add(book)
        session.commit()

        response = book_to_dict(book)
    finally:
        session.close()

    return jsonify(response), 201


@books.route("/books/<int:book_id>")
def get_book(book_id):
    
    session = Session()

    try:
        book = session.query(Book).filter_by(id=book_id).first()

        if book is None:
            return jsonify({"error": "Book not found"}), 404

        response = book_to_dict(book)
    finally:
        session.close()

    return jsonify(response), 200


@books.route("/books/<int:book_id>", methods=["PUT"])
@token_required
def update_book(user, book_id):
    data = request.get_json()
    
    try: 
        book_data = BookSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400 
    
    session = Session()

    try:
        book = session.query(Book).filter_by(id=book_id).first()

        if book is None:
            return jsonify({"error": "Book not found"}), 404

        if book.user_id != user.id:
            return jsonify({"error": "You do not have permission to modify this book"}), 403

        book.title = book_data.title
        book.author = book_data.author

        session.commit()

        response = book_to_dict(book)
    finally:
        session.close()

    return jsonify(response), 200


@books.route("/books/<int:book_id>", methods=["DELETE"])
@token_required
def delete_book(user, book_id):
    session = Session()

    try: 
        book = session.query(Book).filter_by(id=book_id).first()

        if book is None:
            return jsonify({"error": "Book not found"}), 404

        if book.user_id != user.id:
            return jsonify({"error": "You do not have permission to delete this book"}), 403

        session.delete(book)

        session.commit()
    finally:
        session.close()

    return jsonify({"message": "Book deleted"}), 200


@books.route("/my-books", methods=["GET"])
@token_required
def get_my_books(user):
    session = Session()

    try:
        books = session.query(Book).filter_by(user_id=user.id).all()

        if not books:
            return jsonify({"message": "You have no books"}), 200

        response = {
            "books": [book_to_dict(book) for book in books]
        }
    finally:
        session.close()

    return jsonify(response), 200
