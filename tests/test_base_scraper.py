import os
import pytest
from mfs.base_scraper import BaseScraper


def test_scan():
    scraper = BaseScraper('')
    with pytest.raises(NotImplementedError):
        scraper.scan()


def test_save_use_title(tmpdir):
    # download list is empty
    scraper = BaseScraper('')

    scraper.save(tmpdir.strpath, use_title=False, write_url_file=False)
    assert os.listdir(tmpdir.strpath) == [], 'No folders shall be created'

    scraper.save(tmpdir.strpath, use_title=True, write_url_file=False)
    assert os.listdir(tmpdir.strpath) == [scraper.title], 'Folder based on title shall be created'

    scraper.save(tmpdir.strpath, use_title=True, write_url_file=False)
    assert os.listdir(tmpdir.strpath) == [scraper.title], 'If folder already exist there shall be no issue'


def test_save(tmpdir):
    scraper = BaseScraper('')

    nfiles = 2
    scraper.dl = [('http://httpbin.org/image/jpeg', '{:02d}.jpg'.format(i)) for i in range(nfiles)]
    dest = scraper.save(tmpdir.strpath)

    url_files = [fn for fn in os.listdir(dest) if fn.endswith('.url')]
    assert len(url_files) == 1, 'There shall be one url file'

    assert len(os.listdir(dest)) == nfiles + 1, 'Wrong number of files'

