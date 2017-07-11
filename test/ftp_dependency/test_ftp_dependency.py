#!/usr/bin/env python
# encoding: utf-8

import pytest


def mkdir_app(directory):
    app_dir = directory.mkdir('app')
    app_dir.copy_file('test/ftp_dependency/app/main.cpp')
    app_dir.copy_file('test/ftp_dependency/app/wscript')

    app_dir.copy_file('build/waf')

    return app_dir


@pytest.mark.networktest
def test_ftp_dependency(testdirectory):

    app_dir = mkdir_app(directory=testdirectory)

    app_dir.run('python', 'waf', 'configure')
    app_dir.run('python', 'waf', 'build')

    app_dir.run('python', 'waf', 'configure', '--fast_resolve')
    app_dir.run('python', 'waf', 'build')