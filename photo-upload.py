#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo uploader, main command line script.
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 - 2009 Michal Čihař

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
import os

CONFIGFILE = '~/.photo-upload'
CONFIGDEFAULTS = {
        'photo-upload' : {
            'service' : 'imageshack.us',
            'open-browser' : False,
            'use-browser' : '',
            }
        }

def configure():
    '''
    Parameters and config file processing.
    '''
    config = phoupl.config.Config(CONFIGFILE, CONFIGDEFAULTS)

    program_name = 'photo-upload %s' % phoupl.__version__
    usage = "usage: %prog [options] images"
    parser = OptionParser(usage = usage, version = program_name)
    parser.add_option("", "--license",
                      action="store_true",
                      dest="show_license", default=False,
                      help="Display program license.")
    parser.add_option("-s", "--service",
                      action="store", type="string",
                      dest="service_name",
                      default=config.get('photo-upload', 'service'),
                      help="Name of service to use.")
    parser.add_option("-l", "--list-services",
                      action="store_true",
                      dest="list_services", default=False,
                      help="List available services.")
    parser.add_option("-b", "--open-browser",
                      action="store_true",
                      dest="open_browser",
                      default=config.getbool('photo-upload', 'open-browser'),
                      help="Open order in browser after uploading.")
    parser.add_option("-B", "--use-browser",
                      action="store",
                      dest="use_browser",
                      default=config.get('photo-upload', 'use-browser'),
                      help="Define browser to use when opening web page. " +
                      "Default is autodetected by python webbrowser.")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug", default=False,
                      help="Show debugging output.")
    parser.add_option("-S", "--session",
                      action="store", type="string",
                      dest="session", default=None,
                      help="Existing session to reuse "+
                      "(some services won't work without existing session).")

    (options, args) = parser.parse_args()

    # Informational options
    if options.show_license:
        print(program_name)
        print(__license__)
        sys.exit(0)

    return (options, args, parser, config)

def print_str(info, name):
    '''
    Prints single string value.
    '''
    try:
        print('%s: %s' % (name, info[name]))
    except KeyError:
        return

def print_list(info, name):
    '''
    Prints list value.
    '''
    try:
        print('%s: %s' % (name, ', '.join(info[name])))
    except KeyError:
        return

def list_services():
    '''
    List available services.
    '''
    for service in phoupl.list_services():
        print('Name: %s' % service)
        info = phoupl.get_service_info(service)
        print_str(info, 'FullName')
        print_str(info, 'Type')
        print_str(info, 'URL')
        print_list(info, 'Features')
        print_list(info, 'Languages')
        print_list(info, 'Countries')
        print()

def main():
    '''
    Main script.
    '''
    (options, args, parser, config) = configure()

    if options.debug:
        sys.stderr.write('Started photo-uploader, params:\n')
        sys.stderr.write('%s\n' % repr(sys.argv))
        sys.stderr.write('Options:\n')
        sys.stderr.write('%s\n' % repr(options))
        sys.stderr.write('Args:\n')
        sys.stderr.write('%s\n' % repr(args))

    # List services
    if options.list_services:
        list_services()
        sys.exit(0)

    # Check for some files to upload
    if len(args) == 0:
        parser.print_help()
        sys.exit("No files to upload.")

    urls = phoupl.upload_photos(options.service_name, args,
            debug = options.debug,
            session = options.session,
            configstorage = config)

    if type(urls) == str:
        urls = [urls]

    for url in urls:
        if options.open_browser:
            if options.use_browser != '':
                os.system('%s \'%s\' &' % (options.use_browser, url))
            else:
                webbrowser.open(url)


if __name__ == '__main__':
    main()
