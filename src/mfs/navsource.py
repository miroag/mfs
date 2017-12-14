import mfs.util as util
from mfs.base_scraper import BaseScraper


class NavSourceScraper(BaseScraper):
    """
    Scrape karopka model overview. URL is in the form of http://karopka.ru/community/user/<user_id>/?MODEL=<model_id>
    """

    def __init__(self, url, follow=True):
        if not url.startswith('http://www.navsource.narod.ru'):
            raise AttributeError('URL shall start from http://www.navsource.narod.ru')
        super().__init__(url, follow)

    def scan(self):
        soup = util.soup(self.url)

        self.title = soup.find('h3', class_='caption').text.strip()

        urlparts = self.url.split('/')
        for row in soup.find_all('tr'):
            # while there are many tables numbering is going through tables - use it
            tds = row.find_all('td')
            if len(tds) < 4:
                continue

            i = int(tds[0].text.strip().replace('.', ''))

            urlparts[-1] = tds[1].find('a').get('href')
            src = '/'.join(urlparts)
            des = util.sluggify(tds[3].text.replace('(подробнее)', '').strip())

            self.dl.append((src, 'navsource-{:04d} - {}.jpg'.format(i, des)))

        return self
