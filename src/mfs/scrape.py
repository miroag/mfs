import bs4
import requests
import urllib.parse as urlp
import sys
import aiohttp
import asyncio
import tqdm

_KAROPKA = 'http://karopka.ru'

def download_images(dl):
    # avoid to many requests(coroutines) the same time.
    # limit them by setting semaphores (simultaneous requests)
    _sema = asyncio.Semaphore(10)

    async def wait_with_progressbar(coros):
        for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
            await f

    async def download_file(url, fn):
        async with _sema, aiohttp.ClientSession() as session:
            resolved_url = await resolve_image_link(url)
            if resolved_url:
                async with session.get(resolved_url) as resp:
                    if resp.status == 200:
                        with open(fn, 'wb') as f:
                            # print('Downloaded file {}'.format(fn))
                            f.write(await resp.read())

    ioloop = asyncio.get_event_loop()
    tasks = [download_file(url, fn) for url, fn in dl]
    # wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_with_progressbar(tasks))
    # do not close the loop here - it will be closed at program exit
    return


async def resolve_image_link(url):
    """
    Resolves provided link to an image upload site to direct image link
    :param url:
    :param fn:
    :return: None if location not supported, or direct download link
    """

    # if url or hostname is empty - nothing to do
    if not url:
        return None

    # if link points to an image, just return it back
    if url.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']:
        return url

    o = urlp.urlparse(url)
    hn = o.hostname
    if not hn:
        return None
    # if the link is merely to main page, then there is likely nothing to do as well
    if len(o.path) < 3:
        return None

    # keep only last two parts of the hostname. eg www.radikal.ru => radikal.ru; radikal.ru => radikal.ru
    hn = '.'.join(hn.split('.')[-2:])

    # bypass sites
    if hn in ['httpbin.org', 'karopka.ru']:
        return url

    # although following sites do contain images, we are not interested in them
    if hn in ['smayliki.ru', 'nick-name.ru']:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()

    if hn in ['postimg.org', 'postimage.org']:
        return _resolve_postimg(text)
    if hn == 'vfl.ru':
        return _resolve_vfl(text)
    if hn == 'radikal.ru':
        return _resolve_radikal(text)
    if hn == 'keep4u.ru':
        return _resolve_keep4u(text)

    print('{} is not supported or not an image site link'.format(url))
    return None


def _resolve_postimg(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    src = soup.find(id='main-image').get('src')
    return src

def _resolve_vfl(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    src = soup.find(id='f_image').find('img').get('src')

    # vfl likes to return relative to protocol path, like //vfl.ru/ ...
    if src.startswith('//'):
        src = 'http:' + src
    return src

def _resolve_radikal(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    e = soup.find('div', class_='mainBlock')
    if not e:
        return None

    src = e.find('img').get('src')

    # vfl likes to return relative to protocol path, like //vfl.ru/ ...
    if src.startswith('//'):
        src = 'http:' + src
    return src

def _resolve_keep4u(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    e = soup.find(id ='image-viewer')
    if not e:
        return None

    src = e.find('img').get('src')

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
    return dl


def karopka_forum(url, dest, follow=True):
    """
    Scrape karopka forum. URL starts from http://karopka.ru/forum/
    :param url:
    :param dest:
    :return:
    """
    def _karopka_forum(url, dest, follow=True):
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
                url = _KAROPKA+a.get('href')
                fn = a.find('span').get_text()
                fn = '{}/{:04d}-a{:02d}-{}'.format(dest, postnr, i, fn)
                dl.append((url, fn))

            # 2nd class are the images uploaded to image sharing sites, like vfl.ru
            links = post.find('div', class_='forum-post-text').find_all('a')
            for i, link in enumerate(links, 1):
                # within the link there shall be an image, otherwise this is just a normal link
                if link.find('img'):
                    url = link.get('href')
                    if url:
                        fn = '{}/{:04d}-l{:02d}.jpg'.format(dest, postnr, i)
                        dl.append((url, fn))


        print('Found {} potential image links'.format(len(dl)))

        if follow:
            print('Checking if next page is available ... ')
            next_page = soup.find('a', class_='forum-page-next')
            if next_page:
                dl += _karopka_forum(_KAROPKA+next_page.get('href'), dest)

        return dl

    dl = _karopka_forum(url=url, dest=dest, follow=follow)
    download_images(dl)
    return dl
