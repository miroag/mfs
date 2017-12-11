import bs4
import requests


def n(src):
    """
    Normalize the link. Very basic implementation
    :param src:
    :return:
    """
    if src.startswith('//'):
        src = 'http:' + src
    return src


def sluggify(text):
    """
    Create a file system friendly string from passed text by stripping special characters.
     Use this function to make file names from arbitrary text, like titles
    :param text:
    :return:
    """
    if not text:
        return ''
    data = ''.join([c for c in text if c.isalpha() or c.isdigit() or c in [' ', '.', ',' , '_', '-', '=']]).rstrip()
    truncated = data[:75] if len(data) > 75 else data
    return truncated


def soup(url):
    """
    Simple wrapper to BeautifulSoup object from url
    :param url:
    :return: BeautifulSoup
    """

    r = requests.get(url=url)
    r.raise_for_status()
    # force encoding into utf-8 as sometimes airbase comes back in 'ISO-8859-1'
    r.encoding = 'utf-8'
    return bs4.BeautifulSoup(r.text, 'html.parser')
