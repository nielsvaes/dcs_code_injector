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
    log_highlight_rules = "log_highlight_rules"
    log_file = "log_file"
    shift_hours = "shift_hours"
    code_font_size = "code_font_size"
    log_font_size = "log_font_size"
    version = "version"
    main_win_width = "main_win_width"
    main_win_height = "main_win_height"
    main_win_pos_x = "main_win_pos_x"
    main_win_pos_y = "main_win_pos_y"


sk = SettingConstants