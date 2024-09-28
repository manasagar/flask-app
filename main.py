from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
mongo_url = os.getenv('MONGODB_URL')
client = MongoClient(mongo_url, 27017)


@app.route('/user', methods=['POST', 'GET'])
def Users():
    pass
@app.route('/user/<id>', methods=['GET','PUT','DELETE'])
def login(id):
    pass