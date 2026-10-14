import sys

from arcade import __version__
from arcade.main import main

if __name__ == "__main__":
    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"terminal-arcade {__version__}")
        sys.exit(0)
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!", file=sys.stderr)
        sys.exit(130)
    except EOFError:
        print("\nGoodbye!", file=sys.stderr)
        sys.exit(0)
