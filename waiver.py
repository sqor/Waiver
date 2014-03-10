import requests
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):
    scriptTags = []
    inGroup = False
    scriptGroup = []

    htmlData = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.inGroup = True
            for attr in attrs:
                if attr[0] == "src":
                    self.scriptTags.append(attr[1])
                else: 
                    self.htmlData.append({"tag": tag, "attrs": attrs} )
        else:
            self.htmlData.append({"tag": tag, "attrs": attrs} )
            self.inGroup = False
    def handle_endtag(self, tag):
        if not self.inGroup:
            self.htmlData.append({"endTag": tag} )
    def handle_data(self, data):
        if not self.inGroup:
            self.htmlData.append({"data": data} )


# Get the html file:
htmlSource = requests.get("https://raw.github.com/sqor/Waiver/master/index.html")

parser = MyHTMLParser()
parser.feed(htmlSource.content)

#@TODO: check how parser handles <br>, <hr>

for data in parser.htmlData:
    if data.has_key('tag'):
        print "<%s" % (data['tag']),

    if data.has_key('attrs'):
        for attr in data['attrs']:
            print " %s=\"%s\"" % (attr[0], attr[1]),

    if data.has_key('tag'):
        print ">",

    if data.has_key('endTag'):
        print "</%s>" % (data['endTag'])
