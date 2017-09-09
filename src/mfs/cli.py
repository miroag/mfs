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


def main(argv=sys.argv):
    args = docopt(__doc__, argv=None, help=True, version=None, options_first=False)

    dest = args['--destination'] or os.getcwd()
    if not os.path.isdir(dest):
        raise ValueError("{} is not a directory".format(dest))
    url = args['URL']
    print('Processing {}'.format(url))

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
