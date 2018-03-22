from uuid import uuid4

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////D:/python_code/flask_api/api.db'
app.config["SECRET_KEY"] = 'hard words'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=lambda: uuid4())
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default=False)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50))
    completed = db.Column(db.Boolean, default=False)


@app.before_first_request
def create_database():
    db.create_all()


@app.route('/user', methods=["GET"])
def get_user():
    users_list = User.query.all()
    out_put = list()
    for user in users_list:
        user_data = {
            'public_id': user.public_id,
            "username": user.username,
            "password": user.password,
            "admin": user.admin
        }
        out_put.append(user_data)

    return jsonify({"users_info": out_put})


@app.route('/user/<user_id>', methods=["PUT"])
def get_one_user(user_id):
    user = User.query.filter_by(public_id=user_id).first()
    if user:
        user_data = {
            'public_id': user.public_id,
            "username": user.username,
            "password": user.password,
            "admin": user.admin
        }
        return jsonify({"status": 200, "data": user_data})
    return jsonify({"status": 200, "message": "User is not found "})


@app.route('/user', methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        user = User()
        user.username = data['username']
        user.password = generate_password_hash(data['password'], method="sha256")
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": 200, "message": "Successfully create user!"})
    except:
        return jsonify({"status": 200, "message": "User is not found! "})


@app.route('/user/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(public_id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": 200, "message": "User has been deleted "})
    return jsonify({"status": 200, "message": "User is not found "})

 
if __name__ == '__main__':
    app.run()