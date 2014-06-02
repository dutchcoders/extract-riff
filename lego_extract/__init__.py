from __future__ import print_function
from __future__ import unicode_literals

import struct
import sys
import logging

try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

logger = logging.getLogger(__name__)

# Subchunks also have the same structure as chunks. A subchunk is simply any chunk that is contained within another chunk. The only chunks that may contain subchunks are the RIFF file chunk RIFF and the list chunk, LIST (explained in the next section). All other chunks may contain only data.

class Chunk(object):
    def __init__(self):
        self.parent = None
        self.level = 0 
        pass

    def __str__(self):
        return ''.join(['\t' for i in range(self.level)]) + "Chunk {1}: Block size: {0} -> {2}".format(self.block_size, self.signature, self.data[:20])

class ParentChunk(Chunk):
    def __init__(self, f):
        super(ParentChunk, self).__init__()

        self.f = f
        pass

    def read_c_str(self, f):
        s = ""
        while True:
            c=f.read(1)
            if (c==b'\00'):
                break
            try:
                s = s + str(c, 'utf8') 
            except TypeError as exc:
                s = s + str(c) 

        return (s)

    def subchunks(self):
        SUBCHUNK = b"<4sL"
        size = struct.calcsize(SUBCHUNK)
        while True:
            data = self.f.read(size)
            if len(data) == 0:
                return

            subchunk = Chunk()
            subchunk.level= self.level +1
            subchunk.parent = self.parent
            (subchunk.signature, subchunk.block_size) = (struct.unpack(SUBCHUNK,data))

            subchunk.data = self.f.read(subchunk.block_size)
            import binascii
            print (binascii.hexlify(subchunk.data[:50]))
            print (binascii.hexlify(subchunk.signature))
            logger.debug ("{0} {1} {2}".format(subchunk.signature, subchunk.block_size, binascii.hexlify(subchunk.data[:50])))

            # round up to even word boundary
            if (subchunk.block_size % 2==1):
                    self.f.read(1)

            if (subchunk.signature==b'LIST'):
                p = List(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                yield p
                #print (p)
                for x in p.subchunks():
                    #print (x)
                    yield x

            elif (subchunk.signature==b'MxDa'):
                yield subchunk
                # Data?
                pass
            elif (subchunk.signature==b'MxHd'):
                logger.debug(subchunk)
                yield subchunk
                pass
            elif (subchunk.signature==b'MxOf'):
                logger.debug(subchunk)
                yield subchunk
                pass
            elif (subchunk.signature==b'MxOb'):
                p = MxOb(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                #print ("{0} >>> ".format(p))
                # yield subobjects
                yield p

                for x in p.subchunks():
                    #logger.debug("BLABLA Self: {0} Sub: {1} Parent: {2}".format(str(p), str(x), str(self.parent)))
                    yield x
                #print ("<<< {0}".format(p))
            elif (subchunk.signature==b'MxCh'):
                p = MxCh(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                yield p
                pass
            elif (subchunk.signature==b'MxSt'):
                p = MxSt(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                #logger.info("found stream")
                #logger.debug ("{0} >>> ".format(p))
                yield p
                iter_subchunks = p.subchunks()
                for x in iter_subchunks:
                    yield x
            elif (subchunk.signature==b'pad '):
                #print ("Skipping padding")
                logger.debug("Skipping padding")
                pass
            else:
                import binascii
                raise Exception("Unknown chunk found {0} {1}.".format(subchunk, binascii.hexlify(subchunk.data[:40])))

    def __str__(self):
        return ''.join(['\t' for i in range(self.level)]) + "(ParentChunk): Block size: {0}\nSignature: {1}\n".format(self.block_size, self.signature)

class MxCh(ParentChunk):
    def __init__(self, chunk, f):
        super(MxCh, self).__init__(f)

        self.block_size = chunk.block_size
        self.signature = chunk.signature
        self.level = chunk.level
        self.parent = chunk.parent

        import binascii
        (self.mode, self.id) = struct.unpack(b"<hL", self.f.read(6))
        self.data = chunk.data

    def __str__(self):
        import binascii
        return (''.join(['\t' for i in range(self.level)]) + "(MxCh Chunk) Parent: {0} {1} {2} id: {3} mode: {4} {5}".format(self.parent, self.signature, self.block_size, self.id, self.mode, binascii.hexlify(self.data[16:50]) ))

class MxOb(ParentChunk):
    """
    Object
    """


    def __init__(self, chunk, f):
        super(MxOb, self).__init__(f)

        self.block_size = chunk.block_size
        self.signature = chunk.signature
        self.data = chunk.data
        self.s1 = None
        self.s2 = None
        self.s3 = None
        self.s4 = None
        self.path = None
        self.id = None
        self.level = chunk.level
        self.parent = chunk.parent

        self.f=StringIO(chunk.data)
        import binascii
        #print(binascii.hexlify(chunk.data))
        HEADER = b"<H"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        self.s1 = (struct.unpack(HEADER,data))[0]
        print (self.s1)

        import binascii

        if self.s1==4:
            # WAV?
            self.s2=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(4)))
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            (binascii.hexlify(self.f.read(6 * 16 - 6)))
            self.path=self.read_c_str(self.f)
            self.s4=self.read_c_str(self.f)
            (binascii.hexlify( self.f.read(12)))
            self.s4=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(12)))
        elif self.s1==3:
            # SMK? / FLC / Video?
            # http://wiki.multimedia.cx/index.php?title=Smacker
            self.s2=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(4)))
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            (binascii.hexlify(self.f.read(6 * 16 - 6 )))
            self.s4=self.read_c_str(self.f)
            self.path=self.read_c_str(self.f)
            #import binascii
            (binascii.hexlify(self.f.read(12 )))
            (self.read_c_str(self.f))
            (binascii.hexlify(self.f.read(12)))
            #print (binascii.hexlify(self.f.read(10)))
        elif self.s1==8:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            self.f.read(6 * 16 - 6 )
            self.path=self.read_c_str(self.f)
            self.f.read(12)
            self.s4 =self.read_c_str(self.f)
            self.f.read(6)
            #import binascii

            #print (binascii.hexlify(self.f.read(10)))
        elif self.s1==6:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            self.f.read(6 * 16 - 6 )
            self.path=self.read_c_str(self.f)
            #import binascii
            #print (binascii.hexlify(self.f.read(10)))
        elif self.s1==7:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            (binascii.hexlify(self.f.read(6 * 16 - 8 )))
            data = (binascii.hexlify(self.f.read(2 )))
            if not data == b'0000':
                self.s4 = self.read_c_str(self.f)

        elif self.s1==11:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            self.f.read(6 * 16 - 6)
            self.s4=self.read_c_str(self.f)
            self.path=self.read_c_str(self.f)
            ('s4', self.s4)
            ('path', self.path)
            self.f.read(12)
            self.path=self.read_c_str(self.f)
            ('path', self.path)
            import binascii
            data = self.f.read(14)
            (len(data), binascii.hexlify(data))
        elif self.s1==10:
            # bitmap?
            import binascii
            self.s2=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(4)))
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            (binascii.hexlify(self.f.read(6 * 16 - 6)))
            self.s4=self.read_c_str(self.f)
            self.path=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(12)))
            (self.read_c_str(self.f))
            (binascii.hexlify(self.f.read(10)))
        elif self.s1==9:
            import binascii
            self.s2=self.read_c_str(self.f)
            print (self.s2)
            (binascii.hexlify(self.f.read(4)))
            self.s3=self.read_c_str(self.f)
            print (self.s3)
            self.id = struct.unpack(b"<L", self.f.read(4))[0]
            print (self.id)
            print(binascii.hexlify(self.f.read(6 * 16 - 6)))
            #print(self.read_c_str(self.f))
            #self.s4=self.read_c_str(self.f)
            #self.path=self.read_c_str(self.f)
            #print(binascii.hexlify(self.f.read(12)))
            #print(binascii.hexlify(self.f.read(10)))
            
        else:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.f.read(6 * 16 - 2)
            self.s4=self.read_c_str(self.f)
            self.path=self.read_c_str(self.f)

    def __str__(self):
        import binascii
        return (''.join(['\t' for i in range(self.level)]) + "(MxOb Chunk) '{0}' {1} id: {2} {3} {4} {5} {6} {7}".format(self.signature, self.block_size, self.id, self.s1, self.s2, self.s3, self.s4, self.path ))

class MxSt(ParentChunk):
    """ 
    MxSt (Set) contains of MxOb (object) and List (MxDa) (data)
    """

    def __init__(self, chunk, f):
        super(MxSt, self).__init__(f)

        self.block_size = chunk.block_size
        self.signature = chunk.signature
        self.data = chunk.data
        self.level = chunk.level
        self.parent = chunk.parent

        subchunk_iter = self.subchunks()

    def __str__(self):
        import binascii
        return (''.join(['\t' for i in range(self.level)]) + "(MxSt Chunk) {0}".format(binascii.hexlify(self.data[:40])))# {0} {1} {2} {3}".format(self.s1, self.s2, self.s3, binascii.hexlify(self.s3)))

class RIFF(ParentChunk):
    def __init__(self, f):
        super(RIFF, self).__init__(f)

        HEADER = b"<4sL"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        (self.signature, self.block_size) = (struct.unpack(HEADER,data))

        HEADER = b"<4s"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        (self.form_type) = (struct.unpack(HEADER,data))

    def __str__(self):
        return (''.join(['\t' for i in range(self.level)]) + "(RIFF Chunk) {0}".format(self.form_type))

class List(ParentChunk):
    def __init__(self, chunk, f):
        super(List, self).__init__(f)

        self.block_size = chunk.block_size
        self.signature = chunk.signature
        self.data = chunk.data
        self.level = chunk.level
        self.parent = chunk.parent

        HEADER = b"<4s"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        (self.list_type) = (struct.unpack(HEADER,data))

        if self.list_type[0]==b'MxDa':
            pass

        if self.list_type[0]==b'MxCh':
            data = self.f.read(4)
            
            if data == b'RAND':
                # normally this is number of subobjects, but in this case it is RANDOM_3
                data += self.f.read(15)
            else:
                # number of subobjects
                ("List (MxCh) {0}".format(struct.unpack(b'<L', data)))
        pass
        """
        Chunk.__init__(self)
        self.block_size = chunk.block_size
        self.signature = chunk.signature
        self.data = chunk.data

        from StringIO import StringIO
        f = StringIO(chunk.data)

        CHUNK = "<4s"
        size = struct.calcsize(CHUNK)
        data = f.read(size)
        (type_) = (struct.unpack(CHUNK,data))
        print ("type", type_)
        
        container = Container(f)
        print ("list", str(container))
        for subchunk in container.subchunks():
            print (subchunk)
        """
    def __str__(self):
        return ''.join(['\t' for i in range(self.level)]) + "List ('{0}'): {1}".format(self.list_type, self.block_size, self.signature)

