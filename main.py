'''
Help Finn practice the alphabet
'''

import board
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
from adafruit_pybadger import pybadger

print("LOVE YOU FINN! 🐴")

DISPLAY = board.DISPLAY
FONT = bitmap_font.load_font('/fonts/OldStandardTT-Bold-100.bdf')
PALETTE_SIZE = 2
ALPHABET_UPPERCASE = list(map(chr, range(ord('A'), ord('Z')+1)))
ALPHABET_LOWERCASE = list(map(chr, range(ord('a'), ord('z')+1)))

fgColor = 0x0000FF
bgColor = 0xFFFFFF
letterIndex = 0
alphabet = ALPHABET_UPPERCASE

leftButton = Debouncer(lambda: pybadger.button.left == 0)
rightButton = Debouncer(lambda: pybadger.button.right == 0)
selectButton = Debouncer(lambda: pybadger.button.select == 0)

def displayLetter():
  letter = alphabet[letterIndex]
  palette = displayio.Palette(PALETTE_SIZE)
  palette[0] = bgColor # Background
  palette[1] = fgColor # Foreground

  backgroundBitmap = displayio.Bitmap(DISPLAY.width, DISPLAY.height, PALETTE_SIZE)
  background = displayio.TileGrid(backgroundBitmap, pixel_shader=palette)

  text = letter
  textLabel = label.Label(FONT, text=text, color=palette[1])
  textLabel.anchor_point = (0.5, 0.5)
  textLabel.anchored_position = (DISPLAY.width / 2, DISPLAY.height / 2)

  group = displayio.Group()

  group.append(background)
  group.append(textLabel)

  DISPLAY.show(group)

def goToLetter(newIndex):
  global letterIndex
  letterIndex = newIndex
  displayLetter()

def forwardLetter():
  if letterIndex == len(alphabet) - 1:
    goToLetter(0)
  else:
    goToLetter(letterIndex + 1)

def backLetter():
  if letterIndex == 0:
    goToLetter(len(alphabet) - 1)
  else:
    goToLetter(letterIndex - 1)

def switchLetterCase():
  global alphabet
  alphabet = ALPHABET_LOWERCASE if alphabet == ALPHABET_UPPERCASE else ALPHABET_UPPERCASE
  displayLetter()

displayLetter()

while True:
  leftButton.update()
  rightButton.update()
  selectButton.update()

  if leftButton.fell:
    backLetter()
  elif rightButton.fell:
    forwardLetter()

  if selectButton.fell:
    switchLetterCase()
