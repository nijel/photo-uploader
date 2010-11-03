# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4 tw=78:
'''
Photo-Uploader core.
Generic class for uploading photos, no real functionality, just wrapping cURL
and image uploading.
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 - 2010 Michal Čihař

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License version 2 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import sys
import os
import pycurl
import io

from __future__ import print_function

class PhoUplNotImplemented(Exception):
    '''
    Raised when some functionality not implemented by plugin.
    '''
    pass

class UploadFailed(Exception):
    '''
    Raised when upload fails.
    '''
    pass

class NotConfigured(Exception):
    '''
    Raised when configuration is missing.
    '''
    pass

class PhotoUploader:
    '''
    Generic photo uploader class for handling photo uploads.
    '''
    def __init__(self, debug = False, msgcallback = None, session = None,
            config = None):
        '''
        Creates PhotoUploader object.
        '''
        # Variables
        self._debug = debug
        self._msgcallback = msgcallback
        self._connected = False
        self._session = session
        self._config = config

        # Curl backend
        self._curl = pycurl.Curl()
        self._buffer = io.StringIO()
        # Write output to string buffer
        self._curl.setopt(pycurl.WRITEFUNCTION, self._buffer.write)
        # We need to follow redirects
        self._curl.setopt(pycurl.FOLLOWLOCATION, 1)
        # We need cookies support, but we don't have to store them
        self._curl.setopt(pycurl.COOKIEFILE, "")

    def msg(self, text, noeol = False):
        '''
        Prints message to user.
        '''
        if self._msgcallback is not None:
            self._msgcallback(text, noeol)
        else:
            if noeol:
                print(text, end=' ')
            else:
                print(text)
            sys.stdout.flush()

    def get_session(self):
        '''
        Returns currently used session.
        '''
        if self._session is None:
            raise ValueError('Session not known!')

        return self._session

    def dump_request(self):
        '''
        Dumps request data if debug is enabled.
        '''
        if self._debug:
            sys.stderr.write(80 * '-')
            sys.stderr.write('\nStatus: %d: %s\n' % (
                self._curl.getinfo(pycurl.HTTP_CODE),
                self._curl.getinfo(pycurl.EFFECTIVE_URL)
                ))
            sys.stderr.write('Content:\n')
            sys.stderr.write(self._buffer.getvalue())
            sys.stderr.write('\n')

    def do_request(self):
        '''
        Performs request using current cURL configuration.
        '''
        # Cleanup buffer at start
        self._buffer.truncate(0)
        # Do the request
        self._curl.perform()
        # Debugging
        self.dump_request()

    def get(self, url):
        '''
        Performs GET request on URL.
        '''
        # Set URL to fetch
        self._curl.setopt(pycurl.URL, url)
        # Do the actual request
        self.do_request()

    def post(self, url, params = None):
        '''
        Performs POST request on URL with parameters.
        '''
        if self._debug:
            sys.stderr.write('POST: %s\n' % url)
        # Set URL to fetch
        self._curl.setopt(pycurl.URL, url)
        # Set POST content
        if params is None:
            params = []
        self._curl.setopt(pycurl.HTTPPOST, params)
        # Do the actual request
        self.do_request()

    def _connect(self):
        '''
        Actually connect to photo service. You should implement this in
        subclass.
        '''
        raise PhoUplNotImplemented()

    def connect(self):
        '''
        Connects if you are not already connected.
        '''
        if not self._connected:
            self._connect()

    def _upload(self, image):
        '''
        Uploads single image to photo service. You should implement this in
        subclass.
        '''
        raise PhoUplNotImplemented()

    def _post_upload(self):
        '''
        Executed after uploading images, use this for hooking up in subclass.
        '''
        return

    def upload(self, images):
        '''
        Upload images listed in images parameter. List should contain paths to
        files.
        '''
        self.connect()
        count = len(images)
        uploaded = 0
        for i in range(count):
            current = images[i]
            base = os.path.basename(current)
            percent = 100.0 * (i + 1) / count
            self.msg('Uploading %5.01f%% [%d/%d]: %20s\r' %
                    (
                        percent,
                        i + 1,
                        count,
                        base
                    ),
                    True)
            if not os.path.isfile(current):
                self.msg(('Skipped %s, not a file!' % current) + 40 * ' ')
                continue
            self._upload(current)
            uploaded = uploaded + 1
        if uploaded == 0:
            self.msg('None photos uploaded!')
        elif uploaded == count:
            self.msg(('Uploaded all %d photos' % count) + 40 * ' ')
        else:
            self.msg(('Uploaded %d photos out of %d files' % (uploaded, count)) + 40 * ' ')
        self._post_upload()

    def get_review_url(self):
        '''
        Returns URL suitable for review/finishing order. You should implement
        this in subclass.
        '''
        raise PhoUplNotImplemented()

    def get_url(self):
        '''
        Returns URL with information about service. You should implement
        this in subclass.

        This function can return either string of list of strings.
        '''
        raise PhoUplNotImplemented()

    def get_features(self):
        '''
        Returns list of supported features. You should implement
        this in subclass.

        Features are described in README.
        '''
        return []
