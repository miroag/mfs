import os
import pytest
from mfs.base_scraper import BaseScraper

def test_scan():
    scraper = BaseScraper()
    with pytest.raises(NotImplementedError):
        scraper.scan('not implemented')


def test_save_use_title(tmpdir):
    # download list is empty
    scraper = BaseScraper()

    scraper.save(tmpdir.strpath, use_title=False)
    assert os.listdir(tmpdir.strpath) == [], 'No folders shall be created'

    scraper.save(tmpdir.strpath, use_title=True)
    assert os.listdir(tmpdir.strpath) == [scraper.title], 'Folder based on title shall be created'

    scraper.save(tmpdir.strpath, use_title=True)
    assert os.listdir(tmpdir.strpath) == [scraper.title], 'If folder already exist there shall be no issue'


def test_save(tmpdir):
    scraper = BaseScraper()

    nfiles = 2
    scraper.dl = [('http://httpbin.org/image/jpeg', '{:02d}.jpg'.format(i)) for i in range(nfiles)]
    dest = scraper.save(tmpdir.strpath)
    assert len(os.listdir(dest)) == nfiles, 'Wrong number of files'
