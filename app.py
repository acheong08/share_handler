import flask

app = flask.Flask(__name__)

# Define size limit for POST requests (It should only be maximum of 64 bytes)
app.config['MAX_CONTENT_LENGTH'] = 64*2
# Prevent DDOS attacks by limiting the number of requests per second
# 10 requests per second
flask.g.rate_limit = 10
# before_request is a decorator that is called before every request
@app.before_request
def limit_remote_addr():
    flask.g.rate_limit = flask.g.rate_limit - 1
    if flask.g.rate_limit < 0:
        return 'Too many requests', 429

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