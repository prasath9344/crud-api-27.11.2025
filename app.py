from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Build MySQL connection string from environment variables
db_user = os.getenv("DB_USER")
db_password = quote_plus(os.getenv("DB_PASSWORD"))  # ✅ encodes safely
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

print(db_user)
print(db_password)
print(db_host)
print(db_name)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define a simple User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))

# Create tables if they don't exist
with app.app_context():
    db.create_all()
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello World"})

# Get a users list
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])

# Create a user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

# Update user details
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'})
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# Delete a user details
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
