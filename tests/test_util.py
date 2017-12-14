import pytest

import mfs.util as util


def test_n():
    assert util.n('//g.com') == 'http://g.com'
    assert util.n('http://g.com') == 'http://g.com'


def test_sluggify():
    assert util.sluggify('Good text') == 'Good text'
    assert util.sluggify('//Good text\\') == 'Good text'
    assert util.sluggify('-=Good_text=-') == '-=Good_text=-'
    assert util.sluggify('Хороший текст') == 'Хороший текст'


def test_soup():
    assert util.soup('http://google.com') is not None

    with pytest.raises(Exception):
        util.soup('shall fail')

    with pytest.raises(Exception):
        util.soup('http://httpbin.org/status/500')
