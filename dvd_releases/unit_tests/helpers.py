import os


def html_file(path):
    full_path = "{}/{}".format(os.path.dirname(__file__), path)
    with open(full_path) as f:
        return f.read()
