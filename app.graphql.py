import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# For working with GraphQL
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync
from resolvers import query, mutation
from ariadne.explorer import ExplorerGraphiQL

load_dotenv()  # Take environment variables from .env.

# Load the schema from the .graphql file
type_defs = load_schema_from_path("schema.graphql")

# Create the executable schema
schema = make_executable_schema(type_defs, [query, mutation])

# Create an instance of the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "your_default_secret_key"
)

# Initialize CORS with default settings (allows all origins)
CORS(app)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # Serve GraphiQL or GraphQL Playground using ExplorerGraphiQL
    return ExplorerGraphiQL().html(None)

@app.route("/graphql", methods=["POST", "OPTIONS"])
def graphql_server():
    # Handle preflight OPTIONS request for CORS
    if request.method == "OPTIONS":
        return '', 200
    
    # Handle POST request to the GraphQL server
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request},
        debug=True
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True, port=5001)
