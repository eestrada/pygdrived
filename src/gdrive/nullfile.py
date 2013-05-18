import io as _io

class NullTextFile(_io.TextIOBase):
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

class NullFile(_io.RawIOBase):
    def read(self, n=-1):
        return b''
    def write(self, b):
        return len(b)
    def readable(self):
        return True
    def writable(self):
        return True
