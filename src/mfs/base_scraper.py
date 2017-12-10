import bs4
import urllib.parse as urlp
import aiohttp
import asyncio
import tqdm
import requests

class BaseScraper:

    def __init__(self):
        self.url = None
        self.title = 'undefined'
        self.dl = []


    def scrape(self, url, follow):
        pass

    def save(self, dest):
        pass



def _n(src):
    if src.startswith('//'):
        src = 'http:' + src
    return src


def _sluggify(text):
    if not text:
        return ''
    return ''.join([c for c in text if c.isalpha() or c.isdigit() or c in [' ', '.', '_', '-']]).rstrip()


def download_images(dl):
    # avoid to many requests(coroutines) the same time.
    # limit them by setting semaphores (simultaneous requests)
    _sema = asyncio.Semaphore(10)

    async def wait_with_progressbar(coros):
        for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
            await f

    async def download_file(url, fn):
        try:
            async with _sema, aiohttp.ClientSession() as session:
                resolved_url = await resolve_image_link(url)
                if resolved_url:
                    async with session.get(resolved_url) as resp:
                        if resp.status == 200:
                            with open(fn, 'wb') as f:
                                # print('Downloaded file {}'.format(fn))
                                f.write(await resp.read())
        except Exception:
            print('Download of {} failed'.format(url))

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
    if hn in ['smayliki.ru', 'nick-name.ru', 'suveniri-knigi.ru', 'narod.ru', 'wrk.ru', 'aceboard.net']:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                text = await resp.text()
            else:
                print('{} returned {}'.format(url, resp.status))

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
    e = soup.find(id='f_image')
    if not e:
        return None

    return _n(e.find('img').get('src'))


def _resolve_radikal(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    e = soup.find('div', class_='mainBlock')
    if not e:
        return None

    return _n(e.find('img').get('src'))


def _resolve_keep4u(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    e = soup.find(id='image-viewer')
    if not e:
        return None

    return _n(e.find('img').get('src'))


