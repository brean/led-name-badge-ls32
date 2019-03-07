#! /usr/bin/python3
#
# (C) 2019 juergen@fabmail.org
#
# This is an upload tool for e.g.
# https://www.sertronics-shop.de/computer/pc-peripheriegeraete/usb-gadgets/led-name-tag-11x44-pixel-usb
# The font_11x44[] data was downloaded from such a device.
#
# Requires:
#  sudo apt-get install python3-usb
#
# Optional for image support:
#  sudo apt-get install python3-pil
#
# v0.1, 2019-03-05, jw  initial draught. HID code is much simpler than expected.
# v0.2, 2019-03-07, jw  support for loading bitmaps added.

import sys, os, array, time
import usb.core

__version = "0.2"

font_11x44 = (
  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  0x00, 0x38, 0x6c, 0xc6, 0xc6, 0xfe, 0xc6, 0xc6, 0xc6, 0xc6, 0x00,
  0x00, 0xfc, 0x66, 0x66, 0x66, 0x7c, 0x66, 0x66, 0x66, 0xfc, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0xc0, 0xc0, 0xc0, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0xfc, 0x66, 0x66, 0x66, 0x66, 0x66, 0x66, 0x66, 0xfc, 0x00,
  0x00, 0xfe, 0x66, 0x62, 0x68, 0x78, 0x68, 0x62, 0x66, 0xfe, 0x00,
  0x00, 0xfe, 0x66, 0x62, 0x68, 0x78, 0x68, 0x60, 0x60, 0xf0, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0xc0, 0xc0, 0xce, 0xc6, 0xc6, 0x7e, 0x00,
  0x00, 0xc6, 0xc6, 0xc6, 0xc6, 0xfe, 0xc6, 0xc6, 0xc6, 0xc6, 0x00,
  0x00, 0x3c, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x3c, 0x00,
  0x00, 0x1e, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0xcc, 0xcc, 0x78, 0x00,
  0x00, 0xe6, 0x66, 0x6c, 0x6c, 0x78, 0x6c, 0x6c, 0x66, 0xe6, 0x00,
  0x00, 0xf0, 0x60, 0x60, 0x60, 0x60, 0x60, 0x62, 0x66, 0xfe, 0x00,
  0x00, 0x82, 0xc6, 0xee, 0xfe, 0xd6, 0xc6, 0xc6, 0xc6, 0xc6, 0x00,
  0x00, 0x86, 0xc6, 0xe6, 0xf6, 0xde, 0xce, 0xc6, 0xc6, 0xc6, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0xfc, 0x66, 0x66, 0x66, 0x7c, 0x60, 0x60, 0x60, 0xf0, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xd6, 0xde, 0x7c, 0x06,
  0x00, 0xfc, 0x66, 0x66, 0x66, 0x7c, 0x6c, 0x66, 0x66, 0xe6, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0x60, 0x38, 0x0c, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0x7e, 0x7e, 0x5a, 0x18, 0x18, 0x18, 0x18, 0x18, 0x3c, 0x00,
  0x00, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0x6c, 0x38, 0x10, 0x00,
  0x00, 0xc6, 0xc6, 0xc6, 0xc6, 0xd6, 0xfe, 0xee, 0xc6, 0x82, 0x00,
  0x00, 0xc6, 0xc6, 0x6c, 0x7c, 0x38, 0x7c, 0x6c, 0xc6, 0xc6, 0x00,
  0x00, 0x66, 0x66, 0x66, 0x66, 0x3c, 0x18, 0x18, 0x18, 0x3c, 0x00,
  0x00, 0xfe, 0xc6, 0x86, 0x0c, 0x18, 0x30, 0x62, 0xc6, 0xfe, 0x00,

  # 'abcdefghijklmnopqrstuvwxyz'
  0x00, 0x00, 0x00, 0x00, 0x78, 0x0c, 0x7c, 0xcc, 0xcc, 0x76, 0x00,
  0x00, 0xe0, 0x60, 0x60, 0x7c, 0x66, 0x66, 0x66, 0x66, 0x7c, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x7c, 0xc6, 0xc0, 0xc0, 0xc6, 0x7c, 0x00,
  0x00, 0x1c, 0x0c, 0x0c, 0x7c, 0xcc, 0xcc, 0xcc, 0xcc, 0x76, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x7c, 0xc6, 0xfe, 0xc0, 0xc6, 0x7c, 0x00,
  0x00, 0x1c, 0x36, 0x30, 0x78, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x76, 0xcc, 0xcc, 0x7c, 0x0c, 0xcc, 0x78,
  0x00, 0xe0, 0x60, 0x60, 0x6c, 0x76, 0x66, 0x66, 0x66, 0xe6, 0x00,
  0x00, 0x18, 0x18, 0x00, 0x38, 0x18, 0x18, 0x18, 0x18, 0x3c, 0x00,
  0x0c, 0x0c, 0x00, 0x1c, 0x0c, 0x0c, 0x0c, 0x0c, 0xcc, 0xcc, 0x78,
  0x00, 0xe0, 0x60, 0x60, 0x66, 0x6c, 0x78, 0x78, 0x6c, 0xe6, 0x00,
  0x00, 0x38, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x3c, 0x00,
  0x00, 0x00, 0x00, 0x00, 0xec, 0xfe, 0xd6, 0xd6, 0xd6, 0xc6, 0x00,
  0x00, 0x00, 0x00, 0x00, 0xdc, 0x66, 0x66, 0x66, 0x66, 0x66, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x7c, 0xc6, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0x00, 0x00, 0xdc, 0x66, 0x66, 0x66, 0x7c, 0x60, 0x60, 0xf0,
  0x00, 0x00, 0x00, 0x7c, 0xcc, 0xcc, 0xcc, 0x7c, 0x0c, 0x0c, 0x1e,
  0x00, 0x00, 0x00, 0x00, 0xde, 0x76, 0x60, 0x60, 0x60, 0xf0, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x7c, 0xc6, 0x70, 0x1c, 0xc6, 0x7c, 0x00,
  0x00, 0x10, 0x30, 0x30, 0xfc, 0x30, 0x30, 0x30, 0x34, 0x18, 0x00,
  0x00, 0x00, 0x00, 0x00, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc, 0x76, 0x00,
  0x00, 0x00, 0x00, 0x00, 0xc6, 0xc6, 0xc6, 0x6c, 0x38, 0x10, 0x00,
  0x00, 0x00, 0x00, 0x00, 0xc6, 0xd6, 0xd6, 0xd6, 0xfe, 0x6c, 0x00,
  0x00, 0x00, 0x00, 0x00, 0xc6, 0x6c, 0x38, 0x38, 0x6c, 0xc6, 0x00,
  0x00, 0x00, 0x00, 0xc6, 0xc6, 0xc6, 0xc6, 0x7e, 0x06, 0x0c, 0xf8,
  0x00, 0x00, 0x00, 0x00, 0xfe, 0x8c, 0x18, 0x30, 0x62, 0xfe, 0x00,

  # '0987654321^ !"\0$%&/()=?` °\\}][{' + "@ ~ |<>,;.:-_#'+* "
  0x00, 0x7c, 0xc6, 0xce, 0xde, 0xf6, 0xe6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0xc6, 0x7e, 0x06, 0x06, 0xc6, 0x7c, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0xc6, 0x7c, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0xfe, 0xc6, 0x06, 0x0c, 0x18, 0x30, 0x30, 0x30, 0x30, 0x00,
  0x00, 0x7c, 0xc6, 0xc0, 0xc0, 0xfc, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0xfe, 0xc0, 0xc0, 0xfc, 0x06, 0x06, 0x06, 0xc6, 0x7c, 0x00,
  0x00, 0x0c, 0x1c, 0x3c, 0x6c, 0xcc, 0xfe, 0x0c, 0x0c, 0x1e, 0x00,
  0x00, 0x7c, 0xc6, 0x06, 0x06, 0x3c, 0x06, 0x06, 0xc6, 0x7c, 0x00,
  0x00, 0x7c, 0xc6, 0x06, 0x0c, 0x18, 0x30, 0x60, 0xc6, 0xfe, 0x00,
  0x00, 0x18, 0x38, 0x78, 0x18, 0x18, 0x18, 0x18, 0x18, 0x7e, 0x00,
  0x38, 0x6c, 0xc6, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x3c, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x18, 0x3c, 0x3c, 0x3c, 0x18, 0x18, 0x00, 0x18, 0x18, 0x00,
  0x66, 0x66, 0x22, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x7c, 0x04, 0x14, 0x18, 0x10, 0x10, 0x20,
  0x10, 0x7c, 0xd6, 0xd6, 0x70, 0x1c, 0xd6, 0xd6, 0x7c, 0x10, 0x10,
  0x00, 0x60, 0x92, 0x96, 0x6c, 0x10, 0x6c, 0xd2, 0x92, 0x0c, 0x00,
  0x00, 0x38, 0x6c, 0x6c, 0x38, 0x76, 0xdc, 0xcc, 0xcc, 0x76, 0x00,
  0x00, 0x00, 0x02, 0x06, 0x0c, 0x18, 0x30, 0x60, 0xc0, 0x80, 0x00,
  0x00, 0x0c, 0x18, 0x30, 0x30, 0x30, 0x30, 0x30, 0x18, 0x0c, 0x00,
  0x00, 0x30, 0x18, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x18, 0x30, 0x00,
  0x00, 0x00, 0x00, 0x7e, 0x00, 0x00, 0x7e, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x7c, 0xc6, 0xc6, 0x0c, 0x18, 0x18, 0x00, 0x18, 0x18, 0x00,
  0x18, 0x18, 0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x7c, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x7c,
  0x00, 0x10, 0x28, 0x28, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x80, 0xc0, 0x60, 0x30, 0x18, 0x0c, 0x06, 0x02, 0x00, 0x00,
  0x00, 0x70, 0x18, 0x18, 0x18, 0x0e, 0x18, 0x18, 0x18, 0x70, 0x00,
  0x00, 0x3c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x3c, 0x00,
  0x00, 0x3c, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x3c, 0x00,
  0x00, 0x0e, 0x18, 0x18, 0x18, 0x70, 0x18, 0x18, 0x18, 0x0e, 0x00,

  # "@ ~ |<>,;.:-_#'+* "
  0x00, 0x00, 0x3c, 0x42, 0x9d, 0xa5, 0xad, 0xb6, 0x40, 0x3c, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0xc0, 0x00, 0x00, 0x00,
  0x00, 0x76, 0xdc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x08, 0x08, 0x7c, 0x08, 0x08, 0x18, 0x18, 0x28, 0x28, 0x48, 0x18,
  0x00, 0x18, 0x18, 0x18, 0x18, 0x00, 0x18, 0x18, 0x18, 0x18, 0x00,
  0x00, 0x06, 0x0c, 0x18, 0x30, 0x60, 0x30, 0x18, 0x0c, 0x06, 0x00,
  0x00, 0x60, 0x30, 0x18, 0x0c, 0x06, 0x0c, 0x18, 0x30, 0x60, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x10, 0x20,
  0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x18, 0x18, 0x08, 0x10,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x00,
  0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff,
  0x00, 0x6c, 0x6c, 0xfe, 0x6c, 0x6c, 0xfe, 0x6c, 0x6c, 0x00, 0x00,
  0x18, 0x18, 0x08, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x18, 0x18, 0x7e, 0x18, 0x18, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x66, 0x3c, 0xff, 0x3c, 0x66, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,

  # "äöüÄÖÜß"
  0x00, 0xcc, 0xcc, 0x00, 0x78, 0x0c, 0x7c, 0xcc, 0xcc, 0x76, 0x00,
  0x00, 0xc6, 0xc6, 0x00, 0x7c, 0xc6, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0xcc, 0xcc, 0x00, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc, 0x76, 0x00,
  0xc6, 0xc6, 0x38, 0x6c, 0xc6, 0xfe, 0xc6, 0xc6, 0xc6, 0xc6, 0x00,
  0xc6, 0xc6, 0x00, 0x7c, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0xc6, 0xc6, 0x00, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0xc6, 0x7c, 0x00,
  0x00, 0x3c, 0x66, 0x66, 0x66, 0x7c, 0x66, 0x66, 0x66, 0x6c, 0x60,
)

charmap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
          'abcdefghijklmnopqrstuvwxyz' + \
          '0987654321^ !"\0$%&/()=?` °\\}][{' + \
          "@ ~ |<>,;.:-_#'+* " + "äöüÄÖÜß"

char_offset = {}
for i in range(len(charmap)):
  char_offset[charmap[i]] = 11 * i

def bitmap_char(ch):
  """ Returns a tuple of 11 bytes,
      ch = '_' returns (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255)
      The bits in each byte are horizontal, highest bit is left.
  """
  o = char_offset[ch]
  return font_11x44[o:o+11]

def bitmap_text(text):
  """ returns a tuple of (buffer, length_in_byte_columns_aka_chars)
  """
  buf = array.array('B')
  for c in text:
    buf.extend(bitmap_char(c))
  return (buf, len(text))


def bitmap_img(file):
  """ returns a tuple of (buffer, length_in_byte_columns)
  """
  from PIL import Image

  im = Image.open(file)
  print("loading bitmap from file %s -> (%d x %d)" % (file, im.width, im.height))
  if im.height != 11:
    sys.exit("%s: image height must be 11px. Seen %d" % (file, im.height))
  buf = array.array('B')
  cols = int((im.width+7)/8)
  for col in range(cols):
    for row in range(11):
      byte_val = 0
      for bit in range(8):
        bit_val = 0
        x = 8*col+bit
        if x < im.width && sum(im.getpixel( (x, row) )) > 384:
          bit_val = 1 << (7-bit)
        byte_val += bit_val
      buf.append(byte_val)
  im.close()
  return (buf, cols)


def bitmap(arg):
  """ if arg is a valid and existing path name, we load it as an image.
      Otherwise we take it as a string.
  """
  if os.path.exists(arg):
    return bitmap_img(arg)
  return bitmap_text(arg)


proto_header = (
  0x77, 0x61, 0x6e, 0x67, 0x00, 0x00, 0x00, 0x00, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
)

def header(lengths):
  """ lengths[0] is the number of chars of the first text
  """

  h = list(proto_header)
  for i in range(len(lengths)):
    h[17+2*i] = lengths[i]
  return h

if len(sys.argv) < 2:
  print("Usage:\n\n  %s Message1 [Message2 .. 8]\n" % (sys.argv[0]))
  sys.exit(0)

dev = usb.core.find(idVendor=0x0416, idProduct=0x5020)
if dev is None:
  print("No led tag with vendorID 0x0416 and productID 0x5020 found.")
  print("Connect the led tag and run this tool as root.")
  sys.exit(1)
if dev.is_kernel_driver_active(0):
  dev.detach_kernel_driver(0)
dev.set_configuration()
print("using [%s %s] bus=%d dev=%d" % (dev.manufacturer, dev.product, dev.bus, dev.address))



msgs = []
for arg in sys.argv[1:]:
  msgs.append(bitmap(arg))

buf = array.array('B')
buf.extend(header(map(lambda x: x[1], msgs)))

for msg in msgs:
  buf.extend(msg[0])

needpadding = len(buf)%64
if needpadding:
  buf.extend( (0,) * (64-needpadding) )

# print(buf)
for i in range(int(len(buf)/64)):
  time.sleep(0.1)
  dev.write(1, buf[i*64:i*64+64])

