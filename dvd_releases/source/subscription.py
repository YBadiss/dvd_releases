import logging

from onesignal import add_tag, delete_tag, get_tags, send_new_releases_notification

logger = logging.getLogger()


def subscribe_to_movie(user_id, movie_id):
    return add_tag(user_id=user_id, tag=movie_id, value="true")


def unsubscribe_from_movie(user_id, movie_id):
    return delete_tag(user_id=user_id, tag=movie_id)


def get_subscriptions(user_id):
    return get_tags(user_id)


def notify_subscribers_for_movies(movies):
    send_new_releases_notification(movies)
