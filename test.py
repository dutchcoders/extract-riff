from lego_extract import RIFF, MxSt, MxOb, MxCh
from glob import glob
import struct
from StringIO import StringIO
import sys
import logging
import argparse
import os

logger = logging.getLogger(__name__)

def dump(path):
    for path in args.paths:
        for filename in glob(path): #$'/Users/remco/Downloads/documents-export-2014-05-13/NOCD.SI'):
            with open(filename, 'r') as f:
                logger.info ("Extracting {0}.".format(filename))

                riff = RIFF(f)
                for subchunk in riff.subchunks():
                    logger.info (subchunk)

def extract(path, dest):
    for path in args.paths:
        for filename in glob(path): #$'/Users/remco/Downloads/documents-export-2014-05-13/NOCD.SI'):
            # extract
            import os
            with open(filename, 'r') as f:
                logger.info ("Dumping {0}.".format(filename))
                try:
                    os.mkdir(os.path.join(dest, os.path.basename(filename)))
                except OSError, exc:
                    pass

                riff = RIFF(f)

                d = {}
                d2 = {}

                subchunk_iter = riff.subchunks()
                for subchunk in subchunk_iter:
                    #logger.info (subchunk)
                    if isinstance(subchunk, MxOb):
                        d[subchunk.id]=subchunk

                    if isinstance(subchunk, MxCh):
                        if not subchunk.id in d2:
                            d2[subchunk.id] = []
                        d2[subchunk.id].append(subchunk)

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
                            data = StringIO(x.data[14:])
                            data.read(4)
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
                        w = wave.open(os.path.join(dest, os.path.basename(filename), "{0}_{1}.wav".format(str(mxob.id), os.path.basename(mxob.s3))), 'wb')
                        w.setnchannels(1)
                        w.setframerate(bitrate1)
                        w.setsampwidth(bits / 8)

                        for x in d2[b][1:]:
                            w.writeframesraw(x.data[14:])

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

                        logger.info ("Header size {0} Width {1} Height {2} nofcp {3} nobpp {4} com {5} size {6} hor {7} vert {8} pal {9} impo {10}"
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
                        import os
                        with open(os.path.join(dest, os.path.basename(filename), "{0}_{1}.bmp".format(str(mxob.id), os.path.basename(mxob.s3))), 'wb') as f:
                            f.write('BM')
                            # size
                            f.write('\00\00\00\00')
                            f.write('\00\00')
                            f.write('\00\00')
                            f.write(struct.pack('<L', len(d2[b][0].data[14:])))
                            for x in d2[b]:
                                f.write(x.data[14:])
                print ("<<<<", str(mxob))
                    
                    #print (subchunk.data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    handlers=[logging.StreamHandler()])

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='verbose', action='store_true', default=False)

    group = parser.add_argument_group(title='Extract contents')
    group.add_argument('--extract', '-e', help='Extract contents', action="store_true")
    group.add_argument('--output', help='Output folder')

    group = parser.add_argument_group(title='Dump contents')
    group.add_argument('--dump', '-d', help='Extract contents', action="store_true")

    parser.add_argument('paths', nargs='+', help='Path to SI files')

    args = parser.parse_args()

    if args.dump:
        dump(args.paths)
    elif args.extract:
        extract(args.paths, args.output)
    else:
        parser.print_help()
