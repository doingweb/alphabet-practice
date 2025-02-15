'''
Help Finn practice the alphabet
'''

import board
import displayio
import random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
from adafruit_pybadger import pybadger

print("LOVE YOU FINN! 🐴")

DISPLAY = board.DISPLAY
FONTS = [
  bitmap_font.load_font('/fonts/OldStandardTT-Bold-100.bdf'),
  bitmap_font.load_font('/fonts/IndieFlower-Regular-100.bdf'),
  bitmap_font.load_font('/fonts/LibreBaskerville-Bold-100.bdf'),
  bitmap_font.load_font('/fonts/Mali-SemiBold-100.bdf'),
  bitmap_font.load_font('/fonts/PatrickHand-Regular-100.bdf'),
  bitmap_font.load_font('/fonts/Quicksand-SemiBold-100.bdf'),
]
PALETTE_SIZE = 2
ALPHABET_UPPERCASE = list(map(chr, range(ord('A'), ord('Z')+1)))
ALPHABET_LOWERCASE = list(map(chr, range(ord('a'), ord('z')+1)))
COLOR_PALETTES = [ # FG, BG
  (0x804600, 0xE0E0E0), (0xFFD700, 0x72420D), (0xE4F1FE, 0x386EA8), (0xAAAAAA, 0x000000),
  (0x0000FF, 0xFFFFFF), (0xC5EFF7, 0x168815), (0xECECEC, 0x88151A)
]

paletteIndex = 0
fontIndex = 0
letterIndex = 0
alphabet = ALPHABET_UPPERCASE

leftButton = Debouncer(lambda: pybadger.button.left == 0)
rightButton = Debouncer(lambda: pybadger.button.right == 0)
selectButton = Debouncer(lambda: pybadger.button.select == 0)
aButton = Debouncer(lambda: pybadger.button.a == 0)
bButton = Debouncer(lambda: pybadger.button.b == 0)

def displayLetter():
  letter = alphabet[letterIndex]
  palette = displayio.Palette(PALETTE_SIZE)
  palette[0] = COLOR_PALETTES[paletteIndex][1] # Background
  palette[1] = COLOR_PALETTES[paletteIndex][0] # Foreground

  backgroundBitmap = displayio.Bitmap(DISPLAY.width, DISPLAY.height, PALETTE_SIZE)
  background = displayio.TileGrid(backgroundBitmap, pixel_shader=palette)

  font = FONTS[fontIndex]

  textLabel = label.Label(font, text=letter, color=palette[1])
  textLabel.anchor_point = (0.5, 0.5)
  textLabel.anchored_position = (DISPLAY.width / 2, DISPLAY.height / 2)

  group = displayio.Group()

  group.append(background)
  group.append(textLabel)

  DISPLAY.show(group)

  preloadLetter(alphabet[nextIndex()])
  preloadLetter(alphabet[previousIndex()])

def nextIndex():
  return letterIndex + 1 if letterIndex < len(alphabet) - 1 else 0

def previousIndex():
  return letterIndex - 1 if letterIndex > 0 else len(alphabet) - 1

  # TODO: Collect garbage after 50 or so letter changes? Got out-of-memory on 'I' when cycling through all fonts for each letter.

def forwardLetter():
  global letterIndex
  letterIndex = nextIndex()
  displayLetter()

def backLetter():
  global letterIndex
  letterIndex = previousIndex()
  displayLetter()

def switchLetterCase():
  global alphabet
  alphabet = ALPHABET_LOWERCASE if alphabet == ALPHABET_UPPERCASE else ALPHABET_UPPERCASE

def selectRandomPalette():
  if len(COLOR_PALETTES) < 2:
    return

  global paletteIndex
  previousPaletteIndex = paletteIndex

  while paletteIndex == previousPaletteIndex:
    paletteIndex = random.randint(0, len(COLOR_PALETTES) - 1)

def selectRandomFont():
  # TODO: Just go in sequence instead?
  if len(FONTS) < 2:
    return

  global fontIndex
  previousFontIndex = fontIndex

  while fontIndex == previousFontIndex:
    fontIndex = random.randint(0, len(FONTS) - 1)

def preloadLetter(letter):
  # TODO: Also preload next font? Both upper- and lower-case?
  label.Label(FONTS[fontIndex], text=letter)
  print(letter, end='')

displayLetter()

while True:
  leftButton.update()
  rightButton.update()
  selectButton.update()
  aButton.update()
  bButton.update()

  if leftButton.fell:
    backLetter()
  elif rightButton.fell:
    forwardLetter()

  if selectButton.fell:
    switchLetterCase()
    displayLetter()

  if aButton.fell:
    selectRandomPalette()
    displayLetter()

  if bButton.fell:
    selectRandomFont()
    displayLetter()
