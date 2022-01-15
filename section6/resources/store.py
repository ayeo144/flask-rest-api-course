from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):

	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store is not None:
			return store.to_json()
		return {'message': 'Store not found'}, 404

	def post(self, name):
		if StoreModel.find_by_name(name) is not None:
			return {'message': f'Store with name {name} already exists'}, 400

		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message': 'An error occurred creating the store'}, 500

		return store.to_json(), 201

	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store is not None:
			store.delete_from_db()

		return {'message': f'Store deleted'}


class StoreList(Resource):
	
	def get(self):
		return {'stores': [store.to_json() for store in StoreModel.query.all()]}