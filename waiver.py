import requests
import os
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import argparse

class MyHTMLParser(HTMLParser):
    scriptUrls = []
    htmlData = []
    handle_script_tag = False

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

def getargs():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--html_dir',
                        help='directory to find the html file.')
    parser.add_argument('--html_filename',
                        help='html file to parse.')

    return parser.parse_args()

def main():
    args = getargs()

    html_filepath = os.path.join(args.html_dir, args.html_filename)

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

    print ''.join(new_html_contents)

    #@TODO: date/timestamp
    with open(os.path.join(args.html_dir, 'main001.js'), 'w') as fh:
        fh.write('\n'.join(parser.scriptUrls))

if __name__ == '__main__':
    main()
