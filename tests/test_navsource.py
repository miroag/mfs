import pytest

from mfs.navsource import NavSourceScraper


def test_model_wrong_url():
    with pytest.raises(AttributeError):
        scraper = NavSourceScraper('very wrong url')


def test_live_navsource():
    scraper = NavSourceScraper('http://www.navsource.narod.ru/photos/02/020/index.html').scan()

    assert scraper.title == 'Бронепалубный крейсер "Варяг"'
    assert len(scraper.dl) == 56, 'Wrong number of files'

