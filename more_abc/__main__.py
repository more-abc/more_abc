from argparse import ArgumentParser
import more_abc as _pkg

def main():
    parser = ArgumentParser(
        prog="python -m more_abc",
        description="more_abc — an extension of the abc module.",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"more_abc {_pkg.__version__}",
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="list all public symbols",
    )
    parser.add_argument(
        "-d", "--doc",
        metavar="SYMBOL",
        help="print the docstring of a public symbol",
    )
    args = parser.parse_args()

    if args.doc:
        obj = getattr(_pkg, args.doc, None)
        if obj is None:
            print(f"Symbol '{args.doc}' not found in more_abc.")
        elif obj.__doc__:
            print(obj.__doc__)
        else:
            print(f"'{args.doc}' has no docstring.")
    elif args.list:
        for name in sorted(_pkg.__all__):
            print(name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
   
