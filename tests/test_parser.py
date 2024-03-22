# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import pytest

from farr.lexer import FarrRegexLexer
from farr.parser import FarrParser
from farr.parser.nodes import (
    ModuleNode,
    BlockNode,
    PassNode,
    IntegerNode,
    StringNode,
    IdentifierNode,
    RangeNode,
    ItemizedExpressionNode,
    ChainedExpressionsNode,
    CallNode,
    PostIncrementNode,
    PostDecrementNode,
    ArithmeticOperationNode,
    RelationalOperationNode,
    VariableDeclarationNode,
    MultiplyAssignmentNode,
    WhileNode,
    ForNode,
    IfNode,
    TryNode,
    CatchNode,
    MemberFunctionDefinitionNode,
    StructDefinitionNode,
)


def test_even_number_filter_syntax_tree(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Tests the even number filtering AST."""
    assert (
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                'let n = 30; for let i in [1..n] = { '
                'if % i 2 == 0 = { println(i); } }'
            )
        )
    ) == ModuleNode(
        body=[
            VariableDeclarationNode(
                identifier=IdentifierNode(row=1, column=5, value='n'),
                expression=IntegerNode(row=1, column=9, value='30'),
            ),
            ForNode(
                condition=RangeNode(
                    from_=IntegerNode(row=1, column=27, value='1'),
                    to=IdentifierNode(row=1, column=30, value='n'),
                    by=None,
                ),
                body=BlockNode(
                    body=[
                        IfNode(
                            condition=RelationalOperationNode(
                                row=1,
                                column=46,
                                operator='EqualEqual',
                                left=ArithmeticOperationNode(
                                    row=1,
                                    column=40,
                                    operator='Modulus',
                                    left=IdentifierNode(
                                        row=1, column=42, value='i'
                                    ),
                                    right=IntegerNode(
                                        row=1, column=44, value='2'
                                    ),
                                ),
                                right=IntegerNode(row=1, column=49, value='0'),
                            ),
                            body=BlockNode(
                                body=[
                                    CallNode(
                                        invoke=IdentifierNode(
                                            row=1,
                                            column=55,
                                            value='println',
                                        ),
                                        args=ItemizedExpressionNode(
                                            items=[
                                                IdentifierNode(
                                                    row=1, column=63, value='i'
                                                )
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            orelse=None,
                        )
                    ]
                ),
                orelse=None,
                initial=ItemizedExpressionNode(
                    items=[
                        VariableDeclarationNode(
                            identifier=IdentifierNode(
                                row=1, column=21, value='i'
                            ),
                            expression=None,
                        )
                    ]
                ),
            ),
        ]
    )


def test_factorial_calculator_syntax_tree(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Tests the factorial calculation program AST."""
    assert (
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                'let i = 5; let result = 1; while i >= 1 = { result *= i; '
                'i--; } println(result);'
            )
        )
    ) == ModuleNode(
        body=[
            VariableDeclarationNode(
                identifier=IdentifierNode(row=1, column=5, value='i'),
                expression=IntegerNode(row=1, column=9, value='5'),
            ),
            VariableDeclarationNode(
                identifier=IdentifierNode(row=1, column=16, value='result'),
                expression=IntegerNode(row=1, column=25, value='1'),
            ),
            WhileNode(
                condition=RelationalOperationNode(
                    row=1,
                    column=36,
                    operator='GreaterThanOrEqual',
                    left=IdentifierNode(row=1, column=34, value='i'),
                    right=IntegerNode(row=1, column=39, value='1'),
                ),
                body=BlockNode(
                    body=[
                        MultiplyAssignmentNode(
                            references=ItemizedExpressionNode(
                                items=[
                                    IdentifierNode(
                                        row=1, column=45, value='result'
                                    )
                                ]
                            ),
                            expression=IdentifierNode(
                                row=1, column=55, value='i'
                            ),
                        ),
                        PostDecrementNode(
                            row=1,
                            column=59,
                            operator=None,
                            operand=ItemizedExpressionNode(
                                items=[
                                    IdentifierNode(row=1, column=58, value='i')
                                ]
                            ),
                        ),
                    ]
                ),
                orelse=None,
            ),
            CallNode(
                invoke=IdentifierNode(row=1, column=65, value='println'),
                args=ItemizedExpressionNode(
                    items=[IdentifierNode(row=1, column=73, value='result')]
                ),
            ),
        ]
    )


def test_zero_division_error_handling_syntax_tree(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Checks how exceptions are handled."""
    assert (
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                'try = { / 0 5; } catch ZeroDivisionError = { ...; }'
            )
        )
    ) == ModuleNode(
        body=[
            TryNode(
                body=BlockNode(
                    body=[
                        ArithmeticOperationNode(
                            row=1,
                            column=9,
                            operator='Divide',
                            left=IntegerNode(row=1, column=11, value='0'),
                            right=IntegerNode(row=1, column=13, value='5'),
                        )
                    ]
                ),
                catch=CatchNode(
                    excepts=ItemizedExpressionNode(
                        items=[
                            IdentifierNode(
                                row=1, column=24, value='ZeroDivisionError'
                            )
                        ]
                    ),
                    as_=None,
                    body=BlockNode(body=[PassNode(row=1, column=46)]),
                    orelse=None,
                ),
            )
        ]
    )


def test_birthday_greetings_sender_syntax_tree(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Tests the output of the happy birthday code parser."""
    assert (
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                '\n\nstruct Person = { let full_name, let age } fn Person::'
                'happy_birthday!() = { age++; println("Happy, birthday!"); }\n'
                'let person = Person("John Doe", 99);\nperson.happy_birthday!();'
            )
        )
    ) == ModuleNode(
        body=[
            StructDefinitionNode(
                identifier=IdentifierNode(row=3, column=8, value='Person'),
                body=BlockNode(
                    body=[
                        ItemizedExpressionNode(
                            items=[
                                VariableDeclarationNode(
                                    identifier=IdentifierNode(
                                        row=3, column=23, value='full_name'
                                    ),
                                    expression=None,
                                ),
                                VariableDeclarationNode(
                                    identifier=IdentifierNode(
                                        row=3, column=38, value='age'
                                    ),
                                    expression=None,
                                ),
                            ]
                        )
                    ]
                ),
                parents=None,
            ),
            MemberFunctionDefinitionNode(
                identifier=IdentifierNode(
                    row=3, column=55, value='happy_birthday_e'
                ),
                body=BlockNode(
                    body=[
                        PostIncrementNode(
                            row=3,
                            column=80,
                            operator=None,
                            operand=ItemizedExpressionNode(
                                items=[
                                    IdentifierNode(
                                        row=3, column=77, value='age'
                                    )
                                ]
                            ),
                        ),
                        CallNode(
                            invoke=IdentifierNode(
                                row=3, column=84, value='println'
                            ),
                            args=ItemizedExpressionNode(
                                items=[
                                    StringNode(
                                        row=3,
                                        column=92,
                                        value='"Happy, ' 'birthday!"',
                                    )
                                ]
                            ),
                        ),
                    ]
                ),
                params=ItemizedExpressionNode(items=[]),
                struct=IdentifierNode(row=3, column=47, value='Person'),
            ),
            VariableDeclarationNode(
                identifier=IdentifierNode(row=4, column=5, value='person'),
                expression=CallNode(
                    invoke=IdentifierNode(row=4, column=14, value='Person'),
                    args=ItemizedExpressionNode(
                        items=[
                            StringNode(row=4, column=21, value='"John ' 'Doe"'),
                            IntegerNode(row=4, column=33, value='99'),
                        ]
                    ),
                ),
            ),
            ChainedExpressionsNode(
                expressions=ItemizedExpressionNode(
                    items=[
                        IdentifierNode(row=5, column=1, value='person'),
                        CallNode(
                            invoke=IdentifierNode(
                                row=5, column=8, value='happy_birthday_e'
                            ),
                            args=ItemizedExpressionNode(items=[]),
                        ),
                    ]
                )
            ),
        ]
    )


@pytest.mark.xfail(raises=SyntaxError)
def test_parse_syntax_error(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Checks which grammars are not allowed."""
    assert farr_parser_fixture.parse(
        farr_regex_lexer_fixture.tokenize(
            '"An expression without a semicolon at the end..."'
        )
    )
    assert farr_parser_fixture.parse(farr_regex_lexer_fixture.tokenize('/ 8;'))
