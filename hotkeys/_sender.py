
class SendBase:
    shift_chars = set('~!@#$%^&*()_+{}|:"<>?')

    class HKParserError(Exception): pass

    def __init__(self, text, raw=False):
        self.key_codes = []
        if raw:
            self.compile_raw(text)
        else:
            self.compile(text)

    def __call__(self, *args, **kwargs):
        self.send(kwargs.get('send_delay'))

    @staticmethod
    def is_shift_character(key):
        return key.isupper() or key in SendBase.shift_chars

    def compile_raw(self, text):
        for x in text:
            self._compile_press(x)

    def compile(self, text):
        """
        Sends the text with certain special rules.
        ^ = ctrl
        ! = alt
        + = shift
        # = windows key
        :param text: array or string
        :param interval: float, seconds to delay
        :return: None
        """
        if type(text) is not str:
            text = ''.join(text)
        prev_special = literal = False
        hk = []
        i = 0
        l = len(text)
        while i < l:
            c = text[i]
            special_switch = True
            send_literal = False
            if not literal:
                if c == '!':
                    hk.append('alt')
                elif c == '^':
                    hk.append('ctrl')
                elif c == '#':
                    hk.append('win')
                elif c == '+':
                    hk.append('shift')
                elif c == '`':
                    literal = True
                elif c == '{':
                    i += 1
                    j = i
                    send_times = 1
                    key = mod = None
                    while j < l and text[j] != '}':
                        if text[j] == ' ':
                            if key:
                                raise self.HKParserError(f'Multi-Space not allowed {text[i:j]}')
                            key = text[i:j]
                            i = j + 1
                        j += 1
                    if j >= l:
                        raise self.HKParserError(f'Mismatched brackets {text}')
                    if not key:
                        key = text[i:j]
                    else:
                        mod = text[i:j]
                        try:
                            send_times = int(mod)
                            mod = None
                        except ValueError:
                            pass
                    hk.append(key)
                    if not mod:
                        for k in range(send_times):
                            self._compile_hotkey(hk)
                    else:
                        if len(hk) > 1:
                            raise self.HKParserError(f'Multi-keys not supported with {mod} modifier')
                        mod = mod.lower()
                        if mod == 'down':
                            self._compile_keydown(hk[0])
                        elif mod == 'up':
                            self._compile_keyup(hk[0])
                        else:
                            raise self.HKParserError(f'Unknown modifier {mod}')
                    hk = []
                    i = j
                else:
                    send_literal = True
            else:
                send_literal = True
                literal = False
            if send_literal:
                if prev_special:
                    hk.append(c)
                    self._compile_hotkey(hk)
                    hk = []
                else:
                    self._compile_press(c)
                special_switch = False
            prev_special = special_switch
            i += 1
        self._compile_end()

    def _compile_hotkey(self, hotkey):
        raise NotImplementedError()

    def _compile_press(self, key):
        raise NotImplementedError()

    def _compile_keyup(self, key):
        raise NotImplementedError()

    def _compile_keydown(self, key):
        raise NotImplementedError()

    def _compile_end(self):
        raise NotImplementedError()

    def send(self, send_delay):
        raise NotImplementedError()


KEY_NAMES = [
    "\t",
    "\n",
    "\r",
    " ",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    "accept",
    "add",
    "alt",
    "altleft",
    "altright",
    "apps",
    "backspace",
    "browserback",
    "browserfavorites",
    "browserforward",
    "browserhome",
    "browserrefresh",
    "browsersearch",
    "browserstop",
    "capslock",
    "clear",
    "convert",
    "ctrl",
    "ctrlleft",
    "ctrlright",
    "decimal",
    "del",
    "delete",
    "divide",
    "down",
    "end",
    "enter",
    "esc",
    "escape",
    "execute",
    "f1",
    "f10",
    "f11",
    "f12",
    "f13",
    "f14",
    "f15",
    "f16",
    "f17",
    "f18",
    "f19",
    "f2",
    "f20",
    "f21",
    "f22",
    "f23",
    "f24",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "final",
    "fn",
    "hanguel",
    "hangul",
    "hanja",
    "help",
    "home",
    "insert",
    "junja",
    "kana",
    "kanji",
    "launchapp1",
    "launchapp2",
    "launchmail",
    "launchmediaselect",
    "left",
    "modechange",
    "multiply",
    "nexttrack",
    "nonconvert",
    "num0",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num6",
    "num7",
    "num8",
    "num9",
    "numlock",
    "pagedown",
    "pageup",
    "pause",
    "pgdn",
    "pgup",
    "playpause",
    "prevtrack",
    "print",
    "printscreen",
    "prntscrn",
    "prtsc",
    "prtscr",
    "return",
    "right",
    "scrolllock",
    "select",
    "separator",
    "shift",
    "shiftleft",
    "shiftright",
    "sleep",
    "space",
    "stop",
    "subtract",
    "tab",
    "up",
    "volumedown",
    "volumemute",
    "volumeup",
    "win",
    "winleft",
    "winright",
    "yen",
    "command",
    "option",
    "optionleft",
    "optionright",
]
