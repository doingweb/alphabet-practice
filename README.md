Alphabet Practice for Finn 💕
=============================

Connect to the remote console/REPL
----------------------------------

```console
screen -S pybadge /dev/tty.usbmodem14101 115200
```

Pretty sure the device name won't change.

Send it to the pybadge
----------------------

```console
cp main.py /Volumes/CIRCUITPY
```

Add/change font(s)
------------------

Open FontForge:

```console
/Applications/FontForge.app/Contents/MacOS/FontForge ~/Downloads/Alphabet\ fonts/Old_Standard_TT/OldStandardTT-Bold.ttf
```

1. Copy out the letter glyphs and paste into a new font.
2. Run _Bitmap Strikes Available..._ (`cmd+shift+B`) and set pixel size to `100`.
3. Run _Regenerate Bitmap Glyphs..._ (`cmd-B`) and keep pixel size to `100`.
4. Run _Generate Fonts..._ (`cmd-shift-G`) and:
   1. Pick the `fonts` directory in this project
   2. Select `No Outline Font`
   3. Select `BDF`
   4. Ignore _Options_
   5. Ensure the size box is `100`
   6. Click `Generate`
   7. `Guess` the BDF Resolution
   8. Hope it doesn't get into that stupid box dismiss loop thing

Copy it over:

```console
cp -R fonts /Volumes/CIRCUITPY
```
