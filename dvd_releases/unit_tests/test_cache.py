from datetime import timedelta
import mock
import unittest

from dvd_releases.source.cache import cached_call


@mock.patch("dvd_releases.source.cache.ENV_NAME", "fake")
@mock.patch("dvd_releases.source.cache.Redis")
class ParserTestCase(unittest.TestCase):
    def test_value_not_in_cache(self, redis_mock):
        # GIVEN
        full_key = "fake.key"
        expected_result = "ok"
        redis_mock().get.return_value = None
        serialize_mock = mock.Mock()
        deserialize_mock = mock.Mock()

        # WHEN
        result = cached_call(key="key",
                             func=lambda: expected_result,
                             serialize=serialize_mock,
                             deserialize=deserialize_mock)

        # THEN
        self.assertEqual(expected_result, result)
        redis_mock().get.assert_called_once_with(full_key)
        redis_mock().setex.assert_called_once_with(full_key,
                                                   serialize_mock(result),
                                                   timedelta(hours=2))

    def test_value_is_in_cache(self, redis_mock):
        # GIVEN
        full_key = "fake.key"
        expected_result = "ok"
        serialize_mock = mock.Mock()
        deserialize_mock = mock.Mock()
        deserialize_mock.return_value = expected_result

        # WHEN
        result = cached_call(key="key",
                             func=lambda: None,
                             serialize=serialize_mock,
                             deserialize=deserialize_mock)

        # THEN
        self.assertEqual(expected_result, result)
        redis_mock().get.assert_called_once_with(full_key)
        self.assertEqual(0, redis_mock().setex.call_count)
