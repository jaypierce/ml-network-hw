import sys
import struct

class STLVec3:
    def __init__(self, x_coord, y_coord, z_coord):
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord

class STLTriangle:
    def __init__(self, normal, v0, v1, v2, attributes):
        self.normal = normal
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.attributes = attributes

class STLData:
    def __init__(self, header, tris):
        self.header = header
        self.tris = tris

def readFloat(f):
    float_bytes = f.read(4)
    return struct.unpack('f', float_bytes)[0]

def readVec3(f):
    x = ("%.4f" % readFloat(f))
    y = ("%.4f" % readFloat(f))
    z = ("%.4f" % readFloat(f))

    return STLVec3(x, y, z)
    
def readUnsignedInt(f):
    uint_bytes = f.read(4)
    return struct.unpack('I', uint_bytes)[0]

def readUINT16(f):
    uint16_bytes = f.read(2)
    return struct.unpack('H', uint16_bytes)[0]

def readTriangle(f):
    norm = readVec3(f)
    v0 = readVec3(f)
    v1 = readVec3(f)
    v2 = readVec3(f)
    attributes = readUINT16(f)

    return STLTriangle(norm, v0, v1, v2, attributes)

def retVec3(v):
    return (v.x, v.y, v.z,)

def parseSTL(filename):
    f = open(filename, "rb")
    header = f.read(80)

    num_tris = readUnsignedInt(f)

    tris = []

    for i in range(num_tris):
        tris.append(readTriangle(f))

    stlData = STLData(header, tris)

    return stlData

stlData = parseSTL(sys.argv[1])

import csv
with open('output.csv', 'w') as f:
    write = csv.writer(f)

    for triangle in stlData.tris:
        write.writerow(retVec3(triangle.normal))
        write.writerow(retVec3(triangle.v0))
        write.writerow(retVec3(triangle.v1))
        write.writerow(retVec3(triangle.v2))