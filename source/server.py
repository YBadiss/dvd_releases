from hashlib import sha1
import hmac

from flask import Flask, jsonify, abort, request

from store import Store

app = Flask(__name__)
store = Store()
secret = '6ZmzlO6w4YYLxEbXmQ3S'


@app.route('/')
def root():
    return 'Server is up.'


@app.route('/releases')
def releases():
    movies = store.get_new_releases()
    return jsonify([m.__dict__ for m in movies])


@app.route('/githook', methods=['POST'])
def githook():
    header_signature = request.headers.get('X-Hub-Signature')
    if not header_signature:
        abort(403)

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        abort(501)

    # HMAC requires the key to be bytes, but data is string
    mac = hmac.new(secret, msg=request.data, digestmod=sha1)

    if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
        abort(403)

    open('/home/ubuntu/.restart', 'a').close()
    return 'ok'


if __name__ == "__main__":
    app.run()
