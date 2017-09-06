"""
Set of tests
"""

import os

import pytest

import src.mfs.scrape as scrape

REFDATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def test_unsupported():
    assert scrape.resolve_image_upload_site('http://www.notsupported.com') == None, \
        'Shall return None for unsupported links'
    pass

def test_postimg():
    url = scrape.resolve_image_upload_site('http://www.postimg.org/image/n467ovtd9/')
    assert url == 'https://s30.postimg.org/h38irt6r5/f618c175869a.jpg',\
        'Resolved postimg.org image link does not match'

def test_vfl():
    url = scrape.resolve_image_upload_site('http://vfl.ru/fotos/b2203fcd18453338.html')
    assert url=='http://images.vfl.ru/ii/1504336251/b2203fcd/18453338.jpg',\
        'Resolved vfl.ru image link does not match'

@pytest.fixture
def mock_image_download(monkeypatch):
    # mock image download part and return immediately the number of files requested to download
    def mocked_return(dl):
        return len(dl)
    monkeypatch.setattr(scrape, 'download_images', mocked_return)

def test_karopka_model_overview(mock_image_download):
    nimages = scrape.karopka_model_overview('http://karopka.ru/community/user/22051/?MODEL=464829', 'c:/temp/')
    assert nimages == 10, 'Wrong number of files'


def test_karopka_forum_only_attachemnts(mock_image_download):
    # monkeypatch.setattr('mfs.scrape.download_images', image_download_mock)
    nimages = scrape.karopka_forum('http://karopka.ru/forum/messages/forum232/topic8294/message199483/#message199483', 'c:/temp/')
    assert nimages == 13, 'Wrong number of files'

def test_karopka_forum_with_vfl(mock_image_download):
    nimages = scrape.karopka_forum('http://karopka.ru/forum/forum263/topic15798/?PAGEN_1=30', 'c:/temp/')
    assert nimages == 13, 'Wrong number of files'

# TODO: replace fixed local file with some http fixtures
@pytest.mark.webtest
def test_download_images(tmpdir):
    nfiles = 20
    dl = [('http://localhost:8080/1.jpg', '{}/{:02d}.jpg'.format(tmpdir, i)) for i in range(nfiles)]
    scrape.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == nfiles, 'Wrong number of files'

