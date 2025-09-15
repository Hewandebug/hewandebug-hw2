import pytest
from index import text_to_number, number_to_text, base64_to_number, number_to_base64


def test_dependencies_installed():
    # check if all dependencies are installed
    for dep in ["flask", "num2words", "text2digits"]:
        try:
            __import__(dep)
        except ImportError:
            pytest.fail(f"Missing dependency: {dep}. Install with 'pip install {dep}'.")

def test_text_to_number():
    #correct input
    assert text_to_number("one") == 1

    #incorrect input
    with pytest.raises(ValueError):
        text_to_number("hewan")
    with pytest.raises(ValueError):
        text_to_number("")
    with pytest.raises(ValueError):
        text_to_number("negative one")
    
    #case sensitivity and whitespace
    assert text_to_number("  ONE  ") == 1

    # tests that will fail original implementation
    assert text_to_number("one hundred") == 100

    # test zero and nil
    assert text_to_number("zero") == 0
    assert text_to_number("nil") == 0

    # different punctuation
    punctuation_tests = ["one!", "one.", "one?", "one,", "one;", "one:"]
    for test_input in punctuation_tests:
        assert text_to_number(test_input) == 1

def test_number_to_text():
    # basic numbers 
    assert number_to_text(1) == "one"
    assert number_to_text(22) == "twenty-two"

    # ordinal numbers
    assert number_to_text(1) == "first"

    # negative numbers
    assert number_to_text(-1) == "minus one"

    # non-numerical input
    with pytest.raises(ValueError):
        number_to_text("hewan")
    with pytest.raises(ValueError):
        number_to_text("")
    with pytest.raises(ValueError):
        number_to_text("")



def test_base64_to_number():
    """Test base64 to number conversion"""
    # Test basic base64 strings
    assert base64_to_number("AQ==") == 1  # base64 of 1
    
    # Test larger numbers
    assert base64_to_number("ZQ==") == 101  # base64 of 101
    
    # Test invalid base64
    with pytest.raises(ValueError):
        base64_to_number("invalid_base64!")
    
    # Test empty string
    with pytest.raises(ValueError):
        base64_to_number("")
    
    # Test None input
    with pytest.raises(ValueError):
        base64_to_number(None)

def test_number_to_base64():
    """Test number to base64 conversion"""
    # Test basic numbers
    assert number_to_base64(1) == "AQ=="

    
    # Test negative numbers
    assert number_to_base64(-1) == "//8="  # base64 of -1
    
    # Test large numbers
    assert number_to_base64(255) == "//8="  # base64 of 255 (1 byte max)
    
    # Test invalid inputs
    with pytest.raises(ValueError):
        number_to_base64("not_a_number")
    
    with pytest.raises(ValueError):
        number_to_base64(None)

def test_base64_byteorder_bug_detection():
    """
    Test to detect the byteorder bug in both base64 functions.
    This test would FAIL if byteorder='big' was used instead of byteorder='little' in either function.
    """
    # Test round-trip conversion with a number that produces different results
    # with big vs little endian (256 spans 2 bytes)
    original = 256
    base64_str = number_to_base64(original)
    converted_back = base64_to_number(base64_str)
    
    # If either function used wrong byteorder, this would fail
    assert converted_back == original, f"BUG: Round-trip failed for {original} -> {base64_str} -> {converted_back} (wrong byteorder in one or both functions)"