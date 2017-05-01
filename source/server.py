from flask import Flask, jsonify

from store import Store

app = Flask(__name__)
store = Store()


@app.route('/')
def root():
    return 'Server is up.'


@app.route('/releases')
def releases():
    movies = store.get_new_releases()
    return jsonify([m.__dict__ for m in movies])


if __name__ == "__main__":
    app.run()
