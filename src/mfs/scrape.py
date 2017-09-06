import bs4
import requests
import urllib.parse as urlp
import sys
import aiohttp

import pyprind

_KAROPKA = 'http://karopka.ru'

def download_images(dl):
    """
    Download all images in the passes download list
    :param dl: Download list of tuples (url, dest_fn)
    :return:
    """
    bar = pyprind.ProgBar(len(dl), title='Downloading images', stream=sys.stdout)

    for url, fn in dl:
        with open(fn, 'wb') as f:
            r = requests.get(url)
            f.write(r.content)
            bar.update()

def download_images2(dl):

    pass

def resolve_image_upload_site(url):
    """
    Resolves provided link to an image upload site to direct image link
    :param url:
    :param fn:
    :return: False if location not supported
    """

    # if url or hostname is empty - nothing to do
    if not url:
        return None
    o = urlp.urlparse(url)
    hn = o.hostname
    if not hn:
        return None
    # if the link is merely to main page, then there is likely nothing to do as well
    if len(o.path) < 3:
        return None

    # print('Resolve image link for {}'.format(url))

    hn = hn.replace('www.', '')
    # although following sites do contain images, we are not interested in them
    if hn in ['smayliki.ru', 'nick-name.ru']:
        return None
    if not hn in ['postimg.org', 'vfl.ru']:
        print('{} is not supported or not an image site link'.format(url))
        return None

    r = requests.get(url=url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    if hn == 'postimg.org':
        return _resolve_postimg(soup)

    if hn == 'vfl.ru':
        return _resolve_vfl(soup)

    return None


def _resolve_postimg(soup):
    src = soup.find(id='main-image').get('src')
    return src

def _resolve_vfl(soup):
    src = soup.find(id='f_image').find('img').get('src')

    # vfl likes to return relative to protocol path, like //vfl.ru/ ...
    if src.startswith('//'):
        src = 'http:' + src
    return src


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
        dl.append((_KAROPKA+img.get('data-full'), '{}/{:04d}.jpg'.format(dest, i)))

    print('Found {} images'.format(len(dl)))
    download_images(dl)
    return len(dl)


def karopka_forum(url, dest, follow=True):
    """
    Scrape karopka forum. URL starts from http://karopka.ru/forum/
    :param url:
    :param dest:
    :return:
    """
    # list of images to download
    dl = []

    r = requests.get(url=url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    # with open('d:/!/k.html', mode='w', encoding='utf-8') as f:
    #     f.write(soup.prettify(), )

    posts = soup.find_all('table', class_='forum-post-table')
    print('Found {} posts on page {}'.format(len(posts), url))

    # going through posts
    for post in posts:
        # finding the post number and converting it to int
        postnr = post.find('div', class_='forum-post-number').get_text()
        postnr = int(postnr.strip().replace('#', ''))

        # print('Post #{}'.format(postnr))
        post_entry = post.find('div', class_='forum-post-entry')

        # 1st supported image format, when image is directly attached to the post
        # In this case every image is wrapped into construction like
        # <div class='forum-attach>
        #   <img ../>
        #   ..
        #       <a href='link to download image'/>
        #  .. </div>
        # while it's tempting to download image directly, it's not a good idea since image may be of reduced size
        # and it's best to use download link to get the image
        attachments = post_entry.find_all('div', class_='forum-attach')
        for i, attachment in enumerate(attachments, 1):
            # print('Attachment #{}'.format(i))
            a = attachment.find('a', class_='forum-file')
            url = _KAROPKA+a.get('href')
            fn = a.find('span').get_text()
            fn = '{}/{:04d}-{:02d}-{}'.format(dest, postnr, i, fn)
            dl.append((url, fn))

        # 2nd class are the images uploaded to image sharing sites, like vfl.ru
        # it's inside the <a href='...> links
        links = post_entry.find_all('a')
        for i, link in enumerate(links):
            # within the link there shall be an image, otherwise this is just a normal link
            if link.find('img'):
                url = resolve_image_upload_site(link.get('href'))
                if url:
                    fn = '{}/{:04d}-{:02d}.jpg'.format(dest, postnr, i)
                    dl.append((url, fn))


    nimages = len(dl)
    print('Found {} images'.format(nimages))

    download_images(dl)

    print('Checking if next page is available ... ')
    next_page = soup.find('a', class_='forum-page-next')
    if next_page:
        nimages += karopka_forum(_KAROPKA+next_page.get('href'), dest)

    return nimages
