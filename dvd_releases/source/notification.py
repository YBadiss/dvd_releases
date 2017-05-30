import requests
import json
import logging

from movie_parser import get_new_dvd_releases
from secret import ONE_SIGNAL_AUTH_TOKEN

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_new_notifications():
    movies = filter(lambda m: m.is_released_today, get_new_dvd_releases())
    logger.info("Movies to notify found: {}".format(movies))
    for movie in movies:
        _send_new_release_notification(movie)


def _send_new_release_notification(movie):
    filter = {
        "field": "tag",
        "key": movie.id_,
        "relation": "=",
        "value": "true"
    }
    message = "'{}' was released today in DVD!".format(movie.title)
    _send_notification(message, filter)


def _send_notification(message, filter):
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Basic {}".format(ONE_SIGNAL_AUTH_TOKEN)
    }

    payload = {
        "app_id": "1a8f6a98-26b6-4b18-b1a6-ce8f7996f89d",
        "filters": [
            filter
        ],
        "contents": {
            "en": message
        }
    }

    requests.post("https://onesignal.com/api/v1/notifications",
                  headers=header,
                  data=json.dumps(payload))
