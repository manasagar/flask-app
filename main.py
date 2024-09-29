from flask import Flask, request,jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()
app = Flask(__name__)
mongo_url = os.getenv('MONGODB_URL')
client = MongoClient(mongo_url, 27017)
def User_exists(id):
    cached_data = get_cache(id)
    if cached_data:
        return jsonify({"cached": True}), 200
    element = User.find_one({"id": id})
    if element:
        set_cache(id, element)
        return jsonify({"cached": False}), 200
    else:
        return None
def convert(user):
    user['_id']=str(user['_id'])
    return user
db = client.flask_db
User = db.User
cache=db.Cache
cache.create_index("created_at", expireAfterSeconds=int(os.getenv('CACHE_TTL')))
def get_cache(key):
    cache_entry = cache.find_one({"key": key})
    if cache_entry:
        return cache_entry["value"]
    return None
def set_cache(key, value):
    cache.update_one(
        {"key": key},
        {
            "$set": {
                "key": key,
                "value": value,
                "created_at": datetime.utcnow()
            }
        },
        upsert=True
    )
def delete_cache(key):
    cache.delete_one({"key",key})
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
        if  User.find_one({"id":id}):
            return jsonify({"error": "User already exists"}), 404
        User.insert_one({"name":name,"id":id,"email":email,"password":password})
        return jsonify("ok"), 202

@app.route('/users/<id>', methods=['GET','PUT','DELETE'])
def user(id):
    if not User_exists(id):
        return jsonify({"error": "User not found"}), 404
    
    if request.method=='GET':
        user=get_cache(id)
        print(user)
        user=convert(user)
        return jsonify(user)
    elif request.method=='PUT':
        data=request.json
        operation={'$set':data}
        user=User.update_one({"id":id},operation)
        set_cache(id,data)
        return jsonify(user.acknowledged)
    elif request.method=='DELETE':
        user=User.delete_one({"id":id})
        delete_cache(id)
        return jsonify(user.acknowledged)