#!/usr/bin/python2
# coding: utf-8

import urllib, urllib2, cgi, os, sys, json
import file_hash, log
from shotdown.constants import __version__

URI = "https://www.shooter.cn/api/subapi.php"
SYS_ENCODING = sys.getfilesystemencoding()
HEADERS = { "User-Agent" : "shotdown/%s (https://github.com/hrimfaxi/shotdown)" % (__version__)}

def to_utf8(path):
    return path.decode(SYS_ENCODING).encode('utf8')

def get_metadata(pathinfo, filehash="", lang=""):
    pathinfo = to_utf8(os.path.splitext(os.path.basename(pathinfo))[0])
    post_field = {
        "pathinfo" : pathinfo,
        "format" : "json",
    }
    if lang:
        if lang not in ("chn", "eng"):
            raise RuntimeError("Subtitle language can only be either chn or eng.")
        post_field["lang"] = lang
    if filehash:
        post_field["filehash"] = filehash
    data = urllib.urlencode(post_field)
    log.debug("Sending request: %s", data)
    req = urllib2.Request(URI, data, HEADERS)
    response = urllib2.urlopen(req)
    
    if response.code != 200:
        return []

    response = response.read()

    # 没有找到字幕
    if response == "\xff":
        return []

    res_js = json.loads(response)
    return res_js

def download_subtitle(url, path="", dest_dir="", ):
    log.info ("Downloading subtitle...")
    req = urllib2.Request(url, '', HEADERS)
    response = urllib2.urlopen(req)

    if response.code != 200:
        raise RuntimeError("Subtitle downloading gets HTTP error code(%d)" % (response.code))

    if not path:
        _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        path = os.path.basename(params['filename'])
    log.info("Saving as %s" % (path))

    with open(os.path.join(dest_dir, path), "wb") as subtitle:
        subtitle.write(response.read())

def main():
    log.init_logger('debug')
    r = get_metadata("中国")
    print (r)
    r = get_metadata("中国", lang="chn")
    print (r)
    r = get_metadata("中国", lang="eng")
    print (r)
    r = get_metadata("中国", lang="nosuch")
    print (r)

if __name__ == "__main__":
    main()

# vim: set tabstop=4 sw=4 expandtab:
