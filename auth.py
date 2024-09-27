import secrets
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from db import get_db_connection
import jwt
import datetime
import os

# Create a Blueprint for authentication
auth_bp = Blueprint("auth", __name__)

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "1237ac0393917173029ad602d3152bd523ce383e9a89790b098fbf4c6a461ad8"
)
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")

# Route for user login (Authentication operation)
@auth_bp.route("/login", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "example": "john.doe@example.com"},
                        "password": {"type": "string", "example": "yourpassword"},
                    },
                    "required": ["email", "password"],
                },
            }
        ],
        "responses": {
            200: {
                "description": "User logged in successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "token": {"type": "string"},
                        "user": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "email": {"type": "string"},
                                "avatar": {"type": "string"},
                            },
                        },
                    },
                },
            },
            401: {"description": "Invalid email or password"},
        },
    }
)
def login():
    credentials = request.get_json()
    email = credentials.get("email")
    password = credentials.get("password")

    print(email, password)

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    print(user)
    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    stored_password_hash = user["password"]  # Adjust field name if different

    if not check_password_hash(stored_password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    # Convert the user Row object to a dictionary
    user_dict = dict(user)

    # Remove the password field from the user data
    user_dict.pop("password", None)

    return (
        jsonify(
            {
                "message": "User logged in successfully",
                "token": token,
                "user": user_dict,
            }
        ),
        200,
    )


# Route for user signup (Registration operation)
@auth_bp.route("/signup", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "example": "John"},
                        "last_name": {"type": "string", "example": "Doe"},
                        "email": {"type": "string", "example": "john.doe@example.com"},
                        "password": {"type": "string", "example": "yourpassword"},
                        "avatar": {
                            "type": "string",
                            "example": "https://avatars.githubusercontent.com/u/93850343",
                        },
                    },
                    "required": ["first_name", "last_name", "email", "password"],
                },
            }
        ],
        "responses": {
            201: {"description": "User created successfully"},
            400: {"description": "User already exists"},
        },
    }
)
def signup():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    avatar = data.get("avatar")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user already exists
    existing_user = cursor.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    if existing_user:
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    # Insert the new user into the database
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, password, avatar) VALUES (?, ?, ?, ?, ?)",
        (first_name, last_name, email, hashed_password, avatar),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully"}), 201
