import logging
import urllib2

from movie import Movie
from bs4 import BeautifulSoup

logger = logging.getLogger()


def get_new_dvd_releases():
    page = urllib2.urlopen("https://www.moviefone.com/dvd/")
    return parse_new_dvd_releases(BeautifulSoup(page, "html.parser"))


def parse_new_dvd_releases(soup):
    soup_items = soup.find_all("div", {"class": "movie-inner"})
    return [parse_new_dvd_release(item) for item in soup_items]


def parse_new_dvd_release(soup):
    return Movie(title=soup.find("a", {"class": "movie-title"}).string,
                 poster=soup.find("img", {"class": "movie-poster"})["data-original"],
                 more_info=soup.find("a", {"class": "blue"})["href"])


if __name__ == "__main__":
    print get_new_dvd_releases()
