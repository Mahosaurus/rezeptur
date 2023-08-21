import os

def get_repo_root() -> str:
    """
    Returns the absolute path to the root of the  repository
    specific to the system the code is run on.
    """
    path_to_this_file = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/"
    return path_to_this_file
