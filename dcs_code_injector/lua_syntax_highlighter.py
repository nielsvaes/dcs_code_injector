from PySide6.QtCore import *
from PySide6.QtGui import *


def make_format(background_color=Qt.transparent, foreground_color=Qt.white, bold=False, italic=False):
    format = QTextCharFormat()
    format.setBackground(background_color)
    format.setForeground(foreground_color)
    format.setFontItalic(italic)
    if bold:
        format.setFontWeight(QFont.Bold)
    return format

STYLES = {
    'keyword': make_format(foreground_color=QColor(204, 120, 50)),
    'operator': make_format(foreground_color=QColor(200, 200, 200)),
    'special_brace': make_format(foreground_color=QColor(150, 255, 150), bold=True),
    'normal_brace': make_format(foreground_color=Qt.cyan, bold=True),
    'global': make_format(foreground_color=QColor(204, 120, 200), bold=True),
    'global_moose': make_format(foreground_color=Qt.magenta, bold=True),
    'string': make_format(foreground_color=QColor(165, 240, 97)),
    'string2': make_format(foreground_color=QColor(165, 240, 97)),
    'comment': make_format(foreground_color=QColor(125, 154, 57), italic=True),
    'self': make_format(foreground_color=QColor(148, 85, 141), italic=True),
    'numbers': make_format(foreground_color=QColor(104, 151, 187)),
    'colon_function_call': make_format(foreground_color=QColor(0, 151, 255)),
    'period_function_call': make_format(foreground_color=QColor(148, 104, 253)),
}

class SimpleLuaHighlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        super().__init__(doc)
        keywords = [
            "and", "break", "do", "else", "elseif", "end", "false", "for", "function", "if", "in",
            "not", "or", "repeat", "return", "then", "true", "until", "while"
        ]

        keywords_2 = ["local", "nil", ]

        operators = [
            '=',
            # Comparison
            '==', '!=', '<', '<=', '>', '>=',
            # Arithmetic
            '\+', '-', '\*', '/', '//', '\%', '\*\*',
            # In-place
            '\+=', '-=', '\*=', '/=', '\%=',
            # Bitwise
            '\^', '\|', '\&', '\~', '>>', '<<',
        ]
        special_braces = [
            '\{', '\}', '\[', '\]',
        ]

        normal_braces = [
            '\(', '\)'
        ]

        quotes = [
            '"', "'"
        ]

        glob = [
            "CCMISSION"
        ]

        glob_moose = [
            "ACT_ACCOUNT",
            "ACT_ASSIGN",
            "ACT_ASSIST",
            "ACT_ROUTE",
            "AI_A2A_CAP",
            "AI_A2A_DISPATCHER",
            "AI_A2A_GCI",
            "AI_A2A_PATROL",
            "AI_A2G_BAI",
            "AI_A2G_CAS",
            "AI_A2G_DISPATCHER",
            "AI_A2G_SEAD",
            "AI_AIR",
            "AI_AIR_DISPATCHER",
            "AI_AIR_ENGAGE",
            "AI_AIR_PATROL",
            "AI_AIR_SQUADRON",
            "AI_BAI_ZONE",
            "AI_BALANCER",
            "AI_CAP_ZONE",
            "AI_CARGO",
            "AI_CARGO_AIRPLANE",
            "AI_CARGO_APC",
            "AI_CARGO_DISPATCHER",
            "AI_CARGO_DISPATCHER_AIRPLANE",
            "AI_CARGO_DISPATCHER_APC",
            "AI_CARGO_DISPATCHER_HELICOPTER",
            "AI_CARGO_DISPATCHER_SHIP",
            "AI_CARGO_HELICOPTER",
            "AI_CARGO_SHIP",
            "AI_CAS_ZONE",
            "AI_ESCORT",
            "AI_ESCORT_DISPATCHER",
            "AI_ESCORT_DISPATCHER_REQUEST",
            "AI_ESCORT_REQUEST",
            "AI_FORMATION",
            "AI_PATROL_ZONE",
            "CARGO",
            "CARGO_CRATE",
            "CARGO_GROUP",
            "CARGO_SLINGLOAD",
            "CARGO_UNIT",
            "ASTAR",
            "BASE",
            "BEACON",
            "CCMISIONDB",
            "CONDITION",
            "CONVERSATION",
            "DATABASE",
            "EVENT",
            "FSM",
            "GAMELOOPFUNCTION",
            "GOAL",
            "IMPACT_AREA",
            "IMPACT_AREA_MANAGER",
            "MARKEROPS",
            "MENU_BASE",
            "MESSAGE",
            "PATROL_AREA",
            "COORDINATE",
            "REPORT",
            "RULE",
            "SCHEDULEDISPATCHER",
            "SCHEDULER",
            "SET_BASE",
            "SETTINGS",
            "SPAWN",
            "SPAWNSTATIC",
            "SPOT",
            "TEXTANDSOUND",
            "TIMER",
            "USERFLAG",
            "VELOCITY",
            "WEAPON_MANAGER",
            "ZONE_BASE",
            "ZONE_DETECTION",
            "CIRCLE",
            "DRAW_BASE",
            "LINE",
            "OVAL",
            "POLYGON",
            "ARTY",
            "ATC_GROUND",
            "CLEANUP_AIRBASE",
            "DESIGNATE",
            "DETECTION_BASE",
            "DETECTION_ZONES",
            "ESCORT",
            "FOX",
            "MANTIS",
            "MISSILETRAINER",
            "MOVEMENT",
            "PSEUDOATC",
            "RANGE",
            "RANGE_CIRCLE",
            "RATMANAGER",
            "SCORING",
            "SEAD",
            "SHORAD",
            "SUPPRESSION",
            "WAREHOUSE",
            "ZONE_CAPTURE_COALITION",
            "ZONE_GOAL",
            "ZONE_GOAL_CARGO",
            "ZONE_GOAL_COALITION",
            "AIRBOSS",
            "ATIS",
            "CSAR",
            "CTLD_ENGINEERING",
            "RECOVERYTANKER",
            "RESCUEHELO",
            "RADIO",
            "RADIOQUEUE",
            "RADIOSPEECH",
            "SOUNDBASE",
            "MSRS",
            "USERSOUND",
            "COMMANDCENTER",
            "DETECTION_MANAGER",
            "MISSION",
            "TASK",
            "TASKINFO",
            "TASK_A2A",
            "TASK_A2A_DISPATCHER",
            "TASK_A2G",
            "TASK_A2G_DISPATCHER",
            "TASK_CAPTURE_DISPATCHER",
            "TASK_ZONE_GOAL",
            "TASK_CARGO",
            "TASK_CARGO_CSAR",
            "TASK_CARGO_DISPATCHER",
            "TASK_CARGO_TRANSPORT",
            "TASK_MANAGER",
            "COORDINATE_MENU",
            "FIFO",
            "PROFILER",
            "SOCKET",
            "STTS",
            "TEMPLATE",
            "AC130",
            "AIRBASE",
            "CCWEAPON",
            "CLIENT",
            "CONTROLLABLE",
            "GROUND_TRANSPORT",
            "GROUP",
            "IDENTIFIABLE",
            "MARKER",
            "OBJECT",
            "POSITIONABLE",
            "SCENERY",
            "STATIC",
            "STROBE_UNIT",
            "TANKER",
            "UAV",
            "UNIT",
        ]

        self.rules = {}
        for quote in quotes:
            self.rules[quote] = {
                "format": STYLES["string"],
                "regex": rf"{quote}"
            }

        self.rules["between_double_quotes"] = {
            "format": STYLES["string"],
            "regex": r'"[^"\\]*(\\.[^"\\]*)*"'
        }

        self.rules["between_single_quotes"] = {
            "format": STYLES["string"],
            "regex": r"'[^'\\]*(\\.[^'\\]*)*'"
        }

        self.rules["num_lit_01"] = {
            "format": STYLES["numbers"],
            "regex": r'\b[+-]?[0-9]+[lL]?\b'
        }

        self.rules["num_lit_02"] = {
            "format": STYLES["numbers"],
            "regex": r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b'
        }
        self.rules["num_lit_03"] = {
            "format": STYLES["numbers"],
            "regex": r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b'
        }

        for operator in operators:
            self.rules[operator] = {
                "format": STYLES["operator"],
                "regex": rf"{operator}"
            }

        for keyword in keywords:
            self.rules[keyword] = {
                "format": STYLES["keyword"],
                "regex": self.make_word_regex(keyword)
            }

        for keyword2 in keywords_2:
            self.rules[keyword2] = {
                "format": STYLES["numbers"],
                "regex": self.make_word_regex(keyword2)
            }

        for special_brace in special_braces:
            self.rules[special_brace] = {
                "format": STYLES["special_brace"],
                "regex": rf"{special_brace}"
            }

        for brace in normal_braces:
            self.rules[brace] = {
                "format": STYLES["normal_brace"],
                "regex": rf"{brace}"
            }

        for mooseword in glob_moose + glob:
            self.rules[mooseword] = {
                "format": STYLES["global_moose"],
                "regex": self.make_word_regex(mooseword)
            }

        self.rules["colon_function_call"] = {
            "format": STYLES["colon_function_call"],
            "regex": r'\b(\:)\b\s*(\w+)'
        }

        # self.rules["period_function_call"] = {
        #     "format": STYLES["period_function_call"],
        #     "regex": r'\b(\.)\b\s*(\w+)'
        # }

        self.rules["comment"] = {
            "format": STYLES["comment"],
            "regex": r'--[^\n]*'
        }

    def highlightBlock(self, text: str) -> None:
        for item, rule_dict in self.rules.items():
            i = QRegularExpression(rule_dict.get("regex")).globalMatch(text)
            while i.hasNext():
                match = i.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule_dict.get("format"))

    def make_word_regex(self, word):
        return rf'\b(?:{word})\b'