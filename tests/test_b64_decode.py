from cookie_clicker_parser.parser import decode_64
from urllib.parse import unquote
from pytest import assume


def test_b64_decode(save_codes):
    for code in save_codes:
        assume(decode_64(unquote(code["save_code"])) == code["save_code_b64_decoded"])