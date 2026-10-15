import unicodedata

from setuptools import unicode_utils


def test_filesys_decode_fs_encoding_is_None(monkeypatch):
    """
    Test filesys_decode does not raise TypeError when
    getfilesystemencoding returns None.
    """
    monkeypatch.setattr('sys.getfilesystemencoding', lambda: None)
    unicode_utils.filesys_decode(b'test')


def test_normalize():
    """
    normalize returns the NFC form for text and UTF-8 encoded bytes, and
    leaves bytes that are not UTF-8 untouched (GHSA-h35f-9h28-mq5c).
    """
    nfc = u'caf\xe9.txt'
    nfd = unicodedata.normalize('NFD', nfc)
    assert nfc != nfd
    assert unicode_utils.normalize(nfd) == nfc
    assert unicode_utils.normalize(nfc) == nfc
    assert unicode_utils.normalize(nfd.encode('utf-8')) == nfc.encode('utf-8')
    latin_1 = nfc.encode('latin-1')
    assert unicode_utils.normalize(latin_1) == latin_1
