# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import textwrap

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
    CallNode,
    GroupedExpressionNode,
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
                textwrap.dedent(
                    """
                    let n = 30;
                    for let i in [1..n] = {
                      if ((% i 2) == 0) = {
                        println(i);
                      }
                    }
                    """
                )
            )
        )
        == ModuleNode(
            body=[
                VariableDeclarationNode(
                    identifier=IdentifierNode(row=2, column=5, value='n'),
                    expression=IntegerNode(row=2, column=9, value='30'),
                ),
                ForNode(
                    condition=RangeNode(
                        from_=IntegerNode(row=3, column=15, value='1'),
                        to=IdentifierNode(row=3, column=18, value='n'),
                        by=None,
                    ),
                    body=BlockNode(
                        body=[
                            IfNode(
                                condition=RelationalOperationNode(
                                    row=4,
                                    column=15,
                                    operator='EqualEqual',
                                    left=GroupedExpressionNode(
                                        expression=ArithmeticOperationNode(
                                            row=4,
                                            column=8,
                                            operator='Modulus',
                                            left=IdentifierNode(
                                                row=4, column=10, value='i'
                                            ),
                                            right=IntegerNode(
                                                row=4, column=12, value='2'
                                            ),
                                        )
                                    ),
                                    right=IntegerNode(
                                        row=4, column=18, value='0'
                                    ),
                                ),
                                body=BlockNode(
                                    body=[
                                        CallNode(
                                            invoke=IdentifierNode(
                                                row=5, column=5, value='println'
                                            ),
                                            args=ItemizedExpressionNode(
                                                items=[
                                                    IdentifierNode(
                                                        row=5,
                                                        column=13,
                                                        value='i',
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
                                    row=3, column=9, value='i'
                                ),
                                expression=None,
                            )
                        ]
                    ),
                ),
            ]
        )
    )


def test_factorial_calculator_syntax_tree(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Tests the factorial calculation program AST."""
    assert (
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                textwrap.dedent(
                    """
                    let i = 5;
                    let result = 1;
                    while i >= 1 = {
                      result *= i;
                      i--;
                    }
                    println(result);
                    """
                )
            )
        )
        == ModuleNode(
            body=[
                VariableDeclarationNode(
                    identifier=IdentifierNode(row=2, column=5, value='i'),
                    expression=IntegerNode(row=2, column=9, value='5'),
                ),
                VariableDeclarationNode(
                    identifier=IdentifierNode(row=3, column=5, value='result'),
                    expression=IntegerNode(row=3, column=14, value='1'),
                ),
                WhileNode(
                    condition=RelationalOperationNode(
                        row=4,
                        column=9,
                        operator='GreaterThanOrEqual',
                        left=IdentifierNode(row=4, column=7, value='i'),
                        right=IntegerNode(row=4, column=12, value='1'),
                    ),
                    body=BlockNode(
                        body=[
                            MultiplyAssignmentNode(
                                references=ItemizedExpressionNode(
                                    items=[
                                        IdentifierNode(
                                            row=5, column=3, value='result'
                                        )
                                    ]
                                ),
                                expression=IdentifierNode(
                                    row=5, column=13, value='i'
                                ),
                            ),
                            PostDecrementNode(
                                row=6,
                                column=4,
                                operator=None,
                                operand=ItemizedExpressionNode(
                                    items=[
                                        IdentifierNode(
                                            row=6, column=3, value='i'
                                        )
                                    ]
                                ),
                            ),
                        ]
                    ),
                    orelse=None,
                ),
                CallNode(
                    invoke=IdentifierNode(row=8, column=1, value='println'),
                    args=ItemizedExpressionNode(
                        items=[IdentifierNode(row=8, column=9, value='result')]
                    ),
                ),
            ]
        )
    )


def test_zero_division_error_handling_syntax_tree(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Checks how exceptions are handled."""
    assert (
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                textwrap.dedent(
                    """
                    try = {
                      / 10 0;
                    } catch ArithmeticError = {
                      ...;
                    }
                    """
                )
            )
        )
        == ModuleNode(
            body=[
                TryNode(
                    body=BlockNode(
                        body=[
                            ArithmeticOperationNode(
                                row=3,
                                column=3,
                                operator='Divide',
                                left=IntegerNode(row=3, column=5, value='10'),
                                right=IntegerNode(row=3, column=8, value='0'),
                            )
                        ]
                    ),
                    catch=CatchNode(
                        excepts=ItemizedExpressionNode(
                            items=[
                                IdentifierNode(
                                    row=4, column=9, value='ArithmeticError'
                                )
                            ]
                        ),
                        as_=None,
                        body=BlockNode(body=[PassNode(row=5, column=3)]),
                        orelse=None,
                    ),
                )
            ]
        )
    )


def test_birthday_greetings_sender_syntax_tree(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
) -> None:
    """Tests the output of the happy birthday code parser."""
    assert (
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                textwrap.dedent(
                    """
                    struct Person = {
                      let full_name,
                      let age
                    }
                    fn Person::happy_birthday!() = {
                      age++;
                      println("Happy, birthday!");
                    }
                    """
                )
            )
        )
        == ModuleNode(
            body=[
                StructDefinitionNode(
                    identifier=IdentifierNode(row=2, column=8, value='Person'),
                    body=BlockNode(
                        body=[
                            ItemizedExpressionNode(
                                items=[
                                    VariableDeclarationNode(
                                        identifier=IdentifierNode(
                                            row=3, column=7, value='full_name'
                                        ),
                                        expression=None,
                                    ),
                                    VariableDeclarationNode(
                                        identifier=IdentifierNode(
                                            row=4, column=7, value='age'
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
                        row=6, column=12, value='happy_birthday_e'
                    ),
                    body=BlockNode(
                        body=[
                            PostIncrementNode(
                                row=7,
                                column=6,
                                operator=None,
                                operand=ItemizedExpressionNode(
                                    items=[
                                        IdentifierNode(
                                            row=7, column=3, value='age'
                                        )
                                    ]
                                ),
                            ),
                            CallNode(
                                invoke=IdentifierNode(
                                    row=8, column=3, value='println'
                                ),
                                args=ItemizedExpressionNode(
                                    items=[
                                        StringNode(
                                            row=8,
                                            column=11,
                                            value='"Happy, birthday!"',
                                        )
                                    ]
                                ),
                            ),
                        ]
                    ),
                    params=ItemizedExpressionNode(items=[]),
                    struct=IdentifierNode(row=6, column=4, value='Person'),
                ),
            ]
        )
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
