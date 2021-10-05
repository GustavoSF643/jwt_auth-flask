from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import sqlalchemy
from app.exceptions.user_exc import InvalidKeysError, WrongPasswordError
from app.models.user_model import UserModel
from flask import request, jsonify


def create_user():
    try: 
        user_data = request.json

        password_to_hash = user_data.pop("password")
        
        user: UserModel = UserModel(**user_data)
        user.password = password_to_hash
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
        
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    except WrongPasswordError as e:
        return {'message': str(e)}, 401
    except sqlalchemy.exc.NoResultFound:
        return {'message': 'User not found'}, 404
    except KeyError as e:
        return {'message': 'Keys not acceptable. Valid keys: (email, password).'}, 406


@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = UserModel.query.get(user_id)
    return jsonify(user), 200


@jwt_required()
def update_user():
    try:
        user_data = request.json

        user_id = get_jwt_identity()
        user: UserModel = UserModel.query.get(user_id)
        user.update_user(user_data)
        user.save()

        return jsonify(user), 200
    except InvalidKeysError as e:
        return jsonify({'message': str(e)}), 406


@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user: UserModel = UserModel.query.get(user_id)
    user.delete_user()

    return jsonify({'msg': f'User {user.name} has been deleted'}), 200