# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Helper class for ilikephoto based services.
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

import phoupl
import pycurl

import re

MATCHER_FAIL = re.compile('zkontrolujte pros.*m naposledy uploadlou fotografii')
MATCHER_KONTROLA = re.compile('input type="hidden" name="kontrola" value="([^"]*)"')

class ILikePhoto:
    """
    Helper class for ilikephoto based services.
    """
    def __init__(self, baseurl, version):
        self._baseurl = baseurl
        self._version = version
        self._kontrola = ''

    def ipl_init_session(self):
        # Init session...
        self.msg('Initialising session...')
        self.get(self.ipl_get_base_url())
        self.cookies = self._curl.getinfo(pycurl.INFO_COOKIELIST)
        self._session = self.cookies[0].split('\t')[6]
        self.msg('Created session %s' % self._session)

    def ipl_select_simple(self):
        self.msg('Selecting fast/cheaper/simple order...')
        self.post(self.ipl_get_simple_url(),
                [
                    ('krok_zpet', '4'),
                    ('set_ordertype', 'disc'),
                    ('pokracovat', 'some text')
                ])
        self.ipl_get_kontrola()

    def ipl_get_base_url(self):
        return '%s/' % self._baseurl

    def ipl_get_simple_url(self):
        return '%s/index.php' % self._baseurl

    def ipl_get_upload_url(self):
        return '%s/vlozit-fotografie/upload.php?ilikephoto=%s&verze=%s&kam=0' % (
                self._baseurl,
                self._session,
                self._version,
                )

    def ipl_get_kontrola(self):
        data = self._buffer.getvalue()
        m = MATCHER_KONTROLA.search(data)
        if m is None:
            # Hope this is okay
            self._kontrola = ''
        else:
            self._kontrola = m.group(1)

    def ipl_check_failure(self):
        data = self._buffer.getvalue()
        m = MATCHER_FAIL.search(data)
        if m is not None:
            raise phoupl.core.UploadFailed('Error while uploading file, check uploaded photos at %s.' % self.get_review_url())

    def ipl_upload(self, image):
        self.post(self.ipl_get_upload_url(),
                [
                    ('sessionid',  self._session),
                    ('f1', (pycurl.FORM_FILE, image)),
                    ('nf1', ''),
                    ('pokracovat', 'some text'),
                    ('kontrola', self._kontrola),
                ])
        self.ipl_check_failure()
        self.ipl_get_kontrola()

    def ipl_get_review_url(self):
        return '%s/prehled-vlozenych-fotografii/?ilikephoto=%s' % (
                self._baseurl,
                self._session,
                )

    def ipl_get_finish_url(self):
        return '%s/format-fotografii/?ilikephoto=%s' % (
                self._baseurl,
                self._session,
                )

    def ipl_post_upload(self):
        self.msg('''
You can review them here:
%s
You can finish order here:
%s
''' % (
    self.ipl_get_review_url(),
    self.ipl_get_finish_url(),
    ))
