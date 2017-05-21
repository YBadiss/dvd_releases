from datetime import datetime
import mock
import os
import unittest

from dvd_releases.source.movie import Movie
from dvd_releases.source.movie_parser import get_new_dvd_releases, get_future_dvd_releases


def html_file(path):
    full_path = "{}/{}".format(os.path.dirname(__file__), path)
    with open(full_path) as f:
        return f.read()


@mock.patch("dvd_releases.source.movie_parser.urllib2")
class ParserTestCase(unittest.TestCase):
    def test_get_new_dvd_releases(self, urllib_mock):
        # GIVEN
        urllib_mock.urlopen.return_value = html_file("html_pages/new_dvd_releases.htm")
        movie = Movie(title="The Space Between Us",
                      poster=("https://o.aolcdn.com/images/dims?resize=291%2C437&quality="
                              "70&image_uri=http%3A%2F%2Faolx.tmsimg.com%2Fmovieposters%2"
                              "Fv7%2FNowShowing%2F12560207%2Fp12560207_p_v7_ad.jpg%3Fw%3D"
                              "291&client=cbc79c14efcebee57402&signature=1aa7f2d0e8c94146"
                              "9544d3d905d9e43a71927251"),
                      more_info=("https://www.moviefone.com/movie/the-space-between-us/20"
                                 "078145/main/"),
                      release_date=datetime(year=2017, month=5, day=16))

        # WHEN
        new_dvd_releases = get_new_dvd_releases()

        # THEN
        self.assertEqual(len(new_dvd_releases), 36)
        actual_movie = new_dvd_releases[2]
        for attr in actual_movie.__dict__:
            self.assertEqual(getattr(actual_movie, attr), getattr(movie, attr))

    def test_get_future_dvd_releases(self, urllib_mock):
        # GIVEN
        urllib_mock.urlopen.return_value = html_file("html_pages/future_dvd_releases.htm")
        movie = Movie(title="I Am Heath Ledger",
                      poster=("https://o.aolcdn.com/images/dims?resize=291%2C437&quality="
                              "70&image_uri=https%3A%2F%2Fs3.amazonaws.com%2Fmoviefone%2F"
                              "images%2Fposters%2Fheath-poster_1492556885.jpg&client=cbc7"
                              "9c14efcebee57402&signature=cd0d2125ae67c7ee7ee0b2810327e48"
                              "05aca454d"),
                      more_info=("https://www.moviefone.com/movie/i-am-heath-ledger/swFO6"
                                 "RpOgvKONRXLmcYEL1/main/"),
                      release_date=datetime(year=2017, month=5, day=23))

        # WHEN
        future_dvd_releases = get_future_dvd_releases()

        # THEN
        self.assertEqual(len(future_dvd_releases), 36)
        actual_movie = future_dvd_releases[2]
        for attr in actual_movie.__dict__:
            self.assertEqual(getattr(actual_movie, attr), getattr(movie, attr))

