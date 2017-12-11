import pytest

from mfs.airbase import AirbaseForumScraper


def test_model_wrong_url():
    with pytest.raises(AttributeError):
        scraper = AirbaseForumScraper('very wrong url')


def test_live_airbase_1():
    scraper = AirbaseForumScraper('http://forums.airbase.ru/2014/09/t67904--krejser-varyag-vremen-ryav.html',
                                  follow=False).scan()

    assert scraper.title == 'Крейсер" ВАРЯГ"  времен РЯВ'
    assert len(scraper.dl) == 23, 'Wrong number of links'


def test_live_airbase_2():
    scraper = AirbaseForumScraper('http://forums.airbase.ru/2009/07/t67904_3--krejser-varyag-vremen-ryav.html',
                                  follow=False).scan()

    assert scraper.title == 'Крейсер" ВАРЯГ"  времен РЯВ'
    assert len(scraper.dl) == 6, 'Wrong number of links'


def test_live_airbase_3():
    scraper = AirbaseForumScraper('http://forums.airbase.ru/2014/09/t67904--krejser-varyag-vremen-ryav.html',
                                      follow=True).scan()

    assert len(scraper.dl) >= 253, 'Wrong number of links'
