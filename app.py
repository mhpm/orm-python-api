import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger  # Import Flasgger
from dotenv import load_dotenv
from auth import auth_bp
from users import users_bp

load_dotenv()  # take environment variables from .env.

# Create an instance of the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "1237ac0393917173029ad602d3152bd523ce383e9a89790b098fbf4c6a461ad8"
)
CORS(app)


# Initialize Swagger with configuration
swagger = Swagger(
    app,
    config={
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,  # all endpoints
                "model_filter": lambda tag: True,  # all models
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/",
    },
)


# Update Swagger configuration to set the host dynamically
@app.before_request
def set_swagger_host():
    swagger.template = {
        "swagger": "2.0",
        "info": {
            "title": "Python API",
            "description": "API documentation for the user management system.",
            "version": "1.0.0",
        },
        "host": request.host,  # Set the host from the current request
        "basePath": "/",
        "schemes": ["http", "https"],
        "paths": {},  # Empty initially; filled by Flasgger
    }


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)


# Run the Flask app when the script is executed directly
# API deployed on render.com
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
