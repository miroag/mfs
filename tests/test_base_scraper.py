import os
from mfs.base_scraper import BaseScraper


def test_save_use_title(tmpdir):
    # download list is empty
    scrape = BaseScraper()

    scrape.save(tmpdir.strpath, use_title=False)
    assert os.listdir(tmpdir.strpath) == [], 'No folders shall be created'

    scrape.save(tmpdir.strpath, use_title=True)
    assert os.listdir(tmpdir.strpath) == [scrape.title], 'Folder based on title shall be created'

    scrape.save(tmpdir.strpath, use_title=True)
    assert os.listdir(tmpdir.strpath) == [scrape.title], 'If folder already exist there shall be no issue'


def test_save(tmpdir):
    scrape = BaseScraper()

    nfiles = 2
    scrape.dl = [('http://httpbin.org/image/jpeg', '{:02d}.jpg'.format(i)) for i in range(nfiles)]
    dest = scrape.save(tmpdir.strpath)
    assert len(os.listdir(dest)) == nfiles, 'Wrong number of files'
