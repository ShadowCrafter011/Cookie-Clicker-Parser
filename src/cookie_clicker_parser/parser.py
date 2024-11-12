from cookie_clicker_parser.section_parsers import run_detail_data, preference_names, misc_game_data_data, building_data as building_data_parser, buffs_data
from urllib.parse import unquote
import base64


def parse(save_code: str) -> object:
    plain_code: str = decode_64(unquote(save_code))
    sections = plain_code.split("|")

    game = {}
    game["version"] = sections[0]

    run_details = sections[2].split(";")
    load_section(game, run_details, "run_details", run_detail_data())

    preferences = list(sections[3])
    load_section(game, preferences, "preferences", preference_names())

    misc_game_data = sections[4].split(";")
    load_section(game, misc_game_data, "misc_game_data", misc_game_data_data())
    permanent_upgrades = []
    for x in range(5):
        try:
            permanent_upgrades.append(
                game["misc_game_data"][f"permanent_upgrade_{x}"]
            )
            del game["misc_game_data"][f"permanent_upgrade_{x}"]
        except KeyError:
            continue
    game["misc_game_data"]["permanent_upgrades"] = permanent_upgrades
    dragon_auras = []
    for x in range(2):
        try:
            dragon_auras.append(
                game["misc_game_data"][f"dragon_aura_{x}"]
            )
            del game["misc_game_data"][f"dragon_aura_{x}"]
        except KeyError:
            continue
    game["misc_game_data"]["dragon_auras"] = dragon_auras

    building_data = list(filter(None, sections[5].split(";")))
    game["buildings"] = []
    for x, building in enumerate(building_data):
        build_data = building.split(",")
        build_data = list(map(lambda b: b or None, build_data))
        game["buildings"].append({})
        load_section(game["buildings"], build_data, x, building_data_parser(), filter_none=False)

    upgrades = list(sections[6])
    game["upgrades"] = []
    for x in range(len(upgrades) // 2):
        game["upgrades"].append({
            "unlocked": bool(int(upgrades[2 * x])),
            "bought": bool(int(upgrades[2 * x + 1]))
        })

    achievements = list(sections[7])
    game["achievements"] = [
        bool(int(ach)) for ach in achievements
    ]

    buffs = list(filter(None, sections[8].split(";")))
    game["buffs"] = []
    for x, buff in enumerate(buffs):
        game["buffs"].append({})
        load_section(game["buffs"], buff.split(","), x, buffs_data())

    game["mod_data"] = sections[9]

    return game

def get_seed(save_code: str) -> str:
    return parse(save_code)["run_details"]["seed"]

def load_section(game: object, section: list, section_name: str, section_data: object, filter_none: bool = True) -> None:
    if filter_none:
        section = list(filter(None, section))
    if len(section_data) < len(section):
        raise ValueError(f"Too many entries in section {section_name}({len(section)}) ({len(section_data)} supported). Package might be out of date")
    game[section_name] = {}
    for x, value in enumerate(section):
        key = list(section_data)[x]
        try:
            game[section_name][key] = parse_value(value, *section_data[key])
        except ValueError:
            parser_names = map(lambda x: str(x), section_data[key])
            print(f"Failed to parse key {key} with value {value} to {" ".join(parser_names)} falling back to string representation")
            game[section_name][key] = value

def parse_value(value: str, *parsers):
    if value == "NaN":
        return None
    for parser in parsers:
        value = parser(value)
    return value

def decode_64(save_code: str) -> str:
    save_code: str = save_code.removesuffix("!END!")
    save_bytes: bytes = base64.b64decode(save_code)
    return save_bytes.decode("utf-8")


if __name__ == "__main__":
    parsed = parse("Mi4wNTJ8fDE3Mjk1OTU3Mzk4MDQ7MTcyNjc2MzA0NjI0NTsxNzMxNDI2MTgzMjc5O1NoYWRvdzt2bHpicDs0LDYsMSwxLDYsNCwwfDExMTExMTAxMTAwMTExMTAwMTExMDEwMTAwMXwzLjg1OTIzMTE4NTQ2MTkxMzRlKzUxOzMuODg2Mzg5MTYyODg5MzczZSs1MTsyNjsxMDQzOzguMDUxMTI2OTIxNzIxMzQ5ZSs0NDsxNjUyOzA7MDs2LjkyMjgwNzQ1ODE3OTE5ZSs1NjswOzA7MDswOzA7NTM1OzIwOzA7MDswOzA7MDswOzswOzA7ODg0NjI4MTQxNjUzNDUxOzcwMDYxMzE4MDcyMDI2OzgxNDU2NjgyMzU4MTQyNTswOzA7NDQyOzQ2Mjs0OTQ7NjEzOzc2NjswOzA7MDswOzA7MDswOzM7NTc7MTczMTM3NzE1OTMwNDswOzA7OzEwMDswOzA7OC40ODM5MzQ2MDkwOTkzNTJlKzQ1OzA7NjY5OzY2OTt8NzM0LDczNCwyLjQ3MTMyMzU4MDk2NjE0MDNlKzUwLDMsLDAsNzM0OzUsNSw1LjY1MDcwMjQ2NTA2MzM1OGUrMzIsMCwsMSw1OzEwMCwxMDAsNC4yMjIzNDI5MDA2ODYyNzk0ZSsyOSw5LDE3MzE0MjY0MTA5NzY6MDoxNzI5NTk1NzM5ODA4OjA6MDoxODowOjA6MTcyOTU5NTczOTgwODogMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMCAwOjA6MDowOjA6MDowOjA6MDowOjA6MDowOjA6MDowOjE0OjYxOjA6MDowOjA6MDowOjA6MDowOjA6MDowOjA6MDoxNDowOjA6MDowOjA6MTQ6Mzc6MTQ6NzQ6MDowOjA6MDoxNDo2NDowOjA6MTQ6OTg6MDowOjE0OjYxOjE0OjMyOjE0OjE1OjA6MDowOjA6MDowOjA6MDowOjA6MDowOiwwLDEwMDswLDAsMCwwLCwxLDA7MCwwLDAsMCwsMSwwOzAsMCwwLDEsMDowOjE6MDoxOiAyMTU3OjE6Njk6OTg6MDowOjA6MCE5MjM2OjA6MTA2Ojc6MDoxOjA6MCExMDI5OjU6LTI2OjYyNzowOjE6MDowITc3OTo1OjQ6MTE4OjA6MTowOjAhNjMwNTo1Oi0yMDozMzM6MDoxOjA6MCE5MTA1OjI6MTI5OjI3OjA6MDowOjAhNDg1NDoxOjE1NTo1NDY6MDoxOjA6MCExMTE5OjU6LTMxOjU5OTowOjE6MDowITE0MzMwOjE6NTM6NTgzOjA6MTowOjAhMTE4ODA6MTotMToxMTY6MDoxOjA6MCE5MjE5OjU6LTIzOjIyMzowOjE6MDowITk2NDc6NTo0NTo0Njc6MDoxOjA6MCExMTI0MjozOjgzOjUxMTowOjE6MDowITExMjE4OjU6LTM3OjU5NzowOjA6MDowITE0OTk1OjM6NzE6MjU6MDoxOjA6MCExMzUzOTowOjE3OjE2MTowOjE6MDowITEwNzU2OjU6LTcwOjE0MjowOjE6MDowITEwMzYxOjU6LTc2OjI2NjowOjE6MDowISAwLDEsMDswLDAsMCwxLC0xLy0xLy0xIDMgMTcyOTU5NTczOTgxMCAwLDAsMDsxMDAsMTAwLDguNTQwNjc4MzAyMzMyNjc2ZSszMiwxLDUuMjQ4OTg2OTEwNTU0NzQ3NSAwIDE2OCAwLDAsMTAwOzAsMCwwLDAsLDEsMDswLDAsMCwwLCwxLDA7MCwwLDAsMCwsMSwwOzAsMCwwLDAsLDEsMDswLDAsMCwwLCwxLDA7MCwwLDAsMCwsMSwwOzAsMCwwLDAsLDEsMDs0NTUsNDU1LDEuOTM0MTk0NDgzODMxOTQxNGUrNDcsMCwsMSw0NTU7MCwwLDAsMCwsMSwwOzAsMCwwLDAsLDEsMDswLDAsMCwwLCwxLDA7MCwwLDAsMCwsMSwwO3wxMTExMTExMTExMTExMTEwMTAwMDEwMTAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDExMTExMTExMTExMTExMTExMTExMTExMTExMDAxMDAwMDAwMDAwMDAwMDExMTExMTExMTExMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxMTExMTExMTAwMTExMTExMDAwMDAwMTEwMDExMTExMTAwMTExMTExMTExMTExMTEwMDAwMDAwMDAwMTExMTExMTExMTExMDAxMDAwMDAwMDAwMDAwMDAwMTExMTExMTExMTAwMTExMTExMTExMTExMTExMTExMDAwMDAwMDAwMDAwMDAxMTAwMDAwMDAwMDAwMDAwMDAxMTExMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDExMTAxMDEwMTAwMDExMTExMTExMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDExMTExMTExMTExMTAwMTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTExMTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEwMTAxMDEwMTAwMDAwMDAxMDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTExMTExMTExMTExMTExMTExMTEwMDEwMDAxMDAwMDAwMDAwMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMTExMTExMTExMTEwMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxMTExMTExMTExMDAwMDAwMTExMTExMTExMTExMTExMTExMTExMTExMDAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTExMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDExMDAxMTExMTExMTExMTExMTExMTAxMTExMTExMTExMTEwMDEwMTAxMTExMTExMTExMTExMTExMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTExMTExMDAxMTExMTExMTExMTExMTExMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDExMTExMTExMTExMTExMTExMTExMTExMTExMDAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDExMTExMDExMTExMTExMTExMDEwMTAxMTExMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxMDAwMDAwMDExMDAwMDExMTEwMDAwMDAwMDEwMDAwMDAwMDAwMDAwMDAxMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDExMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxMTExMTExMTAwMDAwMDAwMTExMTExMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTExMDExMDAxMTExMTExMTExMTExMTExMTExMTExMDAwMDAwMDAwMDAwMDAwMDExMTExMTExMTExMTExMTExMTAwMDAwMDAwMDAxMTExMDAxMTExMTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTExMTAwMDAwMDAwMTEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEwMTEwMDAwMDAwMDAwMDAxMTEwfDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMTExMTExMTExMDExMTEwMTExMTExMTEwMDAwMDAxMTExMDEwMDAxMTAwMDAxMTExMTExMTExMTExMTEwMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMTExMTExMTAwMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMTEwMTEwMTEwMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMDAwMDAwMDAwMDAwMDExMDAxMTExMTExMTExMTAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMTExMTExMTExMTAwMDAwMTExMTExMTExMTEwMDAwMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEwMTExMTExMTExMTExMTExMTExMTAxMTExMTExMTAxMDAwMDAwMDEwMTExMTAwMTExMTExMTExMTExMTExMTEwMDExMTExMTExMTExMTEwMDAwMTExMTExMTExMTEwMDExMTAxMTExMDExMDAwMDAxMTExMTExMTExMTEwMDExMTAxMTExMTExMTExMDAwMDAwMDAxMDAwMDAwMTEwMDAwMDExMDAwMDExMDAxMDExMTExMTExMTAwMDAwMTExMDExMTExMTAxMDAwMDAwMDAwMDAwMDExMDB8fE1FVEE6KmNvb2xlciBzYW1wbGUgbW9kLCpsYW5nIHNhbXBsZSBtb2QsKnNhbXBsZSBtb2Q7%21END%21")
    with open("tmp.json", "w") as f:
        import json
        json.dump(parsed, f)
