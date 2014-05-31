============
extract-riff
============

Extracts data (Music, Bitmaps, ...) for Lego Island RIFF files.

# description of the file format

## MxOb

## MxSt

## MxCh

## Mxda

## MxHd
Header

## MxOf


# known issues
* INFOMAIN.SI
* ACT2MAIN.SI

# contributors
* Tim 
* Remco (DutchCoders)

# usage
```
python ./test.py --extract --output "/tmp/lego/bla1/" "/Users/remco/Downloads/documents-export-2014-05-13/JUKEBOXW.SI"
python ./test.py --dump "/Users/remco/Downloads/documents-export-2014-05-13/JUKEBOXW.SI"
```

#sample output
```
    Chunk MxHd: Block size: 12 ->
    Chunk MxHd: Block size: 12 ->
    Chunk MxOf: Block size: 8 -> <
    Chunk MxOf: Block size: 8 -> <
    List ('('MxSt',)'): 393160
    List ('('MxSt',)'): 393160
        (MxSt Chunk) 4d784f62f2010000070000000000004e6f43445f4d6f766965000000000022000000000000000000
        (MxSt Chunk) 4d784f62f2010000070000000000004e6f43445f4d6f766965000000000022000000000000000000
            (MxOb Chunk) 'MxOb' 498 id: 0 7  NoCD_Movie None None
            (MxOb Chunk) 'MxOb' 498 id: 0 7  NoCD_Movie None None
                List ('('MxCh',)'): 378
                List ('('MxCh',)'): 378
                    (MxOb Chunk) 'MxOb' 170 id: 1 3  CDSpin1_Smk q:\lego\media\movies\CDSpin1.smk
                    (MxOb Chunk) 'MxOb' 170 id: 1 3  CDSpin1_Smk q:\lego\media\movies\CDSpin1.smk
                    (MxOb Chunk) 'MxOb' 183 id: 2 4  Iicx62In_Wave WAV q:\lego\Audio\Offscreen\In\Iicx62In.wav
                    (MxOb Chunk) 'MxOb' 183 id: 2 4  Iicx62In_Wave WAV q:\lego\Audio\Offscreen\In\Iicx62In.wav
            List ('('MxDa',)'): 353130
            List ('('MxDa',)'): 353130
                (MxCh Chunk) Parent: None MxCh 27150 id: 1 mode: 0 4b3240010000f000000022000000f0d8ffff00000000000000000000000000000000
                (MxCh Chunk) Parent: None MxCh 27150 id: 1 mode: 0 4b3240010000f000000022000000f0d8ffff00000000000000000000000000000000
                (MxCh Chunk) Parent: None MxCh 38 id: 2 mode: 0 0100112b00002256000002001000322601002c000000
                (MxCh Chunk) Parent: None MxCh 38 id: 2 mode: 0 0100112b00002256000002001000322601002c000000
                (MxCh Chunk) Parent: None MxCh 10222 id: 1 mode: 0 170000011916000b002828281814002a12130c0b002a17010500003333330015001f
                (MxCh Chunk) Parent: None MxCh 10222 id: 1 mode: 0 170000011916000b002828281814002a12130c0b002a17010500003333330015001f
                (MxCh Chunk) Parent: None MxCh 22064 id: 2 mode: 0 07001800200023002a002c0033002f001e001500120014001100100014001f002800
                (MxCh Chunk) Parent: None MxCh 22064 id: 2 mode: 0 07001800200023002a002c0033002f001e001500120014001100100014001f002800
Skipping padding
```

# references

* http://www.fileformat.info/format/riff/corion.htm
* http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Docs/RIFFNEW.pdf
* http://www.daubnet.com/en/file-format-riff
* http://www.fileformat.info/format/riff/egff.htm
* http://www.sonicspot.com/guide/wavefiles.html
* http://www.johnloomis.org/cpe102/asgn/asgn1/riff.html
* https://github.com/mathom/LIME
