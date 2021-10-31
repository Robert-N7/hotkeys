import platform
import time

import pyperclip
from system_hotkey import SystemHotkey

SEND_INTERVAL = 0.003
ALLOW_PASTE = True
HK_CLIPBOARD = None

# if sys.platform == "darwin":
#     from . import _pyautogui_osx as platformModule
# elif sys.platform == "win32":
#     from . import _pyautogui_win as platformModule
#
if platform.system() == "Linux":
    from ._linux_sender import LinuxSender as Sender
else:
    raise NotImplementedError("Your platform (%s) is not supported by Hotkeys." % (platform.system()))


# region Exceptions
class HotkeyError(Exception):
    def __init__(self, message, hk):
        super().__init__(f'HK error "{hk.keys}":' + message)


class InvalidKeyError(HotkeyError): pass


class HKParserError(Exception): pass
# endregion

# region send
def clip(text):
    pyperclip.copy(text)


def clip_wait(amount=0.2):
    timer = 0
    increment = 0.01
    s = ''
    while timer < amount:
        s = pyperclip.paste()
        if s:
            break
        time.sleep(increment)
        timer += increment
    return s


def send_paste(text, interval=None):
    pyperclip.copy(text)
    sender = Sender('^v')
    sender.send(interval or SEND_INTERVAL)
    return sender


def send(text, interval=None, raw=False):
    sender = Sender(text, raw)
    sender.send(interval or SEND_INTERVAL)
    return sender

# endregion

# region Hotkey
class Hotkey():
    SYS_HOTKEY = SystemHotkey()
    HK_QUIT = False

    KEY_REMAP = {
        'esc': 'escape',
        ' ': "space",
        '\t': "tab",
        '\n': "return",
        '\r': "return",
        '\e': "escape",
        '!': "exclam",
        '#': "numbersign",
        '%': "percent",
        '$': "dollar",
        '&': "ampersand",
        '"': "quotedbl",
        '\'': "apostrophe",
        '(': "parenleft",
        ')': "parenright",
        '*': "asterisk",
        '=': "equal",
        '+': "plus",
        ',': "comma",
        '-': "minus",
        '.': "period",
        '/': "slash",
        ':': "colon",
        ';': "semicolon",
        '<': "less",
        '>': "greater",
        '?': "question",
        '@': "at",
        '[': "bracketleft",
        ']': "bracketright",
        '\\': "backslash",
        '^': "asciicircum",
        '_': "underscore",
        '`': "grave",
        '{': "braceleft",
        '|': "bar",
        '}': "braceright",
        '~': "asciitilde"
    }

    @staticmethod
    def wait():
        while not Hotkey.HK_QUIT:
            time.sleep(0.2)

    @staticmethod
    def quit(*args, **kwargs):
        Hotkey.HK_QUIT = True

    def __init__(self, keys, bind_to, raw=True, delay=-1.0):
        try:
            some_object_iterator = iter(bind_to)
            if raw and ALLOW_PASTE and len(bind_to) > 9:
                self.bind_to = lambda *args, **kwargs: send_paste(bind_to)
            else:
                self.bind_to = Sender(bind_to, raw)
        except TypeError as te:
            self.bind_to = bind_to
        if delay < 0.0:
            delay = 0.03
        self.set_keys(keys)
        self.delay = delay
        try:
            self.SYS_HOTKEY.register(self.keys, callback=self)
        except KeyError as e:
            raise InvalidKeyError(str(e), self)

    def set_keys(self, text):
        if hasattr(self, 'keys') and self.keys:
            self.unregister()
        if type(text) is not str:
            return text
        hk = []
        done = literal = False
        i = 0
        while i < len(text):
            c = text[i]
            send_literal = False
            if done:
                raise ValueError(f'Failed to parse hotkey {text}')
            if not literal:
                if c == '!':
                    hk.append('alt')
                elif c == '^':
                    hk.append('control')
                elif c == '#':
                    hk.append('win')
                elif c == '+':
                    hk.append('shift')
                elif c == '`':
                    literal = True
                elif c == '{':
                    i += 1
                    j = i
                    while text[j] != '}':
                        j += 1
                    key = text[i:j]
                    rkey = self.KEY_REMAP.get(key.lower())
                    hk.append(rkey or key)
                    i = j
                    done = True
                else:
                    send_literal = True
            else:
                send_literal = True
                literal = False
            if send_literal:
                rkey = self.KEY_REMAP.get(c)
                hk.append(rkey or c)
                done = True
            i += 1
        self.keys = tuple(hk)
        hk.reverse()
        r = ''
        for i in range(0, len(hk)):
            r += '{' + hk[i] + ' up}'
        self.reset_keys = Sender(r)

    def __call__(self, *args, **kwargs):
        kwargs['hotkey'] = self
        # quick pause to release key
        if self.delay > 0:
            time.sleep(self.delay)
        if self.reset_keys:
            self.reset_keys.send()
        self.bind_to(*args, **kwargs)

    def unregister(self):
        self.SYS_HOTKEY.unregister(self.keys)
        self.keys = None

    def set_callback(self, callback):
        self.bind_to = callback


HK_QUIT_KEY = Hotkey('^{Esc}', Hotkey.quit)
# endregion
