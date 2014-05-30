from lego_extract import RIFF, MxSt, MxOb, MxCh
from glob import glob
import struct
from StringIO import StringIO
import sys
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                    format='%(message)s',
                    handlers=[logging.StreamHandler()])

    for path in glob(sys.argv[1]): #$'/Users/remco/Downloads/documents-export-2014-05-13/NOCD.SI'):
        """
        with open(path, 'r') as f:
            print ("Extracting {0}".format(path))
            # DUMP
            riff = RIFF(f)
            #container = Container (f)
            
            print(riff)
            print ("Chunks:")

            for subchunk in riff.subchunks():
                logger.info (subchunk)
                #print (subchunk.data)
        """
        with open(path, 'r') as f:
            print ("Extracting {0}".format(path))
            # Extract
            riff = RIFF(f)
            #container = Container (f)
            
            print(riff)
            print ("Chunks:")

            subchunk_iter = riff.subchunks()
            for subchunk in subchunk_iter:
                #logger.info (subchunk)

                if isinstance(subchunk, MxSt):
                    d = {}
                    d2 = {}
                    print ("Set")
                    subchunk_iter2 = subchunk.subchunks()
                    mxob = subchunk_iter2.next()
                    d[mxob.id]=mxob
                    d2[mxob.id]=[]
                    print (">>>>", str(mxob))
                    for o in mxob.subchunks():
                        if isinstance(o, MxOb):
                            d[o.id]=o
                            d2[o.id]=[]
                        print (o)

                    l = subchunk_iter2.next()
                    print (l)
                    for o in l.subchunks():
                        print (o)
                        if isinstance(o, MxCh):
                            d2[o.id].append(o)
                    print (d)
                    print (d2)
                    for b in d.keys():
                        print (b)
                        mxob = d[b] 
                        print (mxob)
                        if mxob.s1==4:
                            #wav
                            x = d2[b][0]

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

                            for x in d2[b][1:]:
                                w.writeframesraw(x.data[16:])

                            w.close()
                        elif mxob.s1==10:
                            #f.write("BM")
                            # bitmap meta data
                            x = d2[b][0]
                            """
                            000080020000c4000000010008000000000000ea0100130b0000130b00000000000000000000ff00ff0000008000008000000080800080000000800080008080000080808000
                            000080020000c4000000010008000000000000ea0100130b0000130b00000000000000000000ff00ff0000008000008000000080800080000000800080008080000080808000
                            00003900000013000000010008000000000074040000130b0000130b00000000000000000000ff00ff0000008000008000000080800080000000800080008080000080808000
                            """
                            data = StringIO(x.data[14:])

                            import binascii
                            print (binascii.hexlify(x.data[14:]))
                            # http://en.wikipedia.org/wiki/BMP_file_format
                            header_size = struct.unpack('<L', data.read(4))[0]
                            width = struct.unpack('<L', data.read(4))[0]
                            height = struct.unpack('<L', data.read(4))[0]
                            number_of_color_planes = struct.unpack('<H', data.read(2))[0]
                            number_of_bits_per_pixel = struct.unpack('<H', data.read(2))[0]
                            compression = struct.unpack('<L', data.read(4))[0]
                            image_size = struct.unpack('<L', data.read(4))[0]
                            hor_res = struct.unpack('<L', data.read(4))[0]
                            vert_res = struct.unpack('<L', data.read(4))[0]
                            colors_in_palette = struct.unpack('<L', data.read(4))[0]
                            important_colors = struct.unpack('<L', data.read(4))[0]

                            print ("Header size {0} Width {1} Height {2} nofcp {3} nobpp {4} com {5} size {6} hor {7} vert {8} pal {9} impo {10}"
                                        .format(header_size, width, height, number_of_color_planes, number_of_bits_per_pixel, image_size, compression, hor_res, vert_res, colors_in_palette, important_colors))


                            """
                            w = StringIO()

                            for x in d2[b][1:]:
                                w.write(x.data[14:])
                                import binascii
                                #logger.info(binascii.hexlify(x.data[:80]))

                            import PIL
                            import os
                            import PIL.Image
                            import math
                            image_data =  w.getvalue()
                            image_data = image_data #+ '\00\00\00\00\00\00\00\00\00'

                            print ("Width {0}x{1} {2} {3}".format(width, height, len(image_data), math.sqrt(len(image_data))))
                            try:
                                image = PIL.Image.frombytes('RGBA', (width/2, height/2), image_data, 'raw')
                                image.save('/tmp/lego/' + str(mxob.id) + '_' + os.path.basename(mxob.s3) + ".gif")
                            except Exception, exc:
                                print ("Image", exc)
                            """
                            with open('/tmp/lego/' + str(mxob.id) + '_' + os.path.basename(mxob.s3) + ".bmp", 'wb') as f:
                                f.write('BM')
                                f.write('\00\00\00\00')
                                f.write('\00\00')
                                f.write('\00\00')
                                f.write(struct.pack('<L', len(d2[b][0].data[14:])))
                                for x in d2[b]:
                                    f.write(x.data[14:])
                    print ("<<<<", str(mxob))
                
                #print (subchunk.data)
