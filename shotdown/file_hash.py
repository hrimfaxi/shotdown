#!/usr/bin/python
# coding: utf-8

import hashlib, os, math

def digest_file(f, pos, length):
    f.seek(pos)
    data = f.read(length)
    return hashlib.md5(data).hexdigest()

def calc_file_hash(path):
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()

        if size < 8192:
            raise RuntimeError("video file length too small")

        offsets = [ 4096, math.floor(2 * size / 3), math.floor(size / 3), size - 8192]
        r = [ digest_file(f, offset, 4096) for offset in offsets ]

    return ";".join(r)

if __name__ == "__main__":
    r = calc_file_hash("../contrib/testidx.avi")
    assert(r ==
            "84f0e9e5e05f04b58f53e2617cc9c866;b1f0696aec64577228d93eabcc8eb69b;f54d6eb31bef84839c3ce4fc2f57991c;f497c6684c4c6e50d0856b5328a4bedc")
    print ("TEST OK")

# vim: set tabstop=4 sw=4 expandtab:
