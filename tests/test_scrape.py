"""
Set of tests
"""

import os
import pytest
import filecmp

import src.mfs.scrape as scrape
import mfs.cli as cli

REFDATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

def _refdata(fn):
    with open('./data/{}'.format(fn), encoding='utf8') as f:
        return f.read()


def test_resolve_postimg():
    url = scrape._resolve_postimg(_refdata('postimage.org.html'))
    assert url == 'https://s30.postimg.org/h38irt6r5/f618c175869a.jpg',\
        'Resolved postimg.org image link does not match'

def test_postimg(tmpdir):
    fn = tmpdir.strpath + '/aaa.jpg'
    scrape.download_images([('http://www.postimg.org/image/n467ovtd9/', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
    assert filecmp.cmp('./data/postimg.org.jpg', fn, shallow=False), 'Downloaded image does not match the reference one'

def test_resolve_vfl():
    url = url = scrape._resolve_vfl(_refdata('vfl.ru.html'))
    assert url=='http://images.vfl.ru/ii/1504336251/b2203fcd/18453338.jpg',\
        'Resolved vfl.ru image link does not match'


def test_vfl(tmpdir):
    fn = tmpdir.strpath + '/aaa.jpg'
    scrape.download_images([('http://vfl.ru/fotos/b2203fcd18453338.html', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
    assert filecmp.cmp('./data/vfl.ru.jpg', fn, shallow=False), 'Downloaded image does not match the reference one'

@pytest.fixture
def mock_image_download(monkeypatch):
    # mock image download part and return immediately the number of files requested to download
    def mocked_return(dl):
        return len(dl)
    monkeypatch.setattr(scrape, 'download_images', mocked_return)


def test_karopka_model_overview(mock_image_download, tmpdir):
    dl = scrape.karopka_model_overview('http://karopka.ru/community/user/22051/?MODEL=464829', tmpdir)
    assert len(dl)== 10, 'Wrong number of files'


def test_karopka_forum_only_attachemnts(mock_image_download, tmpdir):
    # monkeypatch.setattr('mfs.scrape.download_images', image_download_mock)
    dl = scrape.karopka_forum('http://karopka.ru/forum/messages/forum232/topic8294/message199483/#message199483', tmpdir)
    assert len(dl) == 13, 'Wrong number of links'

def test_karopka_forum_with_external_links(mock_image_download, tmpdir):
    dl = scrape.karopka_forum('http://karopka.ru/forum/forum263/topic15798/?PAGEN_1=30', tmpdir, follow=False)
    assert len(dl) == 13, 'Wrong number of links'

    dl = scrape.karopka_forum('http://karopka.ru/forum/forum263/topic15798/?PAGEN_1=29', tmpdir, follow=True)
    assert len(dl) == 35, 'Wrong number of links'


def test_download_images(tmpdir):
    nfiles = 20
    dl = [('http://httpbin.org/image/jpeg', '{}/{:02d}.jpg'.format(tmpdir, i)) for i in range(nfiles)]
    scrape.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == nfiles, 'Wrong number of files'
