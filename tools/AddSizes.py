import os, sys
from pymongo import MongoClient
import struct, imghdr

def sz(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return -1
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return -1
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
                return -1
        else:
            print ('error: ', imghdr.what(fname))
            return -1
        return width, height

m = MongoClient()
db = m.climateprisms

for rec in db.nodes.find():
	if 'height' not in rec or 'width' not in rec:
		folder = rec['folder']
		filename = rec['filename']
		imgfile = 'images/' + folder + '/' + filename
		if os.path.exists(imgfile):
			s = sz(imgfile)
			if (s == -1):
				print ('problem with', imgfile)
			else:
				w, h = s
				db.nodes.update({'_id': rec['_id']}, {'$set': {'width': w, 'height': h}})
				print (imgfile, 'is OK', 'id:', rec['_id'], 'w:', w, 'h:', h)
				print list(db.nodes.find({'_id': rec['_id']}))[0]
		else:
			print imgfile, 'is NOT OK'
