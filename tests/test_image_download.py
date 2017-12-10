import os
import mfs.image_download as base


def test_resolve_postimg(testdata):
    url = base._resolve_postimg(testdata.textdata('postimage.org.html'))
    assert url == 'https://s30.postimg.org/h38irt6r5/f618c175869a.jpg', \
        'Resolved postimg.org image link does not match'


# def test_postimg(tmpdir):
#     fn = tmpdir.strpath + '/aaa.jpg'
#     scrape.download_images([('http://www.postimg.org/image/n467ovtd9/', fn)])
#     assert len(os.listdir(tmpdir.strpath)) == 1, 'One images shall be downloaded'
#     assert filecmp.cmp(_reffn('postimg.org.jpg'), fn,
#                        shallow=False), 'Downloaded image does not match the reference one'
#


def test_save_download_images(tmpdir):
    nfiles = 20
    dl = [('http://httpbin.org/image/jpeg', '{}/{:02d}.jpg'.format(tmpdir, i)) for i in range(nfiles)]
    base.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == nfiles, 'Wrong number of files'


def test_save_download_images_bad_links(tmpdir):
    # wrong encoding ?
    dl = [('http://www.wrk.ru/forums/attachment.php?item=83381', '{}/aaa.jpg'.format(tmpdir))]
    base.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == 0, 'No files shall be downloaded and no exception'

    # no site
    dl = [('http://www.suveniri-knigi.ru/index.php?kcena=220&kkorzina=3521', '{}/aaa.jpg'.format(tmpdir))]
    base.download_images(dl)
    assert len(os.listdir(tmpdir.strpath)) == 0, 'No files shall be downloaded and no exception'
