import logging

logger = logging.getLogger()


def new_movies(movies, users):
    for user in users:
        logger.info("Notifying user {}".format(user))
        # TODO send notif
