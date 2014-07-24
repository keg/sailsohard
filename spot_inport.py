#/usr/bin/python

import gzip, urllib2
import xml.etree.ElementTree as ET
from StringIO import StringIO



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
for message in root.iter('message'):
    for child in message.getchildren():
        #this is stupid, don't do so many if checks. Create a data object and dump what you need in
        if child.tag == 'id':
            m_id = child.text
        elif child.tag == 'dateTime':
            m_date_time = child.text
        elif child.tag == 'latitude':
            m_latitude = child.text
        elif child.tag == 'longitude':
            m_longitude = child.text
        
        print m_id, m_date_time