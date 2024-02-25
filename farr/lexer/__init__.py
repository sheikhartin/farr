# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

from farr.lexer.base import GroupedTokens, Token, RegexLexer


class FarrRegexLexer(RegexLexer):
    tokens = [
        GroupedTokens(
            r'/{2}.*|\/\*[\s\S]*?\*\/',
            [
                Token('SingleLineComment', r'/{2}.*', ignore=True),
                Token('MultiLineComment', r'\/\*[\s\S]*?\*\/', ignore=True),
            ],
        ),
        GroupedTokens(
            r'[\-\+]?(?:\d+\.(?!\.)\d*|\d*\.(?!\.)\d+|\d+)|'
            r'r?"(?:[^"\\]|\\.)*"',
            [
                Token('Integer', r'[\-\+]?\d+'),
                Token('Float', r'[\-\+]?(?:\d+\.(?!\.)\d*|\d*\.(?!\.)\d+)'),
                Token('String', r'r?"(?:[^"\\]|\\.)*"'),
            ],
        ),
        GroupedTokens(
            r'[&\|\=\:\+\-]{2}|[\<\>\!\+\-\*/%\^]\=|\.{2,3}|[\s\W]',
            [
                Token('LineBreaker', r'[\n\r]', ignore=True),
                Token('Indent', r'[\040\t]', ignore=True),
                Token('LeftParenthesis', r'\('),
                Token('RightParenthesis', r'\)'),
                Token('LeftBrace', r'\{'),
                Token('RightBrace', r'\}'),
                Token('LeftBracket', r'\['),
                Token('RightBracket', r'\]'),
                Token('Comma', r','),
                Token('Dot', r'\.'),
                Token('Colon', r'\:'),
                Token('DoubleColon', r'\:{2}'),
                Token('Increment', r'\+{2}'),
                Token('Decrement', r'\-{2}'),
                Token('Semicolon', r';'),
                Token('Add', r'\+'),
                Token('Subtract', r'\-'),
                Token('Multiply', r'\*'),
                Token('Divide', r'/'),
                Token('Modulus', r'%'),
                Token('Power', r'\^'),
                Token('Not', r'\!'),
                Token('And', r'&{2}'),
                Token('Or', r'\|{2}'),
                Token('Equal', r'\='),
                Token('EqualEqual', r'\={2}'),
                Token('NotEqual', r'\!\='),
                Token('LessThan', r'\<'),
                Token('GreaterThan', r'\>'),
                Token('LessThanOrEqual', r'\<\='),
                Token('GreaterThanOrEqual', r'\>\='),
                Token('AddEqual', r'\+\='),
                Token('SubtractEqual', r'\-\='),
                Token('MultiplyEqual', r'\*\='),
                Token('DivideEqual', r'/\='),
                Token('ModulusEqual', r'%\='),
                Token('PowerEqual', r'\^\='),
                Token('Between', r'\.{2}'),
                Token('Pass', r'\.{3}'),
            ],
        ),
        GroupedTokens(
            r'_?[A-Za-z][A-Za-z_]*\d{,3}(?:\?\!|\!\?|\!|\?)?|\w*',
            [
                Token('Null', r'null'),
                Token('Use', r'use'),
                Token('Variable', r'let'),
                Token('If', r'if'),
                Token('Else', r'else'),
                Token('While', r'while'),
                Token('Break', r'break!'),
                Token('Continue', r'continue!'),
                Token('For', r'for'),
                Token('In', r'in'),
                Token('Try', r'try'),
                Token('Catch', r'catch'),
                Token('Function', r'fn'),
                Token('Return', r'return!'),
                Token('Struct', r'struct'),
                Token('Identifier', r'.*'),
            ],
        ),
    ]


if __name__ == '__main__':
    import sys
    from pprint import pprint

    pprint(FarrRegexLexer().tokenize(sys.stdin.read()))
