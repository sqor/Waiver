#!/usr/bin/python
'''

'''

import os
import sys
import argparse
import requests
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    '''
    Parse given html and handle the script tags.
    '''
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.scriptUrls = []
        #@TODO: consider converting data to text here
        self.htmlData = []
        self.handle_script_tag = False

    def handle_starttag(self, tag, attrs):
        self.handle_script_tag = False
        if tag == "script":
            for attr in attrs:
                if attr[0] == "src":
                    self.scriptUrls.append(attr[1])
                    self.handle_script_tag = True

            if not self.handle_script_tag:
                self.htmlData.append({"tag": tag, "attrs": attrs} )
        else:
            self.htmlData.append({"tag": tag, "attrs": attrs} )

    def handle_endtag(self, tag):
        if not self.handle_script_tag:
            self.htmlData.append({"endTag": tag} )

        self.handle_script_tag = False

    def handle_data(self, data):
        if not self.handle_script_tag:
            self.htmlData.append({"data": data} )

    def handle_comment(self, data):
        self.htmlData.append({"data": data} )
    '''
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data
    '''

def parse_args(input_args):
    '''
    Parse the command line arguments and return an object containing the
    arguments.

    PARAM input_args list
        List of input arguments to parse.
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--html_dir',
                        help='directory to find the html file.')
    parser.add_argument('--html_filename',
                        help='html file to parse.')

    return parser.parse_args(input_args)

def main():
    '''
    
    '''
    # get the commandline arguments
    args = parse_args(sys.argv[1:])

    input_html_dir = args.html_dir
    input_html_filename = args.html_filename
    html_filepath = os.path.join(input_html_dir, input_html_filename)

    # Get the html file:
    parser = MyHTMLParser()
    with open(html_filepath, 'r') as fh:
        contents = fh.read()
        parser.feed(contents)

    #@TODO: check how parser handles <br>, <hr>

    new_html_contents = []

    for data in parser.htmlData:
        if data.has_key('tag'):
            new_html_contents.append("<%s" % (data['tag']))

        if data.has_key('attrs'):
            for attr in data['attrs']:
                new_html_contents.append(" %s=\"%s\"" % (attr[0], attr[1]))

        if data.has_key('tag'):
            new_html_contents.append(">")

        if data.has_key('endTag'):
            if data['endTag'] == 'html':
                new_html_contents.append("    <script src=\"main001.js\"></script>\n")

            new_html_contents.append("</%s>" % (data['endTag']))

        if data.has_key('data'):
            new_html_contents.append(data['data'])

    #print ''.join(new_html_contents)

    #@TODO: date/timestamp
    url_file_contents = ""
    for url in parser.scriptUrls:
        if url.startswith('http'):
            r = requests.get(url)
            url_file_contents += r.content
        else:
            url_fullpath = os.path.join(input_html_dir, url)
            if os.path.isfile(url_fullpath):
                with open(url_fullpath, 'r') as fh:
                    url_file_contents += fh.read()
            else:
                print "Couldn't find file: %s" % (url_fullpath)
        url_file_contents += '\n'

    with open(os.path.join(input_html_dir, 'main001.js'), 'w') as fh:
        fh.write(url_file_contents)

if __name__ == '__main__':
    main()
