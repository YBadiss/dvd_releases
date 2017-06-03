import requests
import unittest
import uuid

HEADERS = {'Content-Type': 'application/json; charset=utf-8'}


def make_url(path):
    return ("https://xt6la9orzh.execute-api.eu-west-1.amazonaws.com/production/"
            "dvd-releases/{}".format(path))


class ServerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = str(uuid.uuid4())
        self.user = "28853054-5992-4594-8c6b-f8edc5e904ba"
        self.del_sub()

    def tearDown(self):
        self.del_sub()

    def get_subs(self):
        response = requests.get(url=make_url("{}/sub".format(self.user)),
                                headers=HEADERS).json()
        return response["subscriptions"]

    def add_sub(self):
        return requests.post(url=make_url("{}/sub/{}".format(self.user, self.movie_id)),
                             headers=HEADERS)

    def del_sub(self):
        return requests.delete(url=make_url("{}/sub/{}".format(self.user, self.movie_id)),
                               headers=HEADERS)

    def test_add_and_delete_tag(self):
        self.assertFalse(self.movie_id in self.get_subs())

        self.assertTrue(self.add_sub().ok)
        self.assertTrue(self.movie_id in self.get_subs())

        self.assertTrue(self.del_sub().ok)
        self.assertFalse(self.movie_id in self.get_subs())
