from __future__ import print_function
import struct
import sys
from StringIO import StringIO
import logging

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
            if (c=='\00'):
                break
            s = s + c #self.f.read(1)

        return (s)

    def subchunks(self):
        SUBCHUNK = "<4sL"
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
            #logger.debug ("{0} {1} {2}".format(subchunk.signature, subchunk.block_size, binascii.hexlify(subchunk.data[:50])))

            # round up to even word boundary
            if (subchunk.block_size % 2==1):
                    self.f.read(1)

            if (subchunk.signature=='LIST'):
                p = List(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                #print (p)
                for x in p.subchunks():
                    #print (x)
                    yield x
            elif (subchunk.signature=='MxDa'):
                # Data?
            elif (subchunk.signature=='MxOb'):
                p = MxOb(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                #print ("{0} >>> ".format(p))
                # yield subobjects
                yield p

                for x in p.subchunks():
                    #logger.debug("BLABLA Self: {0} Sub: {1} Parent: {2}".format(str(p), str(x), str(self.parent)))
                    yield x
                #print ("<<< {0}".format(p))
            elif (subchunk.signature=='MxCh'):
                p = MxCh(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                yield p
                pass
            elif (subchunk.signature=='MxSt'):
                p = MxSt(subchunk, StringIO(subchunk.data))
                logger.debug(p)
                #logger.info("found stream")
                #logger.debug ("{0} >>> ".format(p))
                iter_subchunks = p.subchunks()
                mxob = iter_subchunks.next()

                #logger.info(">>> exporting object1 {0}".format(mxob))
                #logger.info("exporting object {0} {1} {2} length: {3}".format(mxob.s1, mxob.id, mxob.s3, len(mxob.data)))

                if mxob.s1==4:
                    #wav
                    x = iter_subchunks.next()

                    # portions thanks to LIME
                    try:
                        import binascii
                        #logger.info(binascii.hexlify(x.data[0:40]))
                        #logger.info(binascii.hexlify(x.data[18:20]))
                        data = StringIO(x.data[16:])
                        data.read(2)
                        bitrate1 = struct.unpack('<H', data.read(2))[0]
                        data.read(2)
                        bitrate2 = struct.unpack('<H', data.read(2))[0]
                        data.read(2)
                        idk = struct.unpack('<H', data.read(2))[0]
                        bits = struct.unpack('<H', data.read(2))[0]
                        logger.info ("Audio format might be %dHz or %dHz, with %d bits\n" % ( bitrate1, bitrate2, bits))
                    except Exception, exc:
                        logger.error(exc)
                    
                    import os
                    logger.info("Exporting wav to " + '/tmp/lego/' + os.path.basename(mxob.s3) + '.' + mxob.ext)

                    import wave
                    w = wave.open('/tmp/lego/' + str(mxob.id) + '_' + os.path.basename(mxob.s3) + ".wav", 'wb')
                    w.setnchannels(1)
                    w.setframerate(bitrate1)
                    w.setsampwidth(bits / 8)

                    for x in iter_subchunks:
                        w.writeframesraw(x.data[16:])

                    w.close()
                elif mxob.s1==10:
                        #f.write("BM")
                        # bitmap meta data
                        x = iter_subchunks.next()

                        data = StringIO(x.data[16:])

                        import binascii
                        #print (binascii.hexlify(x.data))

                        w = StringIO()

                        for x in iter_subchunks:
                            w.write(x.data[16:])
                            import binascii
                            #logger.info(binascii.hexlify(x.data[:80]))

                        import PIL
                        import os
                        import PIL.Image
                        image = PIL.Image.frombytes('RGBA', (160, 120), w.getvalue(), 'raw')
                        image.save('/tmp/lego/' + str(mxob.id) + '_' + os.path.basename(mxob.s3) + ".gif")
                elif mxob.s1==7:
                    #print (">>> ANIMATION (7)")
                    for x in iter_subchunks:
                        import binascii
                        #logger.debug(binascii.hexlify(x.data[:80]))
                    #print ("<<< ANIMATION (7)")

                else:
                    with open('/tmp/lego/' + str(mxob.id) + '.' + mxob.ext, 'wb') as f:
                        for x in iter_subchunks:
                            f.write(x.data[15:])
                            import binascii
                            logger.debug(str(x))
                            #logger.debug(binascii.hexlify(x.data[:80]))
                #logger.debug("<<< {0}".format(p))

                #logger.info("<<< exporting object {0} {1} {2}".format(mxob.s1, mxob.id, mxob.s3))
            elif (subchunk.signature=='pad '):
                #print ("Skipping padding")
                #logger.debug("Skipping padding")
                pass
            else:
                logger.debug(subchunk)
                yield subchunk

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
        (self.mode, self.id_) = struct.unpack("<hL", self.f.read(6))
        
        if self.mode == 0: 
            with open("/tmp/{0}.exp".format(self.id_), 'w') as w:
                w.write('BM')
                w.write(chunk.data[6:])
        elif self.mode == 16: 
            with open("/tmp/{0}.exp".format(self.id_), 'a+b') as w:
                w.write(chunk.data[6:])
        elif self.mode == 2: 
            with open("/tmp/{0}.exp".format(self.id_), 'a+b') as w:
                w.write(chunk.data[6:])

        self.data = chunk.data

    def __str__(self):
        import binascii
        return (''.join(['\t' for i in range(self.level)]) + "(MxCh Chunk) Parent: {0} {1} {2} id: {3} {4} {5}".format(self.parent, self.signature, self.block_size, self.id_, self.mode, binascii.hexlify(self.data[16:50]) ))

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
        HEADER = "<H"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        self.s1 = (struct.unpack(HEADER,data))[0]
        self.ext='unknown'

        import binascii

        if self.s1==4:
            # WAV?
            self.ext = 'wav'
            self.s2=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(4)))
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack("<L", self.f.read(4))[0]
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
            self.id = struct.unpack("<L", self.f.read(4))[0]
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
            self.id = struct.unpack("<L", self.f.read(4))[0]
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
            self.id = struct.unpack("<L", self.f.read(4))[0]
            self.f.read(6 * 16 - 6 )
            self.path=self.read_c_str(self.f)
            #import binascii
            #print (binascii.hexlify(self.f.read(10)))
        elif self.s1==7:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack("<L", self.f.read(4))[0]
            (binascii.hexlify(self.f.read(6 * 16 - 8 )))
            data = (binascii.hexlify(self.f.read(2 )))
            if not data == '0000':
                self.s4 = self.read_c_str(self.f)

        elif self.s1==11:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack("<L", self.f.read(4))[0]
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
            self.ext = 'bmp'
            import binascii
            self.s2=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(4)))
            self.s3=self.read_c_str(self.f)
            self.id = struct.unpack("<L", self.f.read(4))[0]
            (binascii.hexlify(self.f.read(6 * 16 - 6)))
            self.s4=self.read_c_str(self.f)
            self.path=self.read_c_str(self.f)
            (binascii.hexlify(self.f.read(12)))
            (self.read_c_str(self.f))
            (binascii.hexlify(self.f.read(10)))
        else:
            self.s2=self.read_c_str(self.f)
            self.f.read(4)
            self.s3=self.read_c_str(self.f)
            self.f.read(6 * 16 - 2)
            self.s4=self.read_c_str(self.f)
            self.path=self.read_c_str(self.f)
        """
        self.f.read(3*4)
        
        HEADER = "<4s"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        (s) = (struct.unpack(HEADER,data))
        print (s)
        """ 
    def __str__(self):
        import binascii
        return (''.join(['\t' for i in range(self.level)]) + "(MxOb Chunk) '{0}' {1} id: {2} {3} {4} {5} {6} {7}".format(self.signature, self.block_size, self.id, self.s1, self.s2, self.s3, self.s4, self.path ))

class MxSt(ParentChunk):
    def __init__(self, chunk, f):
        super(MxSt, self).__init__(f)

        self.block_size = chunk.block_size
        self.signature = chunk.signature
        self.data = chunk.data
        self.level = chunk.level
        self.parent = chunk.parent

        subchunk_iter = self.subchunks()
        """
        data = StringIO(subchunk_iter.next()).data
    
        data.seek(18, 1)
        bitrate1 = struct.unpack('<H', data.read(2))[0]
        data.seek(2, 1)
        bitrate2 = struct.unpack('<H', data.read(2))[0]
        data.seek(2, 1)
        idk = struct.unpack('<H', data.read(2))[0]
        bits = struct.unpack('<H', data.read(2))[0]

        print ("\nAudio format might be %dHz or %dHz, with %d bits\n" % (        bitrate1, bitrate2, bits))
        """
        """
        i = 0
        for subchunk in subchunk_iter:
            print ("BLA", subchunk)
            if i==1:
                print ("REMC")
                data = StringIO(subchunk.data)
            
                data.seek(18, 1)
                bitrate1 = struct.unpack('<H', data.read(2))[0]
                data.seek(2, 1)
                bitrate2 = struct.unpack('<H', data.read(2))[0]
                data.seek(2, 1)
                idk = struct.unpack('<H', data.read(2))[0]
                bits = struct.unpack('<H', data.read(2))[0]

                print ("\nAudio format might be %dHz or %dHz, with %d bits\n" % (        bitrate1, bitrate2, bits))
            i = i +1
        """ 
        """
        HEADER = "<4sL2x29s"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        (self.s1, self.s2, self.s3) = (struct.unpack(HEADER,data))
        """
    def __str__(self):
        import binascii
        return (''.join(['\t' for i in range(self.level)]) + "(MxSt Chunk) {0}".format(binascii.hexlify(self.data[:40])))# {0} {1} {2} {3}".format(self.s1, self.s2, self.s3, binascii.hexlify(self.s3)))

class RIFF(ParentChunk):
    def __init__(self, f):
        super(RIFF, self).__init__(f)

        HEADER = "<4sL"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        (self.signature, self.block_size) = (struct.unpack(HEADER,data))

        HEADER = "<4s"
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

        HEADER = "<4s"
        size = struct.calcsize(HEADER)
        data = self.f.read(size)
        (self.list_type) = (struct.unpack(HEADER,data))

        if self.list_type[0]=='MxDa':
            pass

        if self.list_type[0]=='MxCh':
            # number of subobjects
            ("List (MxCh) {0}".format(struct.unpack('<L', self.f.read(4))))
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

