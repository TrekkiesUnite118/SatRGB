#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""====================================================="""
##  satrgb.py                                   14 Jan 2018
##  extract RGB images from Saturn files

##  @ Doyousketch2
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
""" required  ========================================="""
##  you'll need imagemagick.  Try your package manager or
##  https://www.imagemagick.org/script/download.php

##  you'll need easygui, depending on your OS:
##        sudo pip3 install easygui
##        sudo python3 -m pip install easygui
##        py -m pip install easygui

##  you might need the tkinter module
##        sudo apt-get install python-tk python3-tk
""" libs  ============================================="""
import os                         ##  commandline utilities
from sys import exit
import easygui as eg           ##  Graphical User Interface
from binascii import hexlify   ##  convert bytes into ASCII
""" script  ============================================"""

def convert( img, outputpath ):
  with open( img, 'rb' ) as data:
    head, tail = os.path .split( img )
    root, ext  = os.path .splitext( tail )

    Identifier  = data .read(0x10)
    ID  = Identifier .split(b'\x00')[0] .split(b'\xFF')[0] .split(b'/')[0]

    SEGA2D   = b'SEGA_32BIT2DSCR\x1A'  ##  standard scroll data format
    DGT      = b'DIGITIZER 3 Ver2'     ##  index color mode
    RGB      = b'SEGA 32BITGRAPH\x1A'  ##  RGB color mode - 8 bit
    SX2D     = b'Sega Super32X 2D'     ##  32X scroll data format
    SEGA3D   = b'SEGA 3D'  ##  unused, but there's the header anyway
    DGT2PP   = b'PP'    ##  Packed Pixel  handles 32,768 colors
    DGT2DC   = b'DC'    ##  Direct Color
    DGT2RLE  = b'RL'    ##  RunLength Encoding
    FILM     = b'FILM'  ##  Cinepack Codec

    ini  = ID[:2]
    if ini == DGT2PP or ini == DGT2DC or ini == DGT2RLE:
      ID  = ini

    if ID == SEGA2D:
      print( 'skipping  {}  SEGA2D scroll data format'.format( tail ) )

    elif ID == DGT:
      print( 'skipping  {}  DGT index color mode'.format( tail ) )

    elif ID == RGB:
      data .read(0x4)  ##  discard 0xFFFF FFFF
      data .read(0x4)  ##  discard 0x0000 0000

      w  = hexlify( data .read(0x02) )
      h  = hexlify( data .read(0x02) )

      offset  = 256
      width   = int( w, 16 )
      height  = int( h, 16 )
      output  = '{}.png'.format( root )

      args = [ 'convert ',
               '-depth 8 ',
               '-endian MSB '
               '-size {}x{}+{} '.format( width, height, offset ) ]
      call  = '' .join( args )
      inner  = 'RGB:{} '.format( img )
      outer  = os.path .join( outputpath, output )
      print( '{}\n{}\n{}\n'.format( call, inner, outer ) )
      os .system( call + inner + outer )
      ##  convert -depth 8 -endian MSB -size 144x192+256
      ##  rgb:inpath/input.rgb  outpath/output.png

    elif ID == SX2D:
      print( 'skipping  {}  Sega Super32X 2D scroll data'.format( tail ) )

    elif ID == DGT2PP:
      print( 'skipping  {}  DGT2 PP - Packed Pixel data'.format( tail ) )

    elif ID == DGT2DC:
      print( 'skipping  {}  DGT2 DC - Direct Color data'.format( tail ) )

    elif ID == DGT2RLE:
      print( 'skipping  {}  DGT2 RL - Run Length Encoding'.format( tail ) )

    elif ID == FILM:
      print( 'skipping  {}  Cinepak Codec video'.format( tail ) )

    else:
      if len(ID) < 1:  ##  don't bother printing a blank 0x00 or 0xFF header
        print( 'skipping  {}'.format( tail ) )
      else:
        print( 'skipping  {}  header: {}'.format( tail, ID ) )


def main():
  info  = 'Convert Sega Saturn RGB images to PNG'
  title  = 'satrgb'

  choice  = eg.buttonbox( info, title, ['one file', 'entire directory'] )

  if choice == 'one file':
    imagefile  = eg.fileopenbox( 'choose image', title )
    if imagefile is None:  exit()
    else:
      outputdir  = eg.diropenbox( 'choose output dir', title )
      if outputdir is None:  exit()
      else:
        convert( imagefile, outputdir )

  elif choice == 'entire directory':
    directory  = eg.diropenbox( 'choose dir', title )
    if directory is None:  exit()
    else:
      outputdir  = eg.diropenbox( 'choose output dir', title )
      if outputdir is None:  exit()
      else:
        for name in os .listdir( directory ):
          obj  = os.path .join( directory, name )
          if os.path .isfile( obj ):
            convert( obj, outputdir )
  else:
    exit()

main()

""" eof  ==============================================="""
