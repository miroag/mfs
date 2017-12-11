import datetime

from mfs.base_scraper import BaseScraper
import mfs.util as util


class AirbaseForumScraper(BaseScraper):
    """
    Scrape karopka forum. URL is in the form of http://karopka.ru/forum/
    """

    def __init__(self, url, follow=True):
        if not url.startswith('http://forums.airbase.ru'):
            raise AttributeError('URL shall start from http://forums.airbase.ru')
        super().__init__(url, follow)

    def _scan_forum_page(self, soup, follow=True):
        # list of images to download
        dl = []

        posts = soup.find_all('div', class_='post')
        print('Found {} posts on page {}'.format(len(posts), soup.title.text.strip()))

        # going through posts
        for post in posts:
            # finding the post date (there is no post number on airbase)
            e = post.find('div', class_='to-left')
            # posts with non present to-left is advertisement
            if not e:
                continue

            postnr = e.find('a').text
            # post date is in form: "#12.07.2009 12:33" - normalize to allow good sorting order
            dt = datetime.datetime.strptime(postnr.strip().replace('#', ''), '%d.%m.%Y %H:%M')
            # dt = dateutil.parser.parse(postnr.strip().replace('#', ''))
            postnr = dt.strftime('airbase%Y-%m-%d-%H%M')
            # print(postnr)

            # 1st supported image format, when image is directly attached to the post
            attachments = post.find_all('div', class_='attach-desc')
            for i, attachment in enumerate(attachments, 1):
                # print('Attachment #{}'.format(i))
                # there are two links in each attachment - first gives the image second description
                a = attachment.find('a')
                src = util.n(a.get('href'))
                # description looks like rubbish for russian text - encoding issues ....
                des = util.sluggify(a.get('title'))
                fn = '{}-a{:02d}-{}'.format(postnr, i, des)
                dl.append((src, fn))

            # 2nd class are the images uploaded to image sharing sites, like vfl.ru
            links = post.find_all('div', class_='rs_box_nd')
            for i, link in enumerate(links, 1):
                # within the link there shall be an image, otherwise this is just a normal link
                if link.find('img'):
                    # sometimes bloody airbase will miss the a as well
                    if link.find('a'):
                        src = link.find('a').get('href')
                        if src:
                            fn = '{}-l{:02d}.jpg'.format(postnr, i)
                            dl.append((src, fn))

            # 3rd class are the images uploaded to image sharing sites, like vfl.ru
            links = post.find_all('div', class_='rs_box')
            for i, link in enumerate(links, 1):
                # within the link there shall be an image, otherwise this is just a normal link
                if link.find('img'):
                    # sometimes bloody airbase will miss the a as well
                    if link.find('a'):
                        src = link.find('a').get('href')
                        if src:
                            fn = '{}-l{:02d}.jpg'.format(postnr, i)
                            dl.append((src, fn))

        print('Found {} potential image links'.format(len(dl)))

        if follow:
            print('Checking if next page is available ... ')
            next_page = soup.find('a', class_='current_page').find_next('a')
            if next_page:
                src = next_page.get('href')
                if src:
                    dl += self._scan_forum_page(util.soup(util.n(src)), follow)

        return dl

    def scan(self):
        soup = util.soup(self.url)

        self.title = soup.find('h1').text.strip()
        self.dl = self._scan_forum_page(soup=soup, follow=self.follow)

        return self
