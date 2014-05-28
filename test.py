from lego_extract import RIFF
from glob import glob
import sys

if __name__ == '__main__':
    for path in glob(sys.argv[1]): #$'/Users/remco/Downloads/documents-export-2014-05-13/NOCD.SI'):
        with open(path, 'r') as f:
            print ("Extracting {0}".format(path))
            riff = RIFF(f)
            #container = Container (f)
            
            print(riff)
            print ("Chunks:")

            for subchunk in riff.subchunks():
                print (subchunk)
                #print (subchunk.data)
