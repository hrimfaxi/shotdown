#!/usr/bin/python2
# coding: utf-8

" 安装脚本 "

import distutils.filelist

try:
    import py2exe
except ImportError:
    pass

import setuptools, os.path

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    entry_points = {
        'console_scripts' : [ 'shotdown= shotdown.main:main' ] },
    name = 'shotdown',
    version = '0.0',
    author = "hrimfaxi",
    author_email = "outmatch@gmail.com",
    description = ("shotdown: Yet another shooter.cn subtitle downloader."),
    license = "GPL",
    keywords = "subtitle downloader shooter.cn",
    url = "https://github.com/hrimfaxi/shotdown",
    packages = [ 'shotdown' ],
    long_description=read('README.md')
)

# vim: set tabstop=4 sw=4 expandtab:
