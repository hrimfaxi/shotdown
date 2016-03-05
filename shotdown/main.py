#!/usr/bin/python2
# coding: utf-8

import argparse, os, errno, json
from shotdown import file_hash, net, log
from shotdown.constants import __version__

def get_subtitle_directory():
    return os.path.join(os.path.expanduser('~'), ".mplayer/sub")

def mkdir_recursive(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def show_metadata(r):
    log.info ("Metadata: ")
    log.info (json.dumps(r, indent=4, separators=(',', ': ')))

def get_subtitle(r, va):
    log.info ("Video has %d subtitle(s)" % (len(r)))
    if not r:
        return
    if va['no_download']:
        show_metadata(r)
        return

    if va['all']:
        for i in range(len(r)):
            for j in range(len(r[i]["Files"])):
                srt_url = r[i]["Files"][j]["Link"]
                log.debug (srt_url)
                net.download_subtitle(srt_url, dest_dir=va['output_dir'])
    else:
        if va["index"]:
            log.info("Selected subtitle index: %d", va["index"])
        srt_url = r[va["index"]]["Files"][0]["Link"]
        log.debug (srt_url)

        if va['output_filename']:
            net.download_subtitle(srt_url, path=va['output_filename'], dest_dir=va['output_dir'])
        else:
            net.download_subtitle(srt_url, dest_dir=va['output_dir'])

def get_subtitles(va):
    mkdir_recursive(va['output_dir'])
    log.info("Download directory set to %s", va['output_dir'])

    try:
        for filename in va['files']:
            try:
                filehash = file_hash.calc_file_hash(filename)
            except IOError as e:
                filehash = None
            r = net.get_metadata(filename, filehash=filehash, lang=va['language'])

            log.debug ("Metadata: ")
            log.debug (json.dumps(r, indent=4, separators=(',', ': ')))

            get_subtitle(r, va)
    except Exception as e:
        log.error(e)
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description="%(prog)s: Yet another shooter.cn subtitle downloader.")
    parser.add_argument('-a', '--all', action='store_true', help='Download all subtitles')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-n', '--no-download', dest='no_download', action='store_true', help='Don\'t download subtitle, show metadata only')
    parser.add_argument('-i', '--index', type=int, \
            default=0, help='Choice subtitle index to download, starting from 0')
    parser.add_argument('-l', '--language', type=str, \
            default='', choices=('chn', 'eng'), help='Choice subtitle language')
    parser.add_argument('-o', '--output-filename', dest='output_filename', \
            type=str, help='Set output directory')
    parser.add_argument('-O', '--output-dir', dest='output_dir', type=str, \
            default=get_subtitle_directory(), help='Set output directory')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('files', type=str, nargs='+', help='video file paths to search for subtitle')
    args = parser.parse_args()
    va = vars(args)
    log.init_logger('debug' if va['debug'] else 'info')
    log.debug("va: %s", str(va))
    get_subtitles(va)

if __name__ == "__main__":
    main()

# vim: set tabstop=4 sw=4 expandtab:
