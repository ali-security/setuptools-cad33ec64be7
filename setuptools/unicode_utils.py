import unicodedata
import sys

from setuptools.extern import six


# HFS Plus uses decomposed UTF-8
def decompose(path):
    if isinstance(path, six.text_type):
        return unicodedata.normalize('NFD', path)
    try:
        path = path.decode('utf-8')
        path = unicodedata.normalize('NFD', path)
        path = path.encode('utf-8')
    except UnicodeError:
        pass  # Not UTF-8
    return path


def normalize(text):
    """
    Return *text* in a canonical Unicode form (NFC) so that names which are
    visually identical but encoded differently compare equal.

    macOS APFS/HFS+ store file names in decomposed form (NFD), while patterns
    in ``MANIFEST.in`` are typically authored composed (NFC). The two denote
    the same file but differ byte-for-byte, so matching them directly lets an
    exclusion silently fail. Normalizing both the walked path and the pattern
    to a single form before matching avoids that (GHSA-h35f-9h28-mq5c).

    Byte strings (as produced on Python 2) are normalized as UTF-8 and
    returned as bytes; anything that is not UTF-8 is returned unchanged.
    """
    if isinstance(text, six.text_type):
        return unicodedata.normalize('NFC', text)
    if isinstance(text, six.binary_type):
        try:
            decoded = text.decode('utf-8')
        except UnicodeError:
            return text  # Not UTF-8
        return unicodedata.normalize('NFC', decoded).encode('utf-8')
    return text


def filesys_decode(path):
    """
    Ensure that the given path is decoded,
    NONE when no expected encoding works
    """

    if isinstance(path, six.text_type):
        return path

    fs_enc = sys.getfilesystemencoding() or 'utf-8'
    candidates = fs_enc, 'utf-8'

    for enc in candidates:
        try:
            return path.decode(enc)
        except UnicodeDecodeError:
            continue


def try_encode(string, enc):
    "turn unicode encoding into a functional routine"
    try:
        return string.encode(enc)
    except UnicodeEncodeError:
        return None
