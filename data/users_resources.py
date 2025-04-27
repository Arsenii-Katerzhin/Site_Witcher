from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .users import User
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('modified_date', required=True)


def abort_if_users_not_found(user_id):
	session = db_session.create_session()
	users = session.query(User).get(user_id)
	if not users:
		abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
	def get(self, user_id):
		abort_if_users_not_found(user_id)
		session = db_session.create_session()
		users = session.query(User).get(user_id)
		return jsonify({'users': users.to_dict()})

	def delete(self, user_id):
		abort_if_users_not_found(user_id)
		session = db_session.create_session()
		users = session.query(User).get(user_id)
		session.delete(users)
		session.commit()
		return jsonify({'success': 'OK'})


class UsersListResource(Resource):
	def get(self):
		session = db_session.create_session()
		users = session.query(User).all()
		return jsonify({'users': [item.to_dict() for item in users]})

	def post(self):
		args = parser.parse_args()
		session = db_session.create_session()
		users = User(
			id=args['id'],
			surname=args['surname'],
			name=args['name'],
			age=args['age'],
			position=args['position'],
			speciality=args['speciality'],
			address=args['address'],
			email=args['email'],
			modified_date=args['modified_date']
		)
		session.add(users)
		session.commit()
		return jsonify({'id': users.id})
