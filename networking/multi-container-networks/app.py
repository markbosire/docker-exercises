from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
redis_client = redis.Redis(host='redis-db', port=6379, decode_responses=True)

@app.route('/')
def home():
    try:
        count = redis_client.incr('visits')
        return jsonify({
            'message': f'Hello! You are visitor #{count}',
            'redis_host': 'redis-db'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)