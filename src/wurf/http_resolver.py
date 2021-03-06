#! /usr/bin/env python
# encoding: utf-8

import os
import hashlib


class HttpResolver(object):
    """
    Http Resolver functionality. Downloads a file.
    """

    def __init__(self, url_download, dependency, source, cwd):

        """ Construct a new instance.

        :param url_download: An UrlDownload instance
        :param dependency: The dependency instance.
        :param source: The URL of the dependency as a string
        :param cwd: Current working directory as a string. This is the place
            where we should create new folders etc.
        """
        self.url_download = url_download
        self.dependency = dependency
        self.source = source
        self.cwd = cwd

    def resolve(self):
        """
        Fetches the dependency if necessary.

        :return: The path to the resolved dependency as a string.
        """
        # Store the current source in the dependency object
        self.dependency.current_source = self.source

        # Use the first 6 characters of the SHA1 hash of the repository url
        # to uniquely identify the repository
        source_hash = hashlib.sha1(self.source.encode('utf-8')).hexdigest()[:6]

        # The folder for storing the file
        folder_name = 'http-' + source_hash
        folder_path = os.path.join(self.cwd, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if self.dependency.filename:
            filename = self.dependency.filename
        else:
            filename = None

        file_path = self.url_download.download(
            cwd=folder_path, source=self.source, filename=filename)

        assert os.path.isfile(file_path), "We should have a valid path here!"

        return file_path
