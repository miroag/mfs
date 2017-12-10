import pytest

from mfs.karopka import KaropkaModelOverviewScraper


def test_model_overview_wrong_url():
    scraper = KaropkaModelOverviewScraper()
    with pytest.raises(AttributeError):
        scraper.scan('very wrong url')


def test_live_karopka_model_overview():
    scraper = KaropkaModelOverviewScraper()
    scraper.scan('http://karopka.ru/community/user/22051/?MODEL=464829')
    assert scraper.title == 'Паровой буксир "Первый"'
    assert len(scraper.dl) == 10, 'Wrong number of files'
