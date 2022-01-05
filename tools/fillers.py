import os, sys
from pymongo import MongoClient
import struct, imghdr

if len(sys.argv) != 2:
  print("syntax: python fillers.py project")
  sys.exit

project = sys.argv[1]

def sz(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return -1
        return width, height

m = MongoClient('localhost', 1336)
m['climateprisms'].drop_collection('fillers')

for i in os.listdir(project + '/static/content/fillers'):
	s = sz('content/fillers/' + i)
	if s != -1:
		m.climateprisms['fillers'].insert_one({'fname': 'content/fillers/' + i, 'width': s[0], 'height': s[1]})
