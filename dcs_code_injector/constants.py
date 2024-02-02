DEFAULT_HIGHLIGHTING_RULES = {
        "^.*\\b(SCRIPTING)\\b.*$": [
            "(0, 0, 0, 0)",
            "(85, 255, 255, 255)"
        ],
        "^.*\\b(WARNING)\\b.*$": [
            "(0, 0, 0, 0)",
            "(255, 255, 0, 255)"
        ],
        "^.*\\b(ERROR|stack traceback|in function|in main chunk)\\b.*$": [
            "(255, 0, 0, 255)",
            "(255, 255, 255, 255)"
        ],
        "^.*(\\/E:).*$": [
            "(255, 0, 0, 255)",
            "(255, 255, 255, 255)"
        ],
        "^.*\\b(ERROR_ONCE)\\b.*$": [
            "(255, 139, 30, 255)",
            "(255, 255, 255, 255)"
        ],
        "^.*\\b(MOOSE INCLUDE END|MOOSE STATIC INCLUDE START)\\b.*$": [
            "(0, 0, 0, 0)",
            "(54, 194, 72, 255)"
        ]
}

class SettingConstants:
    """
    Used to easily autocomplete setting names in the code
    """
    log_highlight_rules = "log_highlight_rules"
    log_file = "log_file"
    play_sound_on_mission_scripting_error = "play_sound_on_mission_scripting_error"
    shift_hours = "shift_hours"
    code_font_size = "code_font_size"
    log_font_size = "log_font_size"
    version = "version"
    main_win_width = "main_win_width"
    main_win_height = "main_win_height"
    main_win_pos_x = "main_win_pos_x"
    main_win_pos_y = "main_win_pos_y"
    enable_code_completion = "enable_code_completion"
    MOOSE_autocomplete = "MOOSE_autocomplete"
    mist_autocomplete = "mist_autocomplete"
    MOOSE_url = "MOOSE_url"
    mist_url = "mist_url"
    default_MOOSE_url = "https://raw.githubusercontent.com/FlightControl-Master/MOOSE_INCLUDE/master/Moose_Include_Static/Moose_.lua"
    default_mist_url = "https://raw.githubusercontent.com/mrSkortch/MissionScriptingTools/master/mist.lua"
    log_font = "log_font"
    code_font = "code_font"
    default_font = "Courier New"
    theme_material_neon = "Material Neon"
    theme_fusion_dark = "Fusion Dark"
    theme = "theme"

sk = SettingConstants

lua_keywords = ['and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for', 'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat', 'return', 'then', 'true', 'until', 'while']