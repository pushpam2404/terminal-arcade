import sys

from arcade import __version__
from arcade.main import main

if __name__ == "__main__":
    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"terminal-arcade {__version__}")
        sys.exit(0)
    main()

