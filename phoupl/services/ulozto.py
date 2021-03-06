# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for UlozTo service.
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

MATCHER_SHOW = re.compile('<a href="(http://uloz.to/[^"]*)">http://uloz.to/')
MATCHER_SESSION = re.compile('action="/ul/upload.cgi\?tmp_sid=([^"]*)"')

class UlozToService(phoupl.core.PhotoUploader):
    def _connect(self):
        # Init session...
        self.msg('Initialising session...')
        self.get('http://uloz.to/')
        self._img_urls = []
        self._show_urls = []
        data = self._buffer.getvalue()
        m = MATCHER_SESSION.search(data)
        self._session = m.group(1)

    def _upload(self, image):
        self.post('http://uloz.to/ul/upload.cgi?tmp_sid=%s' % self._session,
                [
                    ('upfile_0', (pycurl.FORM_FILE, image)),
                    ('no_script', '1'),
                ])
        data = self._buffer.getvalue()
        m = MATCHER_SHOW.search(data)
        self._show_urls.append(m.group(1))

    def _post_upload(self):
        self.msg('''
You can display image here:
%s
''' % '\n'.join(self._show_urls))

    def get_review_url(self):
        return self._show_urls

# Register service
phoupl.register_service(
        'uloz.to',
        UlozToService,
        'http://uloz.to/',
        ['new'],
        'Uloz.to',
        languages = ['cze'],
        servicetype = 'storage'
        )
