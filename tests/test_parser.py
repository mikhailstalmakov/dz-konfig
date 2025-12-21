import pytest
from config_tool.parser import parse_text, translate, ParseError, Number, Array, GlobalDecl


def test_number_and_basic_translate():
    txt = "42"
    xml = translate(txt)
    assert '<number>42</number>' in xml

def test_array_and_nested():
    txt = "#( 1 2 #(3 4) )"
    xml = translate(txt)
    assert xml.count('<array>') >= 2
    assert '<number>3</number>' in xml

def test_global_and_constref():
    txt = "global a = 10; #( .{a}. 20 )"
    xml = translate(txt)
    assert '<global name="a">' in xml
    assert '<number>10</number>' in xml
    assert xml.count('<number>10</number>') >= 1

def test_comments_ignored():
    txt = "% comment\n=begin\nmultiline\n=end\n42"
    xml = translate(txt)
    assert '<number>42</number>' in xml

def test_unknown_const_raises():
    txt = ".{nope}."
    with pytest.raises(ParseError):
        translate(txt)

def test_syntax_error_unterminated_array():
    txt = "#( 1 2"
    with pytest.raises(ParseError):
        translate(txt)
