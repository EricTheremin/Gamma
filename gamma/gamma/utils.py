import os


def load_csv(file_name, file):

    dir = os.path.dirname(os.path.abspath(file))
    path = os.path.join(dir, 'manual_data', file_name)
    print("loading {}".format(path))
    return path
