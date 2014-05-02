from __future__ import division, with_statement, print_function, unicode_literals

import io
import locale

class NullTextFile(io.TextIOBase):
    '''Text file that writes to no where

Useful for passing a dummy file to callables that require one.'''
    def read(self, n):
        return ''
    def readline(self, limit):
        return ''
    def write(self, s):
        return len(s)
    def readable(self):
        return True
    def writable(self):
        return True

class NullFile(io.RawIOBase):
    '''Binary file that writes to no where

Useful for passing a dummy file to callables that require one.'''
    def read(self, n=-1):
        return b''
    def write(self, b):
        return len(b)
    def readable(self):
        return True
    def writable(self):
        return True

class UnicodeIOWrapper(io.TextIOWrapper):
    '''Quietly converts bytes objects to unicode strings

The regular io.TextIOWrapper object will refuse to accept anything other than
unicode objects. This class is a bit more convenient since some py2k classes
have methods that don't work properly with the rigid behavior of the
TextIOWrapper class. All other non-string objects will still cause an
TypeError to be raised, however.'''
    def __init__(self, file, mode='r', encoding=None, errors=None, 
        newlines=None, bytes_encoding=None):
        
        if mode != 'r' and mode != 'r+' and mode != 'w' and mode != 'w+':
            raise ValueError('Mode argument does not contain a valid value.')

        if bytes_encoding == None: bytes_encoding = locale.getpreferredencoding()
        self._enc = bytes_encoding

        if encoding == None: encoding = locale.getpreferredencoding()

        buf = io.open(file, mode=mode+'b')
        super(UnicodeIOWrapper, self).__init__(buf, encoding=encoding, errors=errors)

    def write(self, s):
        if isinstance(s, bytes):
            s = unicode(s, encoding=self._enc, errors='strict')
        return super(UnicodeIOWrapper, self).write(s)

