#!/usr/bin/env python3
"""Parse S3 ListObjectsV2 XML response from R2."""
import sys
import xml.etree.ElementTree as ET

data = sys.stdin.read()
# Strip XML namespace for ease
data = data.replace(' xmlns="http://s3.amazonaws.com/doc/2006-03-01/"', "")
try:
    root = ET.fromstring(data)
except ET.ParseError as e:
    print("PARSE_ERROR:", e)
    print(data[:500])
    sys.exit(1)
print(f"Bucket: {root.findtext('Name')} / KeyCount: {root.findtext('KeyCount')}")
for c in root.findall("Contents"):
    key = c.findtext("Key")
    size = c.findtext("Size")
    lm = c.findtext("LastModified")
    etag = c.findtext("ETag")
    print(f"  {key} | {size} bytes | {lm} | etag={etag}")
