import filecmp
import os

import mfs.image_download as base


def test_download_images(tmpdir):
    nfiles = 20
    dl = [('http://httpbin.org/image/jpeg', '{}/{:02d}.jpg'.format(tmpdir, i)) for i in range(nfiles)]
    base.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == nfiles, 'Wrong number of files'


def test_download_images_bad_links(tmpdir):
    # wrong encoding ?
    dl = [('http://www.wrk.ru/forums/attachment.php?item=83381', '{}/aaa.jpg'.format(tmpdir))]
    base.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == 0, 'No files shall be downloaded and no exception'

    # no site
    dl = [('http://www.suveniri-knigi.ru/index.php?kcena=220&kkorzina=3521', '{}/aaa.jpg'.format(tmpdir))]
    base.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == 0, 'No files shall be downloaded and no exception'

    # bad link
    dl = [('http://radikal.ru/lfp/s39.radikal.ru/i084/1106/a9/1fca250702b.jpg', '{}/aaa.jpg'.format(tmpdir))]
    base.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == 0, 'No files shall be downloaded and no exception'


def test_live_download_direct_link(tmpdir, testdata):
    fn = tmpdir.strpath + '/aaa.jpg'
    base.download_images([('http://s39.radikal.ru/i084/1106/a9/e1fca250702b.jpg', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
    assert filecmp.cmp(testdata.fn('radikal.ru.jpg'), fn,
                       shallow=False), 'Downloaded image does not match the reference one'


def test_reference_postimg(testdata):
    url = base._resolve_postimg(testdata.textdata('postimage.org.html'))
    assert url == 'https://s30.postimg.org/h38irt6r5/f618c175869a.jpg', \
        'Resolved postimg.org image link does not match'


def test_live_postimg(tmpdir, testdata):
    fn = tmpdir.strpath + '/aaa.jpg'
    base.download_images([('http://www.postimg.org/image/n467ovtd9/', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
    assert filecmp.cmp(testdata.fn('postimg.org.jpg'), fn, shallow=False), \
        'Downloaded image does not match the reference one'


def test_reference_vfl(testdata):
    url = base._resolve_vfl(testdata.textdata('vfl.ru.html'))
    assert url == 'http://images.vfl.ru/ii/1504336251/b2203fcd/18453338.jpg', \
        'Resolved vfl.ru image link does not match'


def test_live_vfl(tmpdir, testdata):
    fn = tmpdir.strpath + '/aaa.jpg'
    base.download_images([('http://vfl.ru/fotos/b2203fcd18453338.html', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
    assert filecmp.cmp(testdata.fn('vfl.ru.jpg'), fn,
                       shallow=False), 'Downloaded image does not match the reference one'


def test_live_vfl_2020(tmpdir, testdata):
    fn = tmpdir.strpath + '/aaa.jpg'
    base.download_images([('http://vfl.ru/fotos/9b930dc417050203.html', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'


def test_reference_radikal(testdata):
    url = base._resolve_radikal(testdata.textdata('radikal.ru.html'))
    assert url == 'http://s39.radikal.ru/i084/1106/a9/e1fca250702b.jpg', \
        'Resolved radikal.ru image link does not match'


def test_live_radikal(tmpdir, testdata):
    fn = tmpdir.strpath + '/aaa.jpg'
    base.download_images([('http://radikal.ru/F/s39.radikal.ru/i084/1106/a9/e1fca250702b.jpg.html', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
    assert filecmp.cmp(testdata.fn('radikal.ru.jpg'), fn,
                       shallow=False), 'Downloaded image does not match the reference one'


def test_resolve_keep4u(testdata):
    url = base._resolve_keep4u(testdata.textdata('keep4u.ru.html'))
    assert url == 'http://static2.keep4u.ru/2011/05/13/486422e15f82de157a64237a9627892e.jpg', \
        'Resolved radikal.ru image link does not match'


def test_keep4u(tmpdir, testdata):
    fn = tmpdir.strpath + '/aaa.jpg'
    base.download_images([('http://keep4u.ru/full/486422e15f82de157a64237a9627892e.html', fn)])
    assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
    assert filecmp.cmp(testdata.fn('keep4u.ru.jpg'), fn,
                       shallow=False), 'Downloaded image does not match the reference one'
