import logging
import json

from flask import Flask, jsonify, request, make_response

from movie_parser import get_new_dvd_releases, get_future_dvd_releases
from subscription import (get_subscriptions,
                          notify_subscribers_for_movies,
                          subscribe_to_movie,
                          unsubscribe_from_movie)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return "Server is up."


@app.route("/dvd-releases/new", methods=["GET"])
def get_new_dvd_releases_request():
    movies = get_new_dvd_releases()
    return jsonify([m.__dict__ for m in movies])


@app.route("/dvd-releases/future", methods=["GET"])
def get_future_dvd_releases_request():
    movies = get_future_dvd_releases()
    return jsonify([m.__dict__ for m in movies])


@app.route("/dvd-releases/<user_id>/sub", methods=["GET"])
def get_subscriptions_request(user_id):
    return make_response(json.dumps({"subscriptions": get_subscriptions(user_id)}))


@app.route("/dvd-releases/<user_id>/sub/<movie_id>", methods=["POST", "DELETE"])
def handle_sub(user_id, movie_id):
    if request.method == "POST":
        success = subscribe_to_movie(user_id=user_id, movie_id=movie_id)
    elif request.method == "DELETE":
        success = unsubscribe_from_movie(user_id=user_id, movie_id=movie_id)
    return make_response(("success", 200) if success else ("failure", 400))


def notify_of_new_releases():
    movies = filter(lambda m: m.is_released_today, get_new_dvd_releases())
    if movies:
        logger.info("Notifying subscribers for movies: {}".format(movies))
        notify_subscribers_for_movies(movies)
    else:
        logger.info("No notifications to send")


if __name__ == "__main__":
    app.run()
