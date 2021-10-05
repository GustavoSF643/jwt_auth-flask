import sqlalchemy
from app.exceptions.user_exc import WrongPasswordError
from app.models.user_model import UserModel
from flask import request, jsonify
from app.configs.auth import auth


def create_user():
    try: 
        user_data = request.json

        password_to_hash = user_data.pop("password")
        
        user: UserModel = UserModel(**user_data)
        user.password = password_to_hash
        user.create_api_key()
        user.save()

        return {"message": "User created"}, 201
    except KeyError as e:
        return {'message': 'Keys not acceptable. Valid keys: (name, last_name, email, password).'}, 406
    except sqlalchemy.exc.IntegrityError:
        return {'message': 'User already exists.'}, 409

def login():
    try:
        user_data = request.json

        user: UserModel = UserModel.query.filter_by(email=user_data["email"]).one()

        user.verify_password(user_data['password'])
        
        return {'api_key': user.api_key}, 200
    except WrongPasswordError as e:
        return {'message': str(e)}, 401
    except sqlalchemy.exc.NoResultFound:
        return {'message': 'User not found'}, 404
    except KeyError as e:
        return {'message': 'Keys not acceptable. Valid keys: (email, password).'}, 406


@auth.login_required
def get_user():
    return jsonify(auth.current_user()), 200


@auth.login_required
def update_user():

    user_data = request.json

    user: UserModel = auth.current_user()
    user.update_user(user_data)
    user.save()

    return jsonify(user), 200


@auth.login_required
def delete_user():
    user: UserModel = auth.current_user()
    user.delete_user()

    return jsonify({'msg': f'User {user.name} has been deleted'}), 200