from argparse import ArgumentParser
import more_abc as _pkg
from .devtools import abc_logger

def main():
    abc_logger.debug("main() called")
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
    abc_logger.debug("args parsed: %r", args)

    if args.doc:
        abc_logger.debug("--doc requested: %r", args.doc)
        obj = getattr(_pkg, args.doc, None)
        if obj is None:
            abc_logger.debug("symbol %r not found", args.doc)
            print(f"Symbol '{args.doc}' not found in more_abc.")
        elif obj.__doc__:
            abc_logger.debug("printing docstring of %r", args.doc)
            print(obj.__doc__)
        else:
            abc_logger.debug("symbol %r has no docstring", args.doc)
            print(f"'{args.doc}' has no docstring.")
    elif args.list:
        abc_logger.debug("--list requested, %d symbols", len(_pkg.__all__))
        for name in sorted(_pkg.__all__):
            print(name)
    else:
        abc_logger.debug("no args given, printing help")
        parser.print_help()

if __name__ == "__main__":
    main()
   
