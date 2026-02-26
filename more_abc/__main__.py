from argparse import ArgumentParser
import more_abc as _pkg

from . import __all__, version
from ._read_last_version import _check_mod_version

# Leave it for now.
# Add in 2.1.1
# INTRODUCTION = """more_abc — an extension of the abc module.

# Provides abstract base class utilities beyond the standard library:
#   ABCMixin          abstract initialize / validate / to_dict interface
#   abstract_class    decorator that converts any class into an ABC
#   abstractdataclass @dataclass with ABCMeta built in
#   ABCEnum / ABCIntEnum / ABCFlag / ABCIntFlag
#                     Enum variants with abstract-method support
#   ABCException / ABCWarning
#                     abstract bases for custom exceptions and warnings
#   AbstractLogHandler / AbstractLogFormatter / AbstractLogFilter
#                     abstract bases for logging components
#   AbstractRawIO / AbstractBufferedIO / AbstractTextIO
#                     abstract bases for io stream types
#   Sortable / Filterable / Transformable
#                     ABC families for custom collection types
# """

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
    parser.add_argument(
        "-d", "--doc",
        metavar="SYMBOL",
        help="print the docstring of a public symbol",
    )
    args = parser.parse_args()
    _check_mod_version()

    if args.doc:
        obj = getattr(_pkg, args.doc, None)
        if obj is None:
            print(f"Symbol '{args.doc}' not found in more_abc.")
        elif obj.__doc__:
            print(obj.__doc__)
        else:
            print(f"'{args.doc}' has no docstring.")
    elif args.list:
        for name in sorted(__all__):
            print(name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
