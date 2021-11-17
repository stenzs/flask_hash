from flask import Flask, request, jsonify
from flask_cors import CORS
import redis

r = redis.StrictRedis(host='192.168.145.195', port=6379, db=2)
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def test():
    if request.method == 'GET':
        return jsonify({'message': 'success, redis'})


@app.route('/cache_phone_cleex/<x>', methods=['POST'])
def cache(x):
    if request.method == 'POST':
        data = request.get_json()
        seconds = 90
        redis_key = str(x) + 'cleex'
        value = str(data['data'])
        secret = str(data['secret'])
        if secret != 'saf3535gasg':
            return jsonify({'message': 'error'})
        try:
            r.setex(redis_key, seconds, value)
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        return jsonify({'message': 'success'})


@app.route('/check_phone_cleex/<x>', methods=['POST'])
def check(x):
    if request.method == 'POST':
        data = request.get_json()
        value = str(data['data'])
        secret = str(data['secret'])
        if secret != 'saf3535gasg':
            return jsonify({'message': 'error'})
        seconds = 90
        try:
            count = (r.get(str('count_cleex') + str(x)))
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if count is not None:
            count = count.decode("utf-8")
        else:
            count = 0
        try:
            r.setex(str('count_cleex') + str(x), seconds, int(count) + 1)
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if int(count) >= 3:
            return jsonify({'message': 'time error'})
        try:
            (r.get(str(x) + 'cleex'))
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if (r.get(str(x) + 'cleex')) is not None:
            data = (r.get(str(x) + 'cleex')).decode("utf-8")
            if str(data) == str(value):
                return jsonify({'check': True})
            else:
                return jsonify({'check': False})
        else:
            return jsonify({'check': False})


@app.route('/cache_phone_kvik/<x>', methods=['POST'])
def cache(x):
    if request.method == 'POST':
        data = request.get_json()
        seconds = 90
        redis_key = str(x) + 'kvik'
        value = str(data['data'])
        secret = str(data['secret'])
        if secret != 'saf3535gasg':
            return jsonify({'message': 'error'})
        try:
            r.setex(redis_key, seconds, value)
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        return jsonify({'message': 'success'})


@app.route('/check_phone_kvik/<x>', methods=['POST'])
def check(x):
    if request.method == 'POST':
        data = request.get_json()
        value = str(data['data'])
        secret = str(data['secret'])
        if secret != 'saf3535gasg':
            return jsonify({'message': 'error'})
        seconds = 90
        try:
            count = (r.get(str('count_kvik') + str(x)))
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if count is not None:
            count = count.decode("utf-8")
        else:
            count = 0
        try:
            r.setex(str('count_kvik') + str(x), seconds, int(count) + 1)
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if int(count) >= 3:
            return jsonify({'message': 'time error'})
        try:
            (r.get(str(x) + 'kvik'))
        except Exception as e:
            return jsonify({'message': 'error', 'error': e})
        if (r.get(str(x) + 'kvik')) is not None:
            data = (r.get(str(x) + 'kvik')).decode("utf-8")
            if str(data) == str(value):
                return jsonify({'check': True})
            else:
                return jsonify({'check': False})
        else:
            return jsonify({'check': False})


if __name__ == '__main__':
    app.run()
