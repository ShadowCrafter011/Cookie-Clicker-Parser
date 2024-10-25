from urllib.parse import unquote
from pytest import assume


def test_unquote(save_codes):
    for code in save_codes:
        assume(unquote(code["save_code"]) == code["save_code_unescaped"])
