#!/usr/bin/python
# coding: utf-8

import cgi, os, sys, json
from shotdown.constants import __version__
from shotdown import log

if sys.version_info[0] < 3:
    import urllib, urllib2
    Request = urllib2.Request
    urlopen = urllib2.urlopen
    urlencode = urllib.urlencode
else:
    import urllib.request, urllib.parse
    Request = urllib.request.Request
    urlopen = urllib.request.urlopen
    urlencode = urllib.parse.urlencode

URI = "https://www.shooter.cn/api/subapi.php"
SYS_ENCODING = sys.getfilesystemencoding()
HEADERS = { "User-Agent" : "shotdown/%s (https://github.com/hrimfaxi/shotdown)" % (__version__)}


def to_utf8(path):
    if isinstance(path, str):
        return path.encode('utf8')
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
    data = urlencode(post_field)
    log.debug("Sending request: %s", data)
    req = Request(URI, data.encode('utf-8'), HEADERS)
    response = urlopen(req)
    
    if response.code != 200:
        return []

    response = response.read()

    # 没有找到字幕
    if response == b"\xff":
        return []

    res_js = json.loads(response.decode('utf-8'))
    return res_js

def get_spared_pathname(path):
    orig = os.path.splitext(path)
    cnt = 1
    while os.path.exists(path):
        path = "%s(%d)%s" % (orig[0], cnt, orig[-1])
        cnt += 1
    return path

def download_subtitle(url, only_needed, path="", dest_dir="", ):
    log.info ("Downloading subtitle...")
    req = Request(url, None, HEADERS)
    response = urlopen(req)

    if response.code != 200:
        raise RuntimeError("Subtitle downloading gets HTTP error code(%d)" % (response.code))

    if not path:
        _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        path = os.path.basename(params['filename'])
    if only_needed:
        if os.path.exists(path):
            log.info("%s already exists, no need to download." % (path))
            return
    else:
        path = get_spared_pathname(os.path.join(dest_dir, path))

    log.info("Saving as %s" % (path))
    with open(path, "wb") as subtitle:
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
