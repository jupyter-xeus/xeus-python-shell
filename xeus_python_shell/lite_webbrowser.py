"""
An implementation of the standard library webbrowser module to open webpages.

For now this is a no-op.
"""


def open(url, new=0, autoraise=True):
    pass


def open_new(url):
    return open(url, 1)


def open_new_tab(url):
    return open(url, 2)
