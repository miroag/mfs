"""
    Model Forums Scraper (mfs)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    mfs is a set of utilities to ease scraping images from some Russian sites related to modelling


Usage:
  mfs URL [-d DESTINATION]

Arguments:
    URL         Location.
Supported locations are:
http://karopka.ru/community/user/
http://karopka.ru/forum/

Options:
  -h --help                                      Show this screen.
  -d DESTINATION, --destination DESTINATION      Destination directory (otherwise current directory)
"""

import os
import sys
from docopt import docopt

import mfs.scrape as scrape

# Module that contains the command line app.
#
# Why does this file exist, and why not put this in __main__?
#
#   You might be tempted to import things from __main__ later, but that will cause
#   problems: the code will get executed twice:
#
#   - When you run `python -mmfs` python will execute
#     ``__main__.py`` as a script. That means there won't be any
#     ``mfs.__main__`` in ``sys.modules``.
#   - When you import __main__ it will get executed again (as a module) because
#     there's no ``mfs.__main__`` in ``sys.modules``.
#
#   Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration





def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """

    args = docopt(__doc__, argv=None, help=True, version=None, options_first=False)

    dest = args['--destination'] or os.getcwd()
    if not os.path.isdir(dest):
        raise ValueError("{} is not a directory".format(dest))
    url = args['URL']
    print(url)

    # karopka model overview ?
    # m = re.match('^http://karopka.ru/community/user/(.*)/\?MODEL=(.*)$', url)
    if url.startswith('http://karopka.ru/community/user/'):
        scrape.karopka_model_overview(url, dest)
    elif url.startswith('http://karopka.ru/forum/'):
        # Scrape karopka forum. URL starts from http://karopka.ru/forum/
        scrape.karopka_forum(url, dest)
    else:
        print ('Unrecognized url ...')

    print('Done')

    return 0
