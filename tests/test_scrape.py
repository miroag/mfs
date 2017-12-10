"""
Set of tests
"""

import os
import pytest
import filecmp

import mfs.scrape as scrape



@pytest.fixture
def mock_image_download(monkeypatch):
    # mock image download part and return immediately the number of files requested to download
    def mocked_return(dl):
        return len(dl)

    monkeypatch.setattr(scrape, 'download_images', mocked_return)




def test_navsource(tmpdir, mock_image_download):
    dl = scrape.navsource('http://www.navsource.narod.ru/photos/02/020/index.html', tmpdir)
    assert len(dl) == 56, 'Wrong number of links'


def test_airbase(mock_image_download, tmpdir):
    dl = scrape.airbase_forum('http://forums.airbase.ru/2014/09/t67904--krejser-varyag-vremen-ryav.html', tmpdir,
                              follow=False)
    assert len(dl) == 23, 'Wrong number of links'

    # another one for 3rd class of links
    dl = scrape.airbase_forum('http://forums.airbase.ru/2009/07/t67904_3--krejser-varyag-vremen-ryav.html', tmpdir,
                              follow=False)
    assert len(dl) == 6, 'Wrong number of links'

    dl = scrape.airbase_forum('http://forums.airbase.ru/2014/09/t67904--krejser-varyag-vremen-ryav.html', tmpdir,
                              follow=True)
    assert len(dl) >= 253, 'Wrong number of links'


