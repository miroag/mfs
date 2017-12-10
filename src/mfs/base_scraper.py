import os

import mfs.util as util
from mfs.image_download import download_images

class BaseScraper:
    """
    Base scraper implements methods to resolve image links, as well as means to download resources.
    Derived class shall implement scan method to populate download list
    """

    def __init__(self):
        self.title = 'undefined'
        self.url = None
        self.dl = []

    def scan(self, url, follow):
        pass

    def save(self, dest, use_title=True):
        """
        save found images to destination location
        :param dest: folder where to store images
        :param use_title: use title to create subfolder in specified location
        :return: folder where the files were written
        """

        if use_title:
            dest = os.path.join(dest, util.sluggify(self.title))
            os.makedirs(dest, exist_ok=True)

        dl = [(url, os.path.join(dest, fn)) for (url, fn) in self.dl]
        download_images(dl)
        return dest

