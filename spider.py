import json

import scrapy

from movie import Movie


class DvdMoviesSpider(scrapy.Spider):
    name = "DvdMovies"
    start_urls = [
        "https://www.moviefone.com/dvd/"
    ]

    def __init__(self, *args, **kwargs):
        if "file" in kwargs:
            self.repo_path = kwargs.pop("file")
        else:
            self.repo_path = "./latest_movies.json"
        super(DvdMoviesSpider, self).__init__(*args, **kwargs)

        try:
            with open(self.repo_path, "r") as f:
                self.previous_movies = set([Movie(**m) for m in json.load(f)])
        except IOError:
            self.previous_movies = set()

    def parse(self, response):
        movies = set([self.parse_movie(s) for s in response.css(".movie-inner")[:10]])

        new_movies = movies - self.previous_movies
        if new_movies:
            print "New Movies: {}".format(new_movies)
            with open(self.repo_path, "w+") as f:
                json.dump([m.__dict__ for m in movies], f)
        else:
            print "No New Movies"

    def parse_movie(self, selector):
        return Movie(
            title=selector.css(".movie-title").xpath("text()").extract_first(),
            poster=selector.css(".movie-poster::attr(data-original)").extract_first(),
            more_info=selector.css(".button.blue::attr(href)").extract_first())
