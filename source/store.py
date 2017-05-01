from pymongo import MongoClient

from movie import Movie


class Store(object):
    DB_NAME = "dvd_releases"

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[Store.DB_NAME]

    def get_new_releases(self):
        new_releases = self.db.new_releases
        return [Movie(**e) for e in new_releases.find()]

    def set_new_releases(self, movies):
        new_releases = self.db.new_releases
        new_releases.delete_many({})
        new_releases.insert_many([m.__dict__ for m in movies])
