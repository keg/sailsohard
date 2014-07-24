#/usr/bin/python

from StringIO import StringIO
from xml.dom import minidom
import gzip, urllib2

URL = 'https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/0PmgJAJrEq7TG0Rlu7oEc9UdOaCtTczH4/message'

request = urllib2.Request(URL)
request.add_header('Accept-encoding', 'gzip')
request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
response = urllib2.urlopen(request)
if response.info().get('Content-Encoding') == 'gzip':
    buf = StringIO( response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()

xmldoc = minidom.parseString(data)
message_list = xmldoc.getElementsByTagName('message')
for message in message_list:
    for node in message.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.localName == 'dateTime':
            print message[0].attributes['dateTime'].value