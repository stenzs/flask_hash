from flask import Flask, request, jsonify
import redis

r = redis.StrictRedis(host='192.168.8.111', port=6379, db=2)
app = Flask(__name__)


@app.route('/cache/<x>', methods=['POST', 'GET'])
def post(x):
    if request.method == 'POST':
        redis_key = x
        data = (request.get_json())['data']
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
            return jsonify({'post_id': x, 'data': (r.get(x)).decode("utf-8") })
        else:
            return jsonify({'post_id': x, 'data': None})


if __name__ == '__main__':
    app.run()