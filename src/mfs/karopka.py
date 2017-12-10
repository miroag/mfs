import bs4
import requests

from mfs.base_scraper import BaseScraper

_KAROPKA = 'http://karopka.ru'


class KaropkaModelOverviewScraper(BaseScraper):
    """
    Scrape karopka model overview. URL is in the form of http://karopka.ru/community/user/<user_id>/?MODEL=<model_id>
    """

    def scan(self, url, follow):
        pass


def karopka_model_overview(url, dest):
    """
    Scrape karopka model overview. URL is in the form of http://karopka.ru/community/user/<user_id>/?MODEL=<model_id>
    :param url:
    :param dest:
    :return:
    """
    r = requests.get(url=url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    # with open('d:/!/k.html', mode='w', encoding='utf-8') as f:
    #     f.write(soup.prettify(), )

    fotorama = soup.find('div', class_='fotorama')
    imgs = fotorama.find_all('img')

    # prepare the list of images to download. Original (not rescaled) images apparently stored in data-full attribute
    dl = []
    for i, img in enumerate(imgs, 1):
        dl.append((_KAROPKA + img.get('data-full'), '{}/{:04d}.jpg'.format(dest, i)))

    print('Found {} images'.format(len(dl)))
    download_images(dl)
    return dl
