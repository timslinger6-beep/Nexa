import sys
from pathlib import Path

from lexer import Lexer
from parser import Parser
from interpreter import run
from runtime import GameRuntime


VERSION = "0.1.0"
PROGRAM_NAME = "Nexa"


def print_help():
    print(f"{PROGRAM_NAME} {VERSION}")
    print()
    print("Verwendung:")
    print("  nexa <datei.my>")
    print("  nexa --version")
    print("  nexa --help")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h"):
        print_help()
        return 0

    if args[0] in ("--version", "-v"):
        print(f"{PROGRAM_NAME} {VERSION}")
        return 0

    if len(args) != 1:
        print("Fehler: Erwartet wird genau eine .my-Datei.", file=sys.stderr)
        print_help()
        return 1

    path = Path(args[0])

    if not path.is_file():
        print(f"Fehler: Datei nicht gefunden: {path}", file=sys.stderr)
        return 1

    try:
        source = path.read_text(encoding="utf-8")

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        runtime = GameRuntime()
        run(program, runtime)

        return 0

    except (SyntaxError, RuntimeError) as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1

    except OSError as error:
        print(f"Fehler beim Lesen der Datei: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())