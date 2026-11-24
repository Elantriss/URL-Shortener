# libs/core/src/core/base62.py

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = 62

def encode_base62(number: int) -> str:
    """Converts an integer ID into a short string in Base62 format."""
    if number == 0:
        return ALPHABET[0]

    result = ""
    
    while number > 0:
        remainder = number % BASE
        
        char = ALPHABET[remainder] 
        
        result = char + result

        number = number // BASE 
        
    return result
    
def decode_base62(short_code: str) -> int:
    """Converts a Base62 string back into its original integer ID."""
    number = 0
    
    for char in short_code:
        position = ALPHABET.index(char)
        number = number * BASE + position
        
    return number