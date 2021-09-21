from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import redis

r = redis.StrictRedis(host='192.168.8.111', port=6379, db=2)
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def test():
    if request.method == 'GET':
        return jsonify({'message': 'success, redis'})


@app.route('/cache/<x>', methods=['POST', 'GET'])
def post(x):
    if request.method == 'POST':
        redis_key = x
        data = str((request.get_json())['data'])
        try:
            r.setex(redis_key, 43200*60, data)
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        return jsonify({'message': 'success'})
    if request.method == 'GET':
        try:
            (r.get(x))
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if (r.get(x)) != None:
            pre_data = ((r.get(x)).decode("utf-8")).replace("'", "\"")
            data = json.loads(pre_data)
            return jsonify({'post_id': x, 'data': data})
        else:
            return jsonify({'post_id': x, 'data': None})


if __name__ == '__main__':
    app.run()