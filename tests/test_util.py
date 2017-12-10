import mfs.util as util


def test_n():
    assert util.n('//g.com') == 'http://g.com'
    assert util.n('http://g.com') == 'http://g.com'

def test_sluggify():
    assert util.sluggify('Good text') == 'Good text'
    assert util.sluggify('//Good text\\') == 'Good text'
    assert util.sluggify('-=Good_text=-') == '-=Good_text=-'
    assert util.sluggify('Хороший текст') == 'Хороший текст'
