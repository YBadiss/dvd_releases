import logging

import scrapy

from movie import Movie
from store import Store

logger = logging.getLogger()


class DvdMoviesSpider(scrapy.Spider):
    name = "DvdMovies"
    start_urls = [
        "https://www.moviefone.com/dvd/"
    ]

    def __init__(self, *args, **kwargs):
        super(DvdMoviesSpider, self).__init__(*args, **kwargs)
        self.store = Store()
        self.previous_movies = self.store.get_new_releases()
        logger.info("Retrieving latest movies previous_movies={}"
                    .format(self.previous_movies))

    def parse(self, response):
        movies = [self.parse_movie(s) for s in response.css(".movie-inner")]

        new_movies = set(movies) - set(self.previous_movies)
        if new_movies:
            logger.info("New Movies: {}".format(new_movies))
            self.store.set_new_releases(movies)
        else:
            logger.info("No New Movies")

    def parse_movie(self, selector):
        return Movie(
            title=selector.css(".movie-title").xpath("text()").extract_first(),
            poster=selector.css(".movie-poster::attr(data-original)").extract_first(),
            more_info=selector.css(".button.blue::attr(href)").extract_first())
