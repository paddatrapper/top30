#!/usr/bin/env python3
from handlers import UserInterface
from top30Creator import Top30Creator

import sys

def main():
    if "--no-gui" in sys.argv:
        creator = Top30Creator()
        creator.create_rundown(30, 21, "")
        creator.create_rundown(20, 11, "")
        reator.create_rundown(10, 2, "")
        reator.create_rundown(10, 1, "last-week")
    else:
        ui = UserInterface()
        ui.run()

if __name__ == "__main__":
    main()
