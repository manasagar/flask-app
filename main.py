from flask import Flask, request,jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
mongo_url = os.getenv('MONGODB_URL')
client = MongoClient(mongo_url, 27017)
def convert(user):
    user['_id']=str(user['_id'])
    return user

db = client.flask_db
User = db.User
@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method=='GET':
        All_users=list(User.find())
        All_users = [convert(user) for user in All_users]
        return  jsonify(All_users)
    elif request.method=='POST':
        data = request.json 
        id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if  id is None or name is None or email is None or password is None:
            return "Missing data", 400
        User.insert_one({"name":name,"id":id,"email":email,"password":password})
        return "User Created"

@app.route('/users/<id>', methods=['GET','PUT','DELETE'])
def user(id):
    if not User.find_one({"id":id}):
        return jsonify({"error": "User not found"}), 404
    if request.method=='GET':
        user=User.find_one({"id":id})
        user=convert(user)
        return jsonify(user)
    elif request.method=='PUT':
        data=request.json
        operation={'$set':data}
        user=User.update_one({"id":id},operation)
        return jsonify(user.acknowledged)
    elif request.method=='DELETE':
        user=User.delete_one({"id":id})
        return jsonify(user.acknowledged)