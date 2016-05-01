#!/bin/env python3
from ui.userInterface import UserInterface
from lib.top30Creator import Top30Creator

import sys

if __name__ == "__main__":
    if "--no-gui" in sys.argv:
        creator.create_rundown(30, 21, "")
    else:
        UserInterface.run()
