from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import redis

r = redis.StrictRedis(host='192.168.145.195', port=6379, db=2)
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def test():
    if request.method == 'GET':
        return jsonify({'message': 'success, redis'})


@app.route('/cache/<x>', methods=['POST', 'GET'])
def post(x):
    if request.method == 'POST':
        data = request.get_json()
        seconds = 90
        redis_key = x
        value = str(data['data'])
        try:
            r.setex(redis_key, seconds, value)
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        return jsonify({'message': 'success'})
    if request.method == 'GET':
        try:
            (r.get(x))
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if (r.get(x)) != None:
            # pre_data = ((r.get(x)).decode("utf-8")).replace("'", "\"")
            # data = json.loads(pre_data)
            data = r.get(x)
            return jsonify({'post_id': x, 'data': data})
        else:
            return jsonify({'post_id': x, 'data': None})


if __name__ == '__main__':
    app.run()