from pymongo import MongoClient

from movie import Movie


class Store(object):
    DB_NAME = "dvd_releases"

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[Store.DB_NAME]

    def get_new_releases(self):
        new_releases = self.db.new_releases
        return [
            Movie(**e)
            for e in sorted(new_releases.find(), key=lambda m: m.get("idx"))
        ]

    def set_new_releases(self, movies):
        def merge_dicts(x, y):
            z = x.copy()
            z.update(y)
            return z
        new_releases = self.db.new_releases
        new_releases.delete_many({})
        new_releases.insert_many([
            merge_dicts({"idx": i}, m.__dict__)
            for i, m in enumerate(movies)
        ])
