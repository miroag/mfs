import pytest

from mfs.karopka import KaropkaForumScraper
from mfs.karopka import KaropkaModelScraper


def test_model_wrong_url():
    with pytest.raises(AttributeError):
        scraper = KaropkaModelScraper('very wrong url')  # noqa


def test_live_karopka_model():
    scraper = KaropkaModelScraper('http://karopka.ru/community/user/22051/?MODEL=464829').scan()

    assert scraper.title == 'Паровой буксир "Первый"'
    assert len(scraper.dl) == 10, 'Wrong number of files'


def test_forum_wrong_url():
    with pytest.raises(AttributeError):
        scraper = KaropkaForumScraper('wrong url')  # noqa


def test_live_karopka_forum_only_attachemnts():
    scraper = KaropkaForumScraper('http://karopka.ru/forum/messages/forum232/topic8294/message199483/#message199483',
                                  False).scan()

    assert scraper.title == 'Леерные ограждения своими руками, Приспособление для изготовления леерных ограждений'
    assert len(scraper.dl) == 13, 'Wrong number of files'


def test_live_karopka_forum_with_external_links():
    scraper = KaropkaForumScraper('http://karopka.ru/forum/forum263/topic15798/?PAGEN_1=30', follow=False).scan()
    assert len(scraper.dl) == 13, 'Wrong number of links'

    scraper = KaropkaForumScraper('http://karopka.ru/forum/forum263/topic15798/?PAGEN_1=29', follow=True).scan()
    assert len(scraper.dl) >= 35, 'Wrong number of links'
