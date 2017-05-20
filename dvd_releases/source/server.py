from flask import Flask, jsonify

from movie_parser import get_new_dvd_releases

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return 'Server is up.'


@app.route('/new-dvd-releases', methods=['GET'])
def new_dvd_releases():
    movies = get_new_dvd_releases()
    return jsonify([m.__dict__ for m in movies])


if __name__ == "__main__":
    app.run()
