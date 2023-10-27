from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy  # Используйте flask_sqlalchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


class User(db.Model):  # Поправьте имя класса на User
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Поправьте db.integer на db.Integer
    username = db.Column(db.String(120), unique=True, nullable=False)  # Поправьте unicue на unique
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


db.create_all()


# Уберите db.create_all() из этого места, лучше вызывать его при необходимости в отдельном скрипте

@app.route('/test', methods=['GET'])  # Исправьте app.rout на app.route
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# Create user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'user not created'}), 500)


# Get users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    except Exception as e:  # Исправьте except e на except Exception as e
        return make_response(jsonify({'message': 'error getting users'}), 500)


# Get users by id
@app.route('/users/<int:id>', methods=['GET'])  # Исправьте app.rout на app.route
def get_user_by_id(id):
    try:
        user = User.query.get(id)
        if user:
            return make_response(jsonify(user.json()), 200)
        else:
            return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:  # Исправьте except e на except Exception as e
        return make_response(jsonify({'message': 'error getting user'}), 500)


# Put user by id
@app.route('/users/<int:id>', methods=['PUT'])  # Маршрут для обновления пользователя по его ID
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        data = request.get_json()
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']

        db.session.commit()
        return make_response(jsonify({'message': 'User updated'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error updating user'}), 500)


# Delete user by id
@app.route('/users/<int:id>', methods=['DELETE'])  # Маршрут для удаления пользователя по его ID
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User deleted'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting user'}), 500)


if __name__ == '__main__':
    app.run()
