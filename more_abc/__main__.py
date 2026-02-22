from argparse import ArgumentParser

from . import __all__, version

def main():
    parser = ArgumentParser(
        prog="python -m more_abc",
        description="more_abc — an extension of the abc module.",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"more_abc {version}",
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="list all public symbols",
    )
    args = parser.parse_args()

    if args.list:
        for name in sorted(__all__):
            print(name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
