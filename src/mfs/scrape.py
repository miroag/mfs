import bs4
import requests
import datetime

# import dateutil.parser

from mfs.base_scraper import *






def navsource(url, dest):
    """
    Scrape photos from http://www.navsource.narod.ru/ source
    Args:
        url:
        dest:

    Returns:

    """
    dl = []
    urlparts = url.split('/')

    r = requests.get(url=url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    for row in soup.find_all('tr'):
        # while there are many tables numbering is going through tables - use it
        tds = row.find_all('td')
        if len(tds) < 4:
            continue

        i = int(tds[0].text.strip().replace('.', ''))

        urlparts[-1] = tds[1].find('a').get('href')
        src = '/'.join(urlparts)
        des = _sluggify(tds[3].text.replace('(подробнее)', '').strip())

        dl.append((src, '{}/navsource-{:04d} - {}.jpg'.format(dest, i, des)))

    print('Found {} images'.format(len(dl)))
    download_images(dl)
    return dl


def airbase_forum(url, dest, follow=True):
    """
    Scrape airbase.ru forum. URL starts from http://forums.airbase.ru
    :param url:
    :param dest:
    :return:
    """

    def _airbase_forum(url, dest, follow=True):
        # list of images to download
        dl = []

        r = requests.get(url=url)
        r.raise_for_status()
        # force encoding into utf-8 as sometimes airbase comes back in 'ISO-8859-1'
        r.encoding = 'utf-8'
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        posts = soup.find_all('div', class_='post')
        print('Found {} posts on page {}'.format(len(posts), url))

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
                src = _n(a.get('href'))
                # description looks like rubbish for russian text - encoding issues ....
                des = _sluggify(a.get('title'))
                fn = '{}/{}-a{:02d}-{}'.format(dest, postnr, i, des)
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
                            fn = '{}/{}-l{:02d}.jpg'.format(dest, postnr, i)
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
                            fn = '{}/{}-l{:02d}.jpg'.format(dest, postnr, i)
                            dl.append((src, fn))

        print('Found {} potential image links'.format(len(dl)))

        if follow:
            print('Checking if next page is available ... ')
            next_page = soup.find('a', class_='current_page').find_next('a')
            if next_page:
                src = next_page.get('href')
                if src:
                    dl += _airbase_forum(_n(src), dest, follow)

        return dl

    dl = _airbase_forum(url=url, dest=dest, follow=follow)
    download_images(dl)
    return dl
