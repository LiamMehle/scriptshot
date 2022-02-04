# scriptshot
A configurable python script that takes screenshots in the in the background.

## What?
This is (as mentioned above) a script intended to take screenshots of a game when action is detected in the form of a left-click or similar button press/mouse movement/action.

## Why?
So the shots don't seem posed or "set up", but instead look and arise organically as a match or operation unfolds.

## .. why a github repo?
This started out as a script of about 20 LoC that promptly balooned in scope and complexity.
As this project grew, version control seemed less and less of a waste of time.
The main goals are:
- take screenshots when in game action is detected over a long period of time.
- have it be configurable via source code, even for users with no knowledge of Python and possibly programming.

# Installation:

prerequisites: a python interpreter, prefferably CPython

currently: put the scripts *somewhere* and edit `USER` and/or `SCREENSHOT_DIR` at the top of `scriptshot.py` to the desired output path.
To make sure the reuqired python modules are installed, run `py installer.py`.
Afterwards, running `py scriptshot.py` directly will suffice.

# Uninstall:
run `py uninstall.py`
The screenshots will remain.
