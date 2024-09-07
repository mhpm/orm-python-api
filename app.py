from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import sqlite3
from flasgger import Swagger, swag_from  # Import Flasgger

# Create an instance of the Flask application
app = Flask(__name__)
PORT = 5001
CORS(app)

# Initialize Swagger with configuration
swagger = Swagger(app, config={
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all endpoints
            "model_filter": lambda tag: True,  # all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}, template={
    "swagger": "2.0",
    "info": {
        "title": "Python API",  # Set your desired title here
        "description": "API documentation for the user management system.",
        "version": "1.0.0"
    },
    "host": f"localhost:{PORT}",
    "basePath": "/",
})

# Helper function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to get all users (Read operation)
@app.route('/api/users', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of all users',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'first_name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'email': {'type': 'string'},
                        'avatar': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(row) for row in users])

# Route to get a specific user by ID (Read operation)
@app.route('/api/users/<int:user_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'A single user',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'avatar': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'User not found'
        }
    }
})
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

# Route to create a new user (Create operation)
@app.route('/api/users', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'first_name': {'type': 'string', 'example': 'John'},
                    'last_name': {'type': 'string', 'example': 'Doe'},
                    'email': {'type': 'string', 'example': 'john.doe@example.com'},
                    'avatar': {'type': 'string', 'example': 'https://example.com/avatar.png'}
                },
                'required': ['first_name', 'last_name', 'email']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User created successfully'
        }
    }
})
def create_user():
    new_user = request.get_json()
    first_name = new_user.get('first_name')
    last_name = new_user.get('last_name')
    email = new_user.get('email')
    avatar = new_user.get('avatar')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (first_name, last_name, email, avatar) VALUES (?, ?, ?, ?)',
                   (first_name, last_name, email, avatar))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User created successfully'}), 201

# Route to update an existing user (Update operation)
@app.route('/api/users/<int:user_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'avatar': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'User updated successfully'
        }
    }
})
def update_user(user_id):
    updated_user = request.get_json()
    first_name = updated_user.get('first_name')
    last_name = updated_user.get('last_name')
    email = updated_user.get('email')
    avatar = updated_user.get('avatar')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET first_name = ?, last_name = ?, email = ?, avatar = ?
        WHERE id = ?
    ''', (first_name, last_name, email, avatar, user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User updated successfully'})

# Route to delete a user (Delete operation)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'User deleted successfully'
        }
    }
})
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User deleted successfully'})

# Run the Flask app when the script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
