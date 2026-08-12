from flask import Flask, jsonify, request
from database import Session
from models import Book, User
from schemas import BookSchema, UserSchema, ValidationError
from werkzeug.security import generate_password_hash

from routes.auth import auth
from routes.books import books

app = Flask(__name__)

app.register_blueprint(auth)

app.register_blueprint(books)

@app.route("/")
def home():
    return jsonify({
        "name": "Library API",
        "version": "1.0",
        "status": "running"
    })


if __name__ == "__main__":
    app.run(debug=True)