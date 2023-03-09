from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/database'
mongo = PyMongo(app)

CORS(app)

db = mongo.db

@app.route('/users', methods=['POST'])
def create_user():
    user = db.users.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify(str(user.inserted_id))

@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in db.users.find():
        users.append({
            '_id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(user['_id']),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({
        'message': 'user deleted'
    })

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    print(request.json)
    db.users.update_one({'_id': ObjectId(id)}, {'$set': {
      'name': request.json['name'],
      'email': request.json['email'],
      'password': request.json['password']
    }})
    
    return jsonify({
        'message': 'user updated'
    })

if __name__ == '__main__':
    app.run(debug=True)
