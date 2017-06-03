from dateutil import parser
import logging
import urllib2

from bs4 import BeautifulSoup
from movie import Movie

logger = logging.getLogger()


def get_new_dvd_releases():
    page = urllib2.urlopen("https://www.moviefone.com/dvd/")
    return _parse_dvds(BeautifulSoup(page, "html.parser"))


def get_future_dvd_releases():
    page = urllib2.urlopen("https://www.moviefone.com/dvd/coming-soon/")
    return _parse_dvds(BeautifulSoup(page, "html.parser"))


def _parse_dvds(soup):
    soup_items = soup.find_all("li", {"class": "movie-wrapper"})
    return [_parse_dvd(item) for item in soup_items]


def _parse_dvd(soup):
    release_date = soup.find("span", {"class": "available-text"}).string
    release_date = parser.parse(release_date.replace("Available", "").strip())

    return Movie(id_=soup["rel"],
                 title=soup.find("a", {"class": "movie-title"}).string,
                 poster=soup.find("img", {"class": "movie-poster"})["data-original"],
                 more_info=soup.find("a", {"class": "blue"})["href"],
                 release_date=release_date)
