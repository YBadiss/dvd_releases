import requests
import json

from secret import ONE_SIGNAL_AUTH_TOKEN, ONE_SIGNAL_APP_ID

HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Basic {}".format(ONE_SIGNAL_AUTH_TOKEN)
}


def send_new_releases_notification(movies):
    _send_notification(message="Movies you like are now on DVD!",
                       filters=_build_filters(movies),
                       data=_build_data(movies))


def add_tag(user_id, tag, value):
    payload = {
        "app_id": ONE_SIGNAL_APP_ID,
        "tags": {
            tag: value
        }
    }
    res = requests.put(url="https://onesignal.com/api/v1/players/{}".format(user_id),
                       headers=HEADERS,
                       data=json.dumps(payload))
    return res.ok


def delete_tag(user_id, tag):
    return add_tag(user_id, tag, "")


def get_tags(user_id):
    res = requests.get(url="https://onesignal.com/api/v1/players/{}".format(user_id),
                       headers=HEADERS,
                       params={"app_id": ONE_SIGNAL_APP_ID})
    return res.json().get("tags", {}).keys()


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
    payload = {
        "app_id": ONE_SIGNAL_APP_ID,
        "filters": filters,
        "contents": {
            "en": message
        },
        "data": data
    }

    requests.post(url="https://onesignal.com/api/v1/notifications",
                  headers=HEADERS,
                  data=json.dumps(payload))
