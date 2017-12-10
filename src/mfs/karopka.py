import bs4
import requests

from mfs.base_scraper import BaseScraper

_KAROPKA = 'http://karopka.ru'


class KaropkaModelOverviewScraper(BaseScraper):
    """
    Scrape karopka model overview. URL is in the form of http://karopka.ru/community/user/<user_id>/?MODEL=<model_id>
    """

    def scan(self, url, follow=True):
        if not url.startswith('http://karopka.ru/community/'):
            raise AttributeError('URL shall start from http://karopka.ru/community/')

        self.dl = []

        r = requests.get(url=url)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        self.title = soup.find('h1').text

        fotorama = soup.find('div', class_='fotorama')
        imgs = fotorama.find_all('img')

        # prepare the list of images to download. Original (not rescaled) images apparently stored in data-full attribute
        for i, img in enumerate(imgs, 1):
            self.dl.append((_KAROPKA + img.get('data-full'), '{:04d}.jpg'.format(i)))

        return len(self.dl)
