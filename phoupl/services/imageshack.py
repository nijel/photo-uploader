# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for ImageShack service.
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
import json

MATCHER_TAG = re.compile(r'\[URL=([^]]*)\]\[IMG\]([^]]*)\[/IMG\]\[/URL\]')

class ImageShackService(phoupl.core.PhotoUploader):
    def _connect(self):
        # Init session...
        self.msg('Initialising session...')
        self.get('http://imageshack.us/')
        self._img_urls = []
        self._show_urls = []

    def _upload(self, image):
        self._curl.setopt(pycurl.HTTPHEADER, ['Expect:'])
        self.post('http://imageshack.us/upload_api.php',
                [
                    ('fileupload', (pycurl.FORM_FILE, image)),
                    ('format', 'json'),
                    ('email', ''),
                    ('public', 'yes' if self._config.getbool('imageshack.us', 'public') else 'no'),
                    ('key', 'SYKFZ21G9186be76287f58e42c6f5ef47b992697'),
                    ('cookie', self._config.get('imageshack.us', 'regcode')),
                ])
        response = json.load(self._buffer)
        self._img_urls.append(response["links"]["image_link"])
        self._show_urls.append(response["links"]["is_link"])

    def _post_upload(self):
        self.msg('''
You can link image as:
%s
You can display image here:
%s
''' % ('\n'.join(self._img_urls), '\n'.join(self._show_urls)))

    def get_review_url(self):
        return self._show_urls

# Register service
phoupl.register_service(
        'imageshack.us',
        ImageShackService,
        'http://imageshack.us/',
        ['new'],
        'ImageShack',
        languages = ['eng'],
        servicetype = 'storage'
        )
