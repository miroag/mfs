import bs4
import requests

from mfs.base_scraper import BaseScraper
import mfs.util as util

_KAROPKA = 'http://karopka.ru'


class KaropkaModelScraper(BaseScraper):
    """
    Scrape karopka model overview. URL is in the form of http://karopka.ru/community/user/<user_id>/?MODEL=<model_id>
    """

    def __init__(self, url, follow=True):
        if not url.startswith('http://karopka.ru/community/'):
            raise AttributeError('URL shall start from http://karopka.ru/community/')
        super().__init__(url, follow)

    def scan(self):
        soup = util.soup(self.url)

        self.title = soup.find('h1').text

        fotorama = soup.find('div', class_='fotorama')
        imgs = fotorama.find_all('img')

        # prepare the list of images to download. Original (not rescaled) images apparently stored in data-full attribute
        for i, img in enumerate(imgs, 1):
            self.dl.append((_KAROPKA + img.get('data-full'), '{:04d}.jpg'.format(i)))

        return self


class KaropkaForumScraper(BaseScraper):
    """
    Scrape karopka forum. URL is in the form of http://karopka.ru/forum/
    """

    def __init__(self, url, follow=True):
        if not url.startswith('http://karopka.ru/forum/'):
            raise AttributeError('URL shall start from http://karopka.ru/forum/')
        super().__init__(url, follow)

    def _scan_forum_page(self, soup, follow=True):
        # list of images to download
        dl = []

        # with open('d:/!/k.html', mode='w', encoding='utf-8') as f:
        #     f.write(soup.prettify(), )

        posts = soup.find_all('table', class_='forum-post-table')
        print('Found {} posts on the page'.format(len(posts)))

        # going through posts
        for post in posts:
            # finding the post number and converting it to int
            postnr = post.find('div', class_='forum-post-number').get_text()
            postnr = int(postnr.strip().replace('#', ''))

            # 1st supported image format, when image is directly attached to the post
            # In this case every image is wrapped into construction like
            # <div class='forum-attach>
            #   <img ../>
            #   ..
            #       <a href='link to download image'/>
            #  .. </div>
            # while it's tempting to download image directly, it's not a good idea since image may be of reduced size
            # and it's best to use download link to get the image
            attachments = post.find_all('div', class_='forum-attach')
            for i, attachment in enumerate(attachments, 1):
                # print('Attachment #{}'.format(i))
                a = attachment.find('a', class_='forum-file')
                url = _KAROPKA + a.get('href')
                fn = a.find('span').get_text()
                fn = 'karopka{:04d}-a{:02d}-{}'.format(postnr, i, fn)
                dl.append((url, fn))

            # 2nd class are the images uploaded to image sharing sites, like vfl.ru
            links = post.find('div', class_='forum-post-text').find_all('a')
            for i, link in enumerate(links, 1):
                # within the link there shall be an image, otherwise this is just a normal link
                if link.find('img'):
                    url = link.get('href')
                    if url:
                        fn = 'karopka{:04d}-l{:02d}.jpg'.format(postnr, i)
                        dl.append((url, fn))

        print('Found {} potential image links'.format(len(dl)))

        if follow:
            print('Checking if next page is available ... ')
            next_page = soup.find('a', class_='forum-page-next')
            if next_page:
                dl += self._scan_forum_page(util.soup(_KAROPKA + next_page.get('href')))

        return dl

    def scan(self):
        soup = util.soup(self.url)

        self.title = soup.find('div', class_='forum-header-title').text.strip()
        self.dl = self._scan_forum_page(soup=soup, follow=self.follow)

        return self
