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

from optparse import OptionParser
import phoupl
import webbrowser
import sys

# Parameters processing
usage = "usage: %prog [options] images"
parser = OptionParser(usage=usage)
parser.add_option("-s", "--service",
                  action="store", type="string",
                  dest="service_name", default="droxi.cz",
                  help="Name of service to use.")
parser.add_option("-l", "--list-services",
                  action="store_true",
                  dest="list_services", default=False,
                  help="List available services.")
parser.add_option("-b", "--open-browser",
                  action="store_true",
                  dest="open_browser", default=False,
                  help="Open order in browser after uploading.")
parser.add_option("-d", "--debug",
                  action="store_true",
                  dest="debug", default=False,
                  help="Show debugging output.")

(options, args) = parser.parse_args()

# List services
if options.list_services:
    print 'Available services:'
    for x in phoupl.list_services():
        print ' %s' % x
    sys.exit(0)

# Check for some files to upload
if len(args) == 0:
    parser.print_help()
    sys.exit("No files to upload.")

url = phoupl.upload_photos(options.service_name, args, debug = options.debug)

if options.open_browser:
    webbrowser.open(url)
