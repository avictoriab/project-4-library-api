from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from config import JWT_SECRET_KEY
from database import Session
from models import User
from schemas import UserSchema


auth = Blueprint("auth", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization")

        if not authorization:
            return jsonify({"error": "Token is missing"}), 401

        parts = authorization.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Invalid Authorization header"}), 401

        token = parts[1]

        try:
            data = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401    

        user_id = data.get("user_id")

        if user_id is None:
            return jsonify({"error": "Invalid token payload"}), 401
        
        session = Session()

        try:
            user = session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

        if user is None:
            return jsonify({"error": "User not found"}), 401
        
        return f(user, *args, **kwargs)

    return decorated


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    try:
        user_data = UserSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session = Session()

    try:
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

        return jsonify({"message": "User registered successfully"}), 201

    finally:
        session.close()


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    try:
        user_data = UserSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    session = Session()

    try:
        user = session.query(User).filter_by(
            username=user_data.username
        ).first()

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

        return jsonify({"token": token}), 200
    
    finally:
        session.close()

