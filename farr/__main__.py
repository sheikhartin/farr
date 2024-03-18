# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import argparse
import pathlib

from farr.exceptions import InterpretError
from farr.lexer import FarrRegexLexer
from farr.parser import FarrParser
from farr.interpreter.base import Environment
from farr.interpreter import FarrInterpreter


def run_file(filepath: str) -> None:
    """Executes the code from a file."""
    return FarrInterpreter().interpret(
        FarrParser().parse(
            FarrRegexLexer().tokenize(pathlib.Path(filepath).read_text())
        )
    )


def run_cmd(code: str) -> None:
    """Executes code provided as a string."""
    return FarrInterpreter().interpret(
        FarrParser().parse(FarrRegexLexer().tokenize(code))
    )


def repl() -> None:
    """Runs the codes in an interactive mode."""
    lexer = FarrRegexLexer()
    parser = FarrParser()
    interpreter = FarrInterpreter()

    while True:
        try:
            interpreter._interpret(
                parser.parse(lexer.tokenize(input('Farr> ')))
            )
        except (KeyboardInterrupt, EOFError):
            print('Exiting REPL...')
            break
        except InterpretError as e:
            if isinstance(e.error, SystemExit):
                raise e.error
            print(f'Error: {e.error}')
        except BaseException as e:
            print(f'Error: {e}')
    return None


def main() -> None:
    """Runs the language based on the arguments."""
    parser = argparse.ArgumentParser(description='Use Farr and enjoy!')
    subparsers = parser.add_subparsers(dest='command')

    run_parser = subparsers.add_parser('run', help='Run code from a file.')
    run_parser.add_argument('filepath', type=str, help='path to the file')

    cmd_parser = subparsers.add_parser(
        'cmd', help='Run a string containing code.'
    )
    cmd_parser.add_argument('code', type=str, help='the code to execute')

    shell_parser = subparsers.add_parser('shell', help='Start the Farr REPL.')

    if (args := parser.parse_args()).command == 'run':
        run_file(args.filepath)
    elif args.command == 'cmd':
        run_cmd(args.code)
    elif args.command == 'shell':
        repl()
    else:
        parser.print_help()
    return None


if __name__ == '__main__':
    main()
