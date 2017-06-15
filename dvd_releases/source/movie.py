from datetime import date

from dateutil import parser


class Movie(object):
    def __init__(self, id_, title, poster, more_info, release_date):
        self.id_ = id_
        self.title = title
        self.poster = poster
        self.more_info = more_info
        self.release_date = release_date

    @property
    def is_released_today(self):
        return self.release_date.date() == date.today()

    def as_dict(self):
        return {
            "id_": self.id_,
            "title": self.title,
            "poster": self.poster,
            "more_info": self.more_info,
            "release_date": str(self.release_date)
        }

    @staticmethod
    def from_dict(dict_):
        dict_["release_date"] = parser.parse(dict_["release_date"])
        return Movie(**dict_)

    def __repr__(self):
        return "Movie(title={})".format(self.title)

    def __hash__(self):
        return hash(self.title)

    def __cmp__(self, rhs):
        return cmp(self.title, rhs.title)

    def __eq__(self, rhs):
        return self.title == rhs.title
