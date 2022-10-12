import flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = flask.Flask(__name__)

# Define size limit for POST requests (It should only be maximum of 64 bytes)
app.config['MAX_CONTENT_LENGTH'] = 64*2

# Use rate limit of 10 requests per second
rate_limit = Limiter(
    app, 
    key_func=get_remote_address, 
    default_limits=["10 per second"]
)

@app.route('/api', methods=['GET', 'PUT', 'DELETE'])
def api():
    if flask.request.method == 'GET':
        return get()
    elif flask.request.method == 'PUT':
        return put(flask.request.data)
    elif flask.request.method == 'DELETE':
        return delete(flask.request.data)
    else:
        return 'Unknown'

def get():
    return open('store,txt', 'r').read()

def put(data):
    # append data to store.txt
    with open('store.txt', 'a') as f:
        f.write(data)
    return 'OK'

def delete(data):
    # delete data from store.txt
    with open('store.txt', 'r') as f:
        lines = f.readlines()
    with open('store.txt', 'w') as f:
        for line in lines:
            if line != data:
                f.write(line)
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)