from datetime import datetime, timedelta
import unittest

from dvd_releases.source.movie import Movie


class MovieTestCase(unittest.TestCase):
    def test_movie_dictify(self):
        # GIVEN
        expected_movie = Movie(id_=1,
                               title='the movie',
                               poster='the poster',
                               more_info='more info',
                               release_date=datetime.now())

        # WHEN
        actual_movie = Movie.from_dict(expected_movie.as_dict())

        # THEN
        for key in expected_movie.__dict__.keys():
            self.assertEqual(getattr(expected_movie, key), getattr(actual_movie, key))

    def test_is_released_today(self):
        # GIVEN
        today_movie = Movie(id_=1,
                            title='the movie',
                            poster='the poster',
                            more_info='more info',
                            release_date=datetime.now())
        tomorrow_movie = Movie(id_=1,
                               title='the movie',
                               poster='the poster',
                               more_info='more info',
                               release_date=datetime.now() + timedelta(days=1))

        # THEN
        self.assertTrue(today_movie.is_released_today)
        self.assertFalse(tomorrow_movie.is_released_today)
