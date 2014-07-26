#/usr/bin/python

import sys, gzip, urllib2
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
db = sqlite3.connect('sailsohard.db')
message_last_update = db.execute('select unixTime from messages order by unixTime desc limit 1').fetchone()[0]

for message in root.iter('message'):
    if int(message.find('./unixTime').text) > int(message_last_update):
        
        db.execute('insert into messages values(?,?,?,?,?,?,?,?,?,?,?,?)',
            [message.find('./longitude').text,
            message.find('./latitude').text,
            message.find('./unixTime').text,
            message.find('./messageType').text,
            message.find('./dateTime').text,
            message.find('./showCustomMsg').text,
            message.find('./messengerName').text,
            message.find('./messengerId').text,
            message.find('./batteryState').text,
            message.find('./messageDetail').text,
            message.find('./id').text,
            message.find('./modelId').text])
        db.commit()
db.close()