from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name)

# Подключение к MongoDB
client = MongoClient("mongodb", 27017)
db = client["mydb"]
collection = db["mycollection"]

@app.route('/api/<key>', methods=['GET', 'POST', 'PUT'])
def handle_key(key):
    if request.method == 'GET':
        result = collection.find_one({'_id': key})
        if result:
            return jsonify({key: result['value']}), 200
        else:
            return 'Key not found', 404
    elif request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
        value = data.get('value')
        if not value:
            return 'Missing value', 400
        collection.update_one({'_id': key}, {'$set': {'value': value}}, upsert=True)
        return 'Key updated', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
