from cookie_clicker_parser import parse, get_seed
from pytest import assume


def test_code(save_codes):
    for code in save_codes:
        assume(parse(code["save_code"]) == code["parsed"])

def test_cookies(save_codes):
    for code in save_codes:
        parsed = parse(code["save_code"])
        assume(code["cookies"] == parsed["misc_game_data"]["cookies"])
        
def test_seed(save_codes):
    for code in save_codes:
        assume(get_seed(code["save_code"]) == code["seed"])
