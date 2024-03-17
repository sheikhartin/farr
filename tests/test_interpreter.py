# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import pytest

from farr.lexer import FarrRegexLexer
from farr.parser import FarrParser
from farr.interpreter import FarrInterpreter


def test_binary_operations_interpretation(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
    farr_interpreter_fixture: FarrInterpreter,
    capsys: pytest.CaptureFixture,
) -> None:
    """Tests three subsets of binary operations."""
    farr_interpreter_fixture.interpret(
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                'println(+ 13 8, - 2 4, * 6 3, / 9 10, % 12 1, ^ 6 4);\n\n'
                'println("73." == 73., "Hi!" != "Hello!", 7 < 15, 11 > 5,'
                '9 <= 6, 13 >= 13);\n\nprintln("Farr" || 67, 11 && 1);'
            )
        )
    )
    captured = capsys.readouterr()
    assert captured.out == (
        '21 -2 18 0.9 0 1296\nfalse true true true false true\nFarr 1\n'
    )


def test_definitions_and_manipulations_interpretation(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
    farr_interpreter_fixture: FarrInterpreter,
    capsys: pytest.CaptureFixture,
) -> None:
    """Checks the status of variables after changes."""
    farr_interpreter_fixture.interpret(
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                'let var; println(var); var = 42; println(var); var += 3;'
                'println(var); var -= 5; println(var); var *= .5; println(var);'
                'var /= 5; println(var); var %= 10; println(var); var ^= 0;'
                'println(var); var++; println(var); var--; println(var);\n\n'
                'fn add_one(let x) = { return! + x 1; } println(add_one(x=9));'
                'fn add_one(let x = 5) = { println(+ x 1); } add_one();\n'
                'struct Person = { let fullname, let birthyear } let person = '
                'Person("John Doe", 1997); println(person, person.fullname, '
                'person.birthyear); person.fullname = "Artin Mohammadi"; '
                'person.birthyear += 5; println(person, person.fullname, '
                'person.birthyear);\nfn Person::calculate_age(let curryear) = {'
                'return! - curryear birthyear; } let person_age = person.'
                'calculate_age(2024); print("I think u r", person_age);'
            )
        )
    )
    captured = capsys.readouterr()
    assert captured.out == (
        'null\n42\n45\n40\n20.0\n4.0\n4.0\n1.0\n2.0\n1.0\n10\nnull\n6\n'
        'StructInstanceObject() John Doe 1997\nStructInstanceObject() Artin '
        'Mohammadi 2002\nI think u r 22'
    )


def test_data_types_and_data_structures_stuff_interpretation(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
    farr_interpreter_fixture: FarrInterpreter,
    capsys: pytest.CaptureFixture,
) -> None:
    """Tests five different types of data."""
    farr_interpreter_fixture.interpret(
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                'let a = 1; let b = 1.; let c = "1."; println(typeof?(a), '
                'typeof?(b), typeof?(c), similartypes?(a, b));\n\nlet d = {'
                '"weirdness", "impeded", 56, "waterfall", "geed", 65, 23, "A"};'
                'println(d, "::", typeof?(d), d.[1], d.[2..4], similartypes?('
                'd.[1..3], {}), d.length, d.first, d.last, d.isempty?(), '
                'typeof?(d.shuffle()) == "ListObject"); d.clear!(); println('
                'typeof?(d), d.isempty?()); d.iappend!(1); d.iprepend!(0); '
                'println(d, d.join("-"), d.nearest?(1)); d.pop!(1); '
                'd.popitem!(1); println(d.isempty?()); \nlet e = {:"One" 1, '
                ':"Two" 2}; println(e, e.first, e.last, e.length, '
                'e.isempty?(), e.get("Three", 3)); e.popitem!("Two"); '
                'e.pop!(1); println(e.isempty?()); let f = "Hello"; println('
                'f.concat(", world!")); println(f.concat(", guys!"), '
                'f.split("l"));'
            )
        )
    )
    captured = capsys.readouterr()
    assert captured.out == (
        'IntegerObject FloatObject StringObject false\nweirdness; impeded; 56; '
        'waterfall; geed; 65; 23; A :: ListObject weirdness impeded; 56; '
        'waterfall true 8 weirdness A false true\nListObject true\n0; 1 0-1 2\n'
        'true\nOne->1; Two->2 One->1 Two->2 2 false 3\ntrue\nHello, world!\n'
        'Hello, guys! He; o\n'
    )


def test_import_system_interpretation(
    farr_regex_lexer_fixture: FarrRegexLexer,
    farr_parser_fixture: FarrParser,
    farr_interpreter_fixture: FarrInterpreter,
    capsys: pytest.CaptureFixture,
) -> None:
    """Checks the health and accessibility of external modules."""
    farr_interpreter_fixture.interpret(
        farr_parser_fixture.parse(
            farr_regex_lexer_fixture.tokenize(
                'use math/random; println(similartypes?(random.random(), .59), '
                'similartypes?(random.uniform(10, 20), 10.20), typeof?(random.'
                'uniform(10, 20, size=2)) != "ListObject");'
            )
        )
    )
    captured = capsys.readouterr()
    assert captured.out == 'true true false\n'
