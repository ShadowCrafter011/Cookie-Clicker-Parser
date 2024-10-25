def you_customizer_parser(you_data: str) -> list:
    return [int(x) for x in you_data.split(",")]

def vault_parser(vault_data: str) -> list:
    if vault_data == "":
        return []
    return [int(d) for d in vault_data.split(",")]

def preference_names() -> object:
    preference_names = [
        "particles",
        "numbers",
        "autosave",
        "autoupdate",
        "milk",
        "fancy",
        "warn",
        "cursors",
        "focus",
        "format",
        "notifs",
        "wobbly",
        "monospace",
        "filters",
        "cookiesound",
        "crates",
        "showBackupWarning",
        "extraButtons",
        "askLumps",
        "customGrandmas",
        "timeout",
        "cloudSave",
        "bgMusic",
        "notScary",
        "fullscreen",
        "screenreader",
        "discordPresence"
    ]
    return {name: (int, bool) for name in preference_names}

def run_detail_data() -> object:
    return {
        "start_date": (int,),
        "legacy_start_date": (int,),
        "last_opened_game_date": (int,),
        "bakery_name": (),
        "seed": (),
        "you_customizer": (you_customizer_parser,)
    }

def misc_game_data_data() -> object:
    return {
        "cookies": (float,),
        "total_cookies_earned": (float,),
        "cookie_clicks": (float,),
        "golden_cookie_clicks": (float,),
        "cookies_made_by_clicking": (float,),
        "golden_cookies_missed": (float,),
        "background_type": (int,),
        "milk_type": (int,),
        "cookies_from_past_runs": (float,),
        "elder_wrath": (float,),
        "pledges": (int,),
        "pledge_time_left": (int,),
        "currently_researching": (int,),
        "research_time_left": (int,),
        "ascensions": (int,),
        "golden_cookie_clicks_this_run": (int,),
        "cookies_sucked_by_wrinklers": (float,),
        "wrinklers_popped": (int,),
        "santa_level": (int,),
        "reindeer_clicked": (int,),
        "season_time_left": (int,),
        "season_switcher_uses": (int,),
        "current_season": (),
        "amount_cookies_in_wrinklers": (float,),
        "number_of_wrinklers": (int,),
        "prestige_level": (float,),
        "heavenly_chips": (float,),
        "heavenly_chips_spent": (float,),
        "heavenly_cookies": (float,),
        "ascension_mode": (int,),
        "permanent_upgrade_0": (int,),
        "permanent_upgrade_1": (int,),
        "permanent_upgrade_2": (int,),
        "permanent_upgrade_3": (int,),
        "permanent_upgrade_4": (int,),
        "dragon_level": (int,),
        "dragon_aura_0": (int,),
        "dragon_aura_1": (int,),
        "chime_type": (int,),
        "volume": (int,),
        "number_of_shiny_wrinklers": (float,),
        "amount_of_cookies_contained_in_shiny_wrinklers": (float,),
        "current_amount_of_sugar_lumps": (float,),
        "total_amount_of_sugar_lumps": (float,),
        "time_when_current_lump_started": (float,),
        "time_when_last_refilled_minigame_with_lump": (float,),
        "sugar_lump_type": (int,),
        "vault": (vault_parser,),
        "heralds": (int,),
        "golden_cookie_fortune": (int,),
        "cps_fortune": (float,),
        "highest_raw_cps": (float,),
        "music_volume": (int,),
        "cookies_sent": (int,),
        "cookies_received": (int,)
    }

def building_data() -> object:
    return {
        "amount_owned": (int,),
        "amount_bought": (int,),
        "total_cookies": (float,),
        "level": (int,),
        "minigame_save": (),
        "muted": (int, bool),
        "highest_amount_owned": (int,)
    }

def buffs_data() -> object:
    return {
        "id": (int,),
        "max_time": (int,),
        "time": (int,),
        "arg_0": (float,),
        "arg_1": (float,),
        "arg_2": (float,) 
    }
