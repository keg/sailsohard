#/usr/bin/python

import gzip, urllib2
import xml.etree.ElementTree as ET
from StringIO import StringIO
import sqlite3



URL = 'https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/0PmgJAJrEq7TG0Rlu7oEc9UdOaCtTczH4/message'

request = urllib2.Request(URL)
request.add_header('Accept-encoding', 'gzip')
request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
response = urllib2.urlopen(request)
if response.info().get('Content-Encoding') == 'gzip':
    buf = StringIO( response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()

root = ET.fromstring(data)

connection = sqlite3.connect('sailsohard.db')
c = connection.cursor()
for message in root.iter('message'):
    values_dict = {}
    for child in message.getchildren():
        values_dict[child.tag] = child.text
    c.execute("insert into messages ('longitude', 'latitude', 'unitTime', 'messageType', 'dateTime', 'showCustomMsg', 'messengerName', 'messengerId', 'batteryState', 'messageDetail', 'id', 'modelId'), values()")

    print values_dict