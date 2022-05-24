from todo import create_app
from flask import Blueprint, jsonify, request


app = create_app()




if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, port='5001')
