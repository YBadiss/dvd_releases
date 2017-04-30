import logging

from scripts.send_sms import send_msg

logger = logging.getLogger()


def new_movies(movies, users):
    for user in users:
        logger.info("Notifying user {}".format(user))
        send_msg(_make_body(movies), user)


def _make_body(movies):
    return "New Movies To DL!\n{}".format(
        "\n".join(["{} ({})".format(m.title, m.more_info) for m in movies]))
