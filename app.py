from flask import Flask
import redis
import os

app = Flask(__name__)

# Get Redis config from environment variables
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

# Connect to Redis
try:
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    r.ping()
except redis.RedisError:
    r = None

@app.route("/")
def home():
    return "Welcome to my DevOps app!"

@app.route("/visit")
def visit():
    if r:
        count = r.incr("visit_count")
        return f"Visit count: {count}"
    else:
        return "Redis connection failed.", 500

@app.route("/health")
def health():
    if r:
        try:
            r.ping()
            return "OK", 200
        except redis.RedisError:
            return "Redis not reachable", 500
    return "Redis not initialized", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)