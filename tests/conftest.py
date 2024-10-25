import pytest
import json


@pytest.fixture
def save_codes():
    with open("tests/save_codes.json") as save_code_file:
        return json.load(save_code_file)
