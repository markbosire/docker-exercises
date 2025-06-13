from flask import Flask, render_template_string
import psycopg2
import redis
import os

app = Flask(__name__)

@app.route('/')
def status():
    postgres_status = check_postgres()
    redis_status = check_redis()
    
    template = '''
    <h1>Service Connection Status</h1>
    <div style="font-size: 20px;">
        <p>PostgreSQL: {{ postgres_status }}</p>
        <p>Redis: {{ redis_status }}</p>
    </div>
    '''
    
    return render_template_string(template, 
                                postgres_status=postgres_status,
                                redis_status=redis_status)

def check_postgres():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        conn.close()
        return "✅ Connected"
    except:
        return "❌ Not Connected"

def check_redis():
    try:
        r = redis.from_url(os.getenv('REDIS_URL'))
        r.ping()
        return "✅ Connected"
    except:
        return "❌ Not Connected"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)