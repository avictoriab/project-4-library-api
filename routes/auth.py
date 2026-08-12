from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from config import JWT_SECRET_KEY

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY

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

@auth.route("/login", methods=["POST"])
def login():
    session = Session()
    data = request.get_json()

    try:
        user_data = UserSchema(**data)
    except ValidationError as e:
            return jsonify({"error": e.errors()}), 400

    user = session.query(User).filter_by(username=user_data.username).first()

    if user is None:
         return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.password, user_data.password):
         return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
    {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    },
    JWT_SECRET_KEY,
    algorithm="HS256"
    )

    session.close()

    return jsonify({"token": token})