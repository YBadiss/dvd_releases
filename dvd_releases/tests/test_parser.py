import os
import unittest

from bs4 import BeautifulSoup

from dvd_releases.source.movie import Movie
from dvd_releases.source.movie_parser import parse_new_dvd_releases


def bs_from_file(path):
    """
    Create a new BeautifulSoup object from a file which path is provided as argument
    """
    full_path = "{}/{}".format(os.path.dirname(__file__), path)
    with open(full_path) as f:
        return BeautifulSoup(f, "html.parser")


def bs_source(path):
    """
    Given a relative path to an html file, we build a BeautifulSoup object and pass it to
    the decorated function to use for testing parsing methods.
    This allows us to reproduce parsing errors, unit test them, and ensure they never come 
    back to bite us because of a parsing refactor.
    """
    def test_decorator(func):
        def test_decorated(*args, **kwargs):
            args_ = list(args) + [bs_from_file(path)]
            func(*args_, **kwargs)
        return test_decorated
    return test_decorator


class ParserTestCase(unittest.TestCase):
    @bs_source("html_pages/new_dvd_releases.htm")
    def test_parse_new_dvd_releases(self, soup):
        # GIVEN
        movie = Movie(title="The Space Between Us",
                      poster=("https://o.aolcdn.com/images/dims?resize=291%2C437&quality="
                              "70&image_uri=http%3A%2F%2Faolx.tmsimg.com%2Fmovieposters%2"
                              "Fv7%2FNowShowing%2F12560207%2Fp12560207_p_v7_ad.jpg%3Fw%3D"
                              "291&client=cbc79c14efcebee57402&signature=1aa7f2d0e8c94146"
                              "9544d3d905d9e43a71927251"),
                      more_info=("https://www.moviefone.com/movie/the-space-between-us/20"
                                 "078145/main/"))

        # WHEN
        dvd_releases = parse_new_dvd_releases(soup)

        # THEN
        self.assertEqual(len(dvd_releases), 36)
        actual_movie = dvd_releases[2]
        for attr in actual_movie.__dict__:
            self.assertEqual(getattr(actual_movie, attr), getattr(movie, attr))

