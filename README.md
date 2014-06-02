============
extract-riff
============

Extracts data (Music, Bitmaps, ...) for Lego Island RIFF files.

# description of the file format

## MxOb
The MxOb describes the object. It contains an id, name and meta information.

## MxSt

## MxCh
The MxCh contains the object id it belongs to and the actual data.

## MxDa

## MxHd
The MxHd contains the header of the SI file.

## MxOf


# known issues
* INFOMAIN.SI (0x34dfffa should start at 0x034e0000, 6 bytes extra)
* ACT2MAIN.SI (0x1cbffd6, says it is length 0x22, but should be 0x26, or is should be rounded up or something, to 0x10000?)

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
Dumping ./NOCD.SI.
    Chunk MxHd: Block size: 12 ->
    Chunk MxOf: Block size: 8 -> <
    List ('('MxSt',)'): 393160
        (MxSt Chunk) 4d784f62f2010000070000000000004e6f43445f4d6f766965000000000022000000000000000000
            (MxOb Chunk) 'MxOb' 498 id: 0 7  NoCD_Movie None None
                List ('('MxCh',)'): 378
                    (MxOb Chunk) 'MxOb' 170 id: 1 3  CDSpin1_Smk q:\lego\media\movies\CDSpin1.smk
                    (MxOb Chunk) 'MxOb' 183 id: 2 4  Iicx62In_Wave WAV q:\lego\Audio\Offscreen\In\Iicx62In.wav
            List ('('MxDa',)'): 353130
                (MxCh Chunk) Parent: None MxCh 27150 id: 1 mode: 0 4b3240010000f000000022000000f0d8ffff00000000000000000000000000000000
                (MxCh Chunk) Parent: None MxCh 38 id: 2 mode: 0 0100112b00002256000002001000322601002c000000
                (MxCh Chunk) Parent: None MxCh 10222 id: 1 mode: 0 170000011916000b002828281814002a12130c0b002a17010500003333330015001f
                (MxCh Chunk) Parent: None MxCh 22064 id: 2 mode: 0 07001800200023002a002c0033002f001e001500120014001100100014001f002800
                (MxCh Chunk) Parent: None MxCh 9586 id: 1 mode: 0 c3d719004071a47e00a43aa0d80e00bf75becf5632008c1c56989b0160a8de01b682
                (MxCh Chunk) Parent: None MxCh 8506 id: 1 mode: 0 9955d2c10c00602a2b8e07a0eb183553bbcf0c80082da13f0b06405460359f0503c0
                (MxCh Chunk) Parent: None MxCh 6778 id: 1 mode: 0 996d8001d02afad17c39b013759288831ccb707706e997c95a092b5ecb0094b9e9e7
                (MxCh Chunk) Parent: None MxCh 3306 id: 1 mode: 0 67e40b63b28ea6ead483f2796180a52a569a44536a75b2ebe85b834e26d158412e85
                (MxCh Chunk) Parent: None MxCh 4450 id: 1 mode: 0 275b660000095300c0393dd8042f19cc1cab3dc835c9eb688701f0205d3f1c012e53
                (MxCh Chunk) Parent: None MxCh 6450 id: 1 mode: 0 271bc0000038470090540edb840350be87bac00080d1bcbdc30c0020d0eb2ae46454
                (MxCh Chunk) Parent: None MxCh 7682 id: 1 mode: 0 275b6600005ec63d00c0a2667300002f873e00405c2ff7c4850f00e095921e2a883e
                (MxCh Chunk) Parent: None MxCh 8430 id: 1 mode: 0 27da18008097714b1ddc0f00f03a2f0f00507e313a711b953c0079ac32edf4431e57
                (MxCh Chunk) Parent: None MxCh 8950 id: 1 mode: 0 c32f99020c0080b478b307002804b9e603003ce2850300d832ee00008bb16d3a71e3
                (MxCh Chunk) Parent: None MxCh 8070 id: 1 mode: 0 99e90c00200b0b0000ce110000e6fc3207c0cbb84b28130320ae531beecb00408b47
                (MxCh Chunk) Parent: None MxCh 22064 id: 2 mode: 0 ebad7bacffb273bd55c7c2df6cf8120ceb22a4314842c43d40404a380e2c2a25e514
                (MxCh Chunk) Parent: None MxCh 6042 id: 1 mode: 0 996d8001406b3578341e3a3f3a8110fdaa3e923863b03529c2b647fa968901caef54
                (MxCh Chunk) Parent: None MxCh 3322 id: 1 mode: 0 67e40b63cc243d45bd21d2c8000fca1d4b536af5e9b5311379eaa1c57ca1d4ca0b93
                (MxCh Chunk) Parent: None MxCh 5386 id: 1 mode: 0 275b660044577114b0306dca4e9f751d06fb63bdaa1f71181b0c80125c1089901aa7
                (MxCh Chunk) Parent: None MxCh 7602 id: 1 mode: 0 271bc000a0ae1f829d0e401fa19297bece00d834d1265a9e1900149d7e2f65bc0c00
                (MxCh Chunk) Parent: None MxCh 8706 id: 1 mode: 0 271a6600009925ab7a008089f6431c002e59d53a000360615cd601180008e44cb90f
                (MxCh Chunk) Parent: None MxCh 9550 id: 1 mode: 0 67c9146600005de7bf0f0010a1516c07209043a552070c80f2497f3cebc6000072a7
                (MxCh Chunk) Parent: None MxCh 9374 id: 1 mode: 0 c3d71900003b513f0052780ac576009a75689fad6400f441d156989b0160a8de01de
                (MxCh Chunk) Parent: None MxCh 8546 id: 1 mode: 0 9955901b660024d554561c0f401c8c9aa9dd6706409ebf6e6a9f6500d42e27dab360
                (MxCh Chunk) Parent: None MxCh 7050 id: 1 mode: 0 99d19229c000d82a8de11b6c9241abd09830aabb3d43030c8c9ca49b95fb1c001860
                (MxCh Chunk) Parent: None MxCh 4142 id: 1 mode: 0 c38f3803800b32816869f45a9049e52562ed4bc574c90040090ad79b832bcf7cee89
                (MxCh Chunk) Parent: None MxCh 22064 id: 2 mode: 0 14f4e5f879edc8ef45db92e03adbb3ce13d6c1d3adcc2dc947eae9f6d9b03fe77e17
                (MxCh Chunk) Parent: None MxCh 3854 id: 1 mode: 0 279a72064052254c01b4565e728eb7af0c033861b5103333c8f0ba5e9653b3f23457
                (MxCh Chunk) Parent: None MxCh 5086 id: 1 mode: 0 271bcc000038470010570ec7e200c4852d0e3380a1fa304dd804871900f0d0afce67
                (MxCh Chunk) Parent: None MxCh 6650 id: 1 mode: 0 279b330000cea9700000c7994d7f1e6e0700f072e025483a8380039030459f3be471
                (MxCh Chunk) Parent: None MxCh 6682 id: 1 mode: 0 27da1900400f0200c04bce2975703b00c0ebbcacc3a01357f20000a1620140a926cc
                (MxCh Chunk) Parent: None MxCh 7294 id: 1 mode: 0 c3ef1ad51900c06696e9007049fdab2d63007868d6e680320058bef73c8b3300b2f0
                (MxCh Chunk) Parent: None MxCh 7390 id: 1 mode: 0 c32f510a300080bacce60000e6b0fe0128aff11000c016db0e00d0c2cb3db5f90038
                (MxCh Chunk) Parent: None MxCh 6714 id: 1 mode: 0 99954c61068043e2d2ec072002b39491ba0383510ed9b8d9f42d13038076161d100c
                (MxCh Chunk) Parent: None MxCh 5286 id: 1 mode: 0 9945994174d5c38d11db1f9946679697c2f10279329a3ae90c40ab8c925f8d37cc00
                (MxCh Chunk) Parent: None MxCh 3250 id: 1 mode: 0 27663b83c6e48b2874619422a80759270775bfa9197966cf907264325726231f57f9
                (MxCh Chunk) Parent: None MxCh 5902 id: 1 mode: 0 271bc000a0aecc4600756d1a9337191c832cf0df6f8a83c15924038c4af0d4ac51bc
                (MxCh Chunk) Parent: None MxCh 9164 id: 2 mode: 0 9a0528067306a906e206c506c3067c064306d4056005f2045f04cd0321036302b401
                (MxCh Chunk) Parent: None MxCh 7718 id: 1 mode: 0 27baf214600024d50fc14e07a00f7e5f020320fd126da2e5990140d1acf84ba63b06
                (MxCh Chunk) Parent: None MxCh 8738 id: 1 mode: 0 271a6600009925ab7a00803c536c07804b56b50ec00058189775000600023953eec3
                (MxCh Chunk) Parent: None MxCh 9486 id: 1 mode: 0 67c9146600005de7bf0f0010a1516c0720d03f964a1d3000ca27fdf1ac1b0300c89d
                (MxCh Chunk) Parent: None MxCh 14 id: 1 mode: 2
                (MxCh Chunk) Parent: None MxCh 14 id: 2 mode: 2
                (MxCh Chunk) Parent: None MxCh 14 id: 0 mode: 2
```

# references

* http://www.fileformat.info/format/riff/corion.htm
* http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Docs/RIFFNEW.pdf
* http://www.daubnet.com/en/file-format-riff
* http://www.fileformat.info/format/riff/egff.htm
* http://www.sonicspot.com/guide/wavefiles.html
* http://www.johnloomis.org/cpe102/asgn/asgn1/riff.html
* https://github.com/mathom/LIME
