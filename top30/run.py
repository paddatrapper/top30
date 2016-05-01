#!/bin/env python3
from handlers import UserInterface
from top30Creator import Top30Creator

import sys

def main():
    if "--no-gui" in sys.argv:
        creator.create_rundown(30, 21, "")
        creator.create_rundown(20, 11, "")
        creator.create_rundown(10, 2, "")
        creator.create_rundown(10, 1, "last-week")
    else:
        UserInterface.run()

if __name__ == "__main__":
    main()
