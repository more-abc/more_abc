from sys import argv

from . import version

def main():
    # Let's try one first.
    if len(argv) > 1 and (argv[1] == "-v" or argv[1] == "-version"):
        print(version)

if __name__ == "__main__":
    main()
