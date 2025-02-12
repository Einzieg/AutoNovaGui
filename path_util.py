import os
import sys


def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
