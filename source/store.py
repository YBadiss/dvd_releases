from pymongo import MongoClient

from movie import Movie


class Store(object):
    DB_NAME = "dvd_releases"

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[Store.DB_NAME]

    def get_movies(self):
        movies = self.db.movies
        return [Movie(**e) for e in movies.find()]

    def set_movies(self, new_movies):
        movies = self.db.movies
        movies.delete_many({})
        movies.insert_many([m.__dict__ for m in new_movies])

    def get_users(self):
        users = self.db.users
        return [u['number'] for u in users.find()]

    def add_user(self, number):
        users = self.db.users
        users.insert_one({'number': number})
