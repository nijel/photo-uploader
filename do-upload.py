#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader for foto.droxy.cz
Main uploader script.
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright (c) 2007 Michal Čihař

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
import StringIO
import os
import sys
import webbrowser

debug = False

def dumpRequest(c, b):
    if debug:
        sys.stderr.write(80 * '-')
        sys.stderr.write('\n%d: %s\n' % (
            c.getinfo(pycurl.HTTP_CODE), 
            c.getinfo(pycurl.EFFECTIVE_URL)
            ))
        sys.stderr.write(b.getvalue())
        sys.stderr.write('\n')

def msg(s, noeol = False):
    if noeol:
        print s,
    else:
        print s
    sys.stdout.flush()


c = pycurl.Curl()
b = StringIO.StringIO()
# Write output to string buffer
c.setopt(pycurl.WRITEFUNCTION, b.write)
# We need to follow redirects
c.setopt(pycurl.FOLLOWLOCATION, 1)
# We need cookies support, but we don't have to store them
c.setopt(pycurl.COOKIEFILE, "")

# Init session...
msg('Initialising session...')
c.setopt(pycurl.URL, 'http://foto.droxi.cz/')
c.perform()
dumpRequest(c, b)
b.truncate(0)

cookies = c.getinfo(pycurl.INFO_COOKIELIST)
sessionid = cookies[0].split('\t')[6]

# Select photo and not photoalbum...
msg('Selecting photo order...')
c.setopt(pycurl.URL, 'http://foto.droxi.cz/index.php')
c.setopt(pycurl.HTTPPOST, [
    ('scripttest', '0'), 
    ('vyber', 'fotka')
    ])
c.perform()
dumpRequest(c, b)
b.truncate(0)

# Select fast/cheaper/simple order...
msg('Selecting fast/cheaper/simple order...')
c.setopt(pycurl.URL, 'http://foto.droxi.cz/typ-zakazky/index.php')
c.setopt(pycurl.HTTPPOST, [
    ('krok_zpet', '4'), 
    ('set_ordertype', 'disc'), 
    ('pokracovat', 'some text')
    ])
c.perform()
dumpRequest(c, b)
b.truncate(0)

# Now we have a upload form
file_list = sys.argv[1:]
files = len(file_list)
for i in range(files):
    current = file_list[i]
    base = os.path.basename(current)
    msg('Uploading %.01f%% [%d/%d]: %20s\r' % (100.0 * (i + 1) / files, i + 1, files, base), True)
    sys.stdout.flush()
    c.setopt(pycurl.HTTPPOST, [
        ('sessionid',  sessionid), 
        ('f1', (pycurl.FORM_FILE, current)), 
        ('nf1', ''),
        ('pokracovat', 'some text')
        ])
    c.setopt(pycurl.URL, 'http://foto.droxi.cz/vlozit-fotografie/upload.php?ilikephoto=%s&verze=droxi' % sessionid)
    c.perform()
    dumpRequest(c, b)
    b.truncate(0)

msg('Uploaded all %d photos                                  ' % files)
msg('You can review them here:')
msg('http://foto.droxi.cz/prehled-vlozenych-fotografii/?ilikephoto=%s' % sessionid)
msg('You can finish order here:')
msg('http://foto.droxi.cz/format-fotografii/?ilikephoto=%s' % sessionid)
msg('Opening review URL in browser...')
webbrowser.open('http://foto.droxi.cz/prehled-vlozenych-fotografii/?ilikephoto=%s' % sessionid)
