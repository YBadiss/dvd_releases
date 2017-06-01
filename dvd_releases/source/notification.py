import requests
import json
import logging

from movie_parser import get_new_dvd_releases
from secret import ONE_SIGNAL_AUTH_TOKEN

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_new_notifications():
    movies = filter(lambda m: m.is_released_today, get_new_dvd_releases())
    if movies:
        logger.info("Sending notifications for movies: {}".format(movies))
        _send_new_releases_notification(movies)
    else:
        logger.info("No notifications to send")


def _send_new_releases_notification(movies):
    _send_notification(message="Movies you like are now on DVD!",
                       filters=_build_filters(movies),
                       data=_build_data(movies))


def _build_filters(movies):
    filters = []
    for movie in movies:
        filters.append({
            "field": "tag",
            "key": movie.id_,
            "relation": "exists"
        })
        filters.append({"operator": "OR"})
    filters.pop()  # remove last OR operator
    return filters


def _build_data(movies):
    return {
        "movie_ids": json.dumps([movie.id_ for movie in movies])
    }


def _send_notification(message, filters, data):
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Basic {}".format(ONE_SIGNAL_AUTH_TOKEN)
    }

    payload = {
        "app_id": "1a8f6a98-26b6-4b18-b1a6-ce8f7996f89d",
        "filters": filters,
        "contents": {
            "en": message
        },
        "data": data
    }

    requests.post("https://onesignal.com/api/v1/notifications",
                  headers=header,
                  data=json.dumps(payload))
