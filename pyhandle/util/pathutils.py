import os


def _split_path(path_string):
    drive, rest = os.path.splitdrive(path_string)
    parts = [part for part in rest.split(os.path.sep) if part]
    return [drive + os.path.sep] + parts if drive else [os.path.sep] + parts


def get_absolute_path(path, file_path_string):
    if os.path.isabs(path):
        return path

    elif path.startswith(os.path.curdir):
        thisdir = get_this_directory(file_path_string)
        return os.path.normpath(os.path.join(thisdir, path))

    else:
        raise ValueError("Path is neither absolute nor relative.")


def get_this_directory(file_path_string, as_list=False):
    this_directory_string = os.path.dirname(os.path.realpath(file_path_string))

    if as_list:
        return _split_path(this_directory_string)
    else:
        return this_directory_string


def get_super_directory(file_path_string, as_list=False):
    super_directory_string = os.path.dirname(get_this_directory(file_path_string))

    if as_list:
        return _split_path(super_directory_string)
    else:
        return super_directory_string


def get_neighbour_directory(file_path_string, dirname):
    return os.path.join(get_super_directory(file_path_string), dirname)
