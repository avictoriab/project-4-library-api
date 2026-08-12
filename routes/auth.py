from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from werkzeug.security import generate_password_hash

from database import Session
from models import User
from schemas import UserSchema

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    session = Session()
    data = request.get_json()

    try:
        user_data = UserSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    existing_user = session.query(User).filter_by(
    username=user_data.username
    ).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    user = User(
    username=user_data.username,
    password=generate_password_hash(user_data.password)
    )

    session.add(user)
    session.commit()
    session.close()

    return jsonify({"message": "User registered successfully"}), 201