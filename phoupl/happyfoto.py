# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Helper class for happyfoto based services.
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 - 2008 Michal Čihař

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

import pycurl

import re

MATCHER_SESSION = re.compile('window.location.href = \'album\?xsl=standard&action=album&id=([0-9A-Z]*)\'')

class HappyFoto:
    """
    Helper class for ilikephoto based services.
    """
    def __init__(self, domain, mnd, baseurl = None):
        if baseurl is None:
            self._baseurl = 'http://digi.%s/' % domain
        self._domain = domain
        self._mnd = mnd
        self._user = self._config.get(domain, 'user')
        self._password = self._config.get(domain, 'password')

    def _connect(self):
        # Init session...
        self.msg('Initialising session...')
        self.post('%s/album?xsl=login_success&action=login&mnd=%d' % (self._baseurl, self._mnd), [
            ('mnd', '%s' % self._mnd),
            ('txtName', self._user),
            ('txtPassword', self._password),
            ])
        data = self._buffer.getvalue()
        m = MATCHER_SESSION.search(data)
        self._session = m.group(1)

    def _upload(self, image):
        self.post('%s/album?xsl=cart&action=upload&id=%s' % (self._baseurl, self._session), [
                    ('Filedata_01', (pycurl.FORM_FILE, image)),
                    ('session', self._session),
                    ('cut', 'fit'),
                    ('total_files', '1'),
                ])
        data = self._buffer.getvalue()
        if data.find('order_confirm') == -1:
            raise phoupl.core.UploadFailed('Error while uploading file, check uploaded photos at %s.' % self.get_review_url())

    def get_review_url(self):
        return self._baseurl
