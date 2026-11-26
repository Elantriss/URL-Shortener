import pytest
from core.base62 import encode_base62, decode_base62

def test_encode_of_zero_returns_alphabet_first_char():
    number = 0
    expected = '0'

    result = encode_base62(number)

    assert result == expected

def test_encode_of_known_number():
    number = 11157
    expected = '2TX'

    result = encode_base62(number)

    assert result == expected

def test_decode_of_known_short_code():
    short_code = '2TX'
    expected = 11157

    result = decode_base62(short_code)

    assert result == expected


def test_round_trip_encode_decode():
    numbers = [0, 1, 61, 62, 1000, 99999, 12345678]
    
    for n in numbers:
        assert decode_base62(encode_base62(n)) == n
        

def test_decode_with_invalid_character_raises_error():

    invalid_code = "!"
    
    with pytest.raises(ValueError):
        decode_base62(invalid_code)

