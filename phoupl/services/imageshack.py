# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for ImageShack service.
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 Michal Čihař

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

MATCHER_IMG = re.compile('\[IMG\](.*)\[/IMG\]')
MATCHER_SHOW = re.compile('href="([^"]*)"><b>Show<')

class ImageShackService(phoupl.core.PhotoUploader):
    def _connect(self):
        # Init session...
        self.msg('Initialising session...')
        self.get('http://imageshack.us/')

    def _upload(self, image):
        self._curl.setopt(pycurl.HTTPHEADER, ['Expect:'])
        self.post('http://imageshack.us/',
                [
                    ('fileupload', (pycurl.FORM_FILE, image)),
                    ('uploadtype', 'on'),
                    ('refer', 'http://www.imageshack.us/'),
                    ('brand', ''),
                    ('email', ''),
                    ('MAX_FILE_SIZE', '13145728'),
                    ('optsize', '320x320'),
                    ('url', 'paste image url here'),

                ])
        data = self._buffer.getvalue()
        m = MATCHER_IMG.search(data)
        self._img_url = m.group(1)
        m = MATCHER_SHOW.search(data)
        self._show_url = m.group(1)

    def _post_upload(self):
        self.msg('''
You can link image as:
%s
You can display image here:
%s
''' %(self._img_url, self._show_url))

    def get_review_url(self):
        return self._show_url

# Register service
phoupl.register_service(
        'imageshack.us',
        ImageShackService,
        'http://imageshack.us/',
        ['new'],
        'ImageShack',
        languages = ['eng']
        )
