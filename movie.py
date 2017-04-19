class Movie(object):
    def __init__(self, title, poster, more_info):
        self.title = title
        self.poster = poster
        self.more_info = more_info

    def __repr__(self):
        return "Movie(title={})".format(self.title)

    def __hash__(self):
        return hash(self.title)

    def __cmp__(self, rhs):
        return cmp(self.title, rhs.title)

    def __eq__(self, rhs):
        return self.title == rhs.title