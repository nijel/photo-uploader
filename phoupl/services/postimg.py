# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for PostImage service.
'''
__author__ = 'Andrew Shadura'
__email__ = 'andrew@shadura.me'
__license__ = '''
Copyright © 2007 - 2010 Michal Čihař
Copyright © 2014 Andrew Shadura

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

MATCHER_TAG = re.compile(r'\[img\]([^]]*)\[/img\]')
MATCHER_SHOWLINK = re.compile(r'(https*://postimg.org/image/[^/]*/)')
MATCHER_DELETELINK = re.compile(r'(https*://postimg.org/delete/[^/]*/)')

class PostImageService(phoupl.core.PhotoUploader):
    def _connect(self):
        # Init session...
        self.msg('Initialising session...')
        self.get('http://postimage.org/')
        self._img_urls = []
        self._show_urls = []
        self._delete_urls = []

    def _upload(self, image):
        self._curl.setopt(pycurl.HTTPHEADER, ['Expect: 100-continue'])
        self.post('http://postimage.org/index.php',
                [
                    ('upload', (pycurl.FORM_FILE, image)),
                ])
        data = self._buffer.getvalue()
        m = MATCHER_TAG.search(data)
        self._img_urls.append(m.group(1))
        m = MATCHER_SHOWLINK.search(data)
        self._show_urls.append(m.group(1))
        m = MATCHER_DELETELINK.search(data)
        self._delete_urls.append(m.group(1))


    def _post_upload(self):
        self.msg('''
You can link image as:
%s
You can display image here:
%s
You can delete image here:
%s
''' % ('\n'.join(self._img_urls), '\n'.join(self._show_urls), '\n'.join(self._delete_urls)))

    def get_review_url(self):
        return self._show_urls

# Register service
phoupl.register_service(
        'postimage.org',
        PostImageService,
        'http://postimage.org/',
        ['new'],
        'PostImage',
        languages = ['eng'],
        servicetype = 'storage'
        )
