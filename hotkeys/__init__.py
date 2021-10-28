import os
import platform
import subprocess
import sys
import time

import pyperclip
from system_hotkey import SystemHotkey
import pyautogui as HK

SEND_INTERVAL = 0.00
HK_CLIPBOARD = None

if sys.platform == "darwin":
    from . import _pyautogui_osx as platformModule
elif sys.platform == "win32":
    from . import _pyautogui_win as platformModule
elif platform.system() == "Linux":
    from ._linux_sender import LinuxSender as Sender
else:
    raise NotImplementedError("Your platform (%s) is not supported by PyAutoGUI." % (platform.system()))


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


def send_raw(text, interval=None):
    return HK.write(text, interval or SEND_INTERVAL)


def send_input(text, interval=None):
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
    interval = interval or SEND_INTERVAL
    if type(text) is not str:
        text = ''.join(text)
    n_str = ''
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
                            raise HKParserError(f'Multi-Space not allowed {text[i:j]}')
                        key = text[i:j]
                        i = j + 1
                    j += 1
                if j >= l:
                    raise HKParserError(f'Mismatched brackets {text}')
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
                        HK.hotkey(*hk)
                        time.sleep(interval)
                else:
                    if len(hk) > 1:
                        raise HKParserError(f'Multi-keys not supported with {mod} modifier')
                    mod = mod.lower()
                    if mod == 'down':
                        HK.keyDown(hk[0])
                    elif mod == 'up':
                        HK.keyUp(hk[0])
                    else:
                        raise HKParserError(f'Unknown modifier {mod}')
                hk = []
                i = j
            else:
                send_literal = True
        else:
            send_literal = True
            literal = False
        if send_literal:
            if (prev_special):
                # reset str built
                if n_str:
                    send_raw(n_str, interval)
                    time.sleep(interval)
                    n_str = ''
                hk.append(c)
                HK.hotkey(*hk)
                time.sleep(interval)
                hk = []
            else:
                n_str += c
            special_switch = False
        prev_special = special_switch
        i += 1
    if n_str:
        send_raw(n_str, interval)


def send(text, interval=None):
    sender = Sender(text)
    sender.send()
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

    def __init__(self, keys, bind_to, raw=False, delay=-1.0):
        try:
            some_object_iterator = iter(bind_to)
            f = send_raw if raw else send
            if delay == -1:
                delay = 0.05
            self.bind_to = lambda *args, **kwargs: f(bind_to)
        except TypeError as te:
            self.bind_to = bind_to
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
        self.reset_keys = ''
        if len(hk) > 1:
            hk.reverse()
            for i in range(1, len(hk)):
                self.reset_keys += '{' + hk[i] + ' up}'

    def __call__(self, *args, **kwargs):
        start = time.time()
        kwargs['hotkey'] = self
        # quick pause to release key
        if self.delay > 0:
            time.sleep(self.delay)
        if self.reset_keys:
            send(self.reset_keys, 0.01)
        self.bind_to()

    def unregister(self):
        self.SYS_HOTKEY.unregister(self.keys)
        self.keys = None

    def set_callback(self, callback):
        self.bind_to = callback


HK_QUIT_KEY = Hotkey('^{Esc}', Hotkey.quit)
# endregion
