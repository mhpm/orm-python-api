from flask import Blueprint, request, jsonify
from flasgger import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import sqlite3


# Create a Blueprint for users
users_bp = Blueprint("users", __name__)


# Route to get all users (Read operation)
@users_bp.route("/users", methods=["GET"])
@swag_from(
    {
        "responses": {
            200: {
                "description": "A list of all users",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "email": {"type": "string"},
                            "role": {"type": "string"},
                            "avatar": {"type": "string"},
                        },
                    },
                },
            }
        }
    }
)
def get_users():
    conn = get_db_connection()
    users = conn.execute(
        "SELECT id, first_name, last_name, email, role, avatar FROM users"
    ).fetchall()

    conn.close()
    return jsonify([dict(row) for row in users])


# Route to get a specific user by ID (Read operation)
@users_bp.route("/users/<user_id>", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "ID of the user to retrieve",
            }
        ],
        "responses": {
            200: {
                "description": "A single user",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string"},
                        "avatar": {"type": "string"},
                    },
                },
            },
            404: {"description": "User not found"},
        },
    }
)
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, first_name, last_name, email, role, avatar FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))


# Route to create a new user (Create operation)
@users_bp.route("/users", methods=["POST"])
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
                        "role": {"type": "string", "example": "user | admin"},
                        "avatar": {
                            "type": "string",
                            "example": "https://example.com/avatar.png",
                        },
                    },
                    "required": ["first_name", "last_name", "email", "password"],
                },
            }
        ],
        "responses": {201: {"description": "User created successfully"}},
    }
)
def create_user():
    new_user = request.get_json()
    first_name = new_user.get("first_name")
    last_name = new_user.get("last_name")
    email = new_user.get("email")
    password = new_user.get("password")
    role = new_user.get("role")
    avatar = new_user.get("avatar")

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
        "INSERT INTO users (first_name, last_name, email, password, role, avatar) VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, email, hashed_password, role, avatar),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully"}), 201


# Route to update an existing user (Update operation)
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
@swag_from(
    {
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "ID of the user to update",
            },
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "avatar": {"type": "string"},
                    },
                },
            },
        ],
        "responses": {200: {"description": "User updated successfully"}},
    }
)
def update_user(user_id):
    updated_user = request.get_json()
    first_name = updated_user.get("first_name")
    last_name = updated_user.get("last_name")
    email = updated_user.get("email")
    avatar = updated_user.get("avatar")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users
        SET first_name = ?, last_name = ?, email = ?, avatar = ?
        WHERE id = ?
    """,
        (first_name, last_name, email, avatar, user_id),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "User updated successfully"})


# Route to delete a user (Delete operation)
@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@swag_from(
    {
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "ID of the user to delete",
            }
        ],
        "responses": {200: {"description": "User deleted successfully"}},
    }
)
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404  # User ID not found
        return jsonify({"message": "User deleted successfully"}), 200
    except sqlite3.Error as e:
        # Log the error details
        users_bp.logger.error(f"Database error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        # Log unexpected errors
        users_bp.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
