import sys
import argparse
from toolkit.calculator import calc
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc")
    calc_parser.add_argument("expression", type=str)

    conv_parser = subparsers.add_parser("convert")
    conv_parser.add_argument("value", type=str)
    conv_parser.add_argument("--from", dest="from_unit", type=str, required=True)
    conv_parser.add_argument("--to", dest="to_unit", type=str, required=True)

    args = parser.parse_args()

    try:
        if args.command == "calc":
            result = calc(args.expression)
            print(result)
        elif args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
            print(result)
        sys.exit(0)
    except ToolkitError as e:
        print("Ошибка:", e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print("Неизвестная ошибка:", e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()