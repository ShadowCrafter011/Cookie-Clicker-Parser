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
        game[section_name][key] = parse_value(value, *section_data[key])

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
