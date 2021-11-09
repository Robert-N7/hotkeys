import platform
import sys
import time
import traceback

import pyperclip
from system_hotkey import SystemHotkey

SEND_INTERVAL = 0.003
ALLOW_PASTE = True
HK_CLIPBOARD = None

if platform.system() == "Linux":
    from ._linux_sender import LinuxSender as Sender
    from ._linux_sender import KEY_REMAP
elif platform.system() == "Windows":
    from ._win_sender import WinSender as Sender
    from ._win_sender import KEY_REMAP
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


def clip_get():
    return pyperclip.paste()


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
class Hotkey:
    ON_ERR_QUIT = 0
    ON_ERR_CONTINUE = 1
    SYS_HOTKEY = SystemHotkey()
    hk_quit = False
    hk_pause = False
    paused = []
    err_handler = ON_ERR_CONTINUE

    @staticmethod
    def wait():
        while not Hotkey.hk_quit:
            time.sleep(0.2)

    @staticmethod
    def quit(hotkey=None):
        Hotkey.hk_quit = True

    @staticmethod
    def toggle_pause(hotkey=None):
        Hotkey.unpause() if Hotkey.hk_pause else Hotkey.pause()

    @staticmethod
    def unpause(hotkey=None):
        Hotkey.hk_pause = False
        for x in Hotkey.paused:
            x.set_keys(x.original_keys)
        Hotkey.paused = []

    @staticmethod
    def pause(hotkey=None):
        Hotkey.hk_pause = True

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

    def register(self):
        try:
            keys = [KEY_REMAP.get(x) or x for x in self.keys]
            self.SYS_HOTKEY.register(keys, callback=self)
        except KeyError as e:
            raise InvalidKeyError(str(e), self)

    def set_keys(self, text):
        if hasattr(self, 'keys') and self.keys:
            self.unregister()
        if type(text) is not str:
            return text
        self.original_keys = text
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
                    key = text[i:j].lower()
                    hk.append(key)
                    i = j
                    done = True
                else:
                    send_literal = True
            else:
                send_literal = True
                literal = False
            if send_literal:
                hk.append(c)
                done = True
            i += 1
        self.keys = tuple(hk)
        hk.reverse()
        r = ''
        for i in range(0, len(hk)):
            r += '{' + hk[i] + ' up}'
        self.reset_keys = Sender(r)
        self.register()

    def __call__(self, *args, **kwargs):
        if self.hk_pause and self.bind_to not in (self.toggle_pause, self.quit, self.unpause):
            self.unregister()
            self.paused.append(self)
            time.sleep(0.01)
            send(self.original_keys)
            return
        # quick pause to release key
        if self.delay > 0:
            time.sleep(self.delay)
        if self.reset_keys:
            self.reset_keys.send()
        try:
            self.bind_to(self)
        except Exception as e:
            if self.bind_to is self.quit:
                # quit method failed, try direct approach
                sys.exit(1)
            elif self.err_handler == self.ON_ERR_QUIT:
                Hotkey.quit(self)
                raise e
            elif self.err_handler == self.ON_ERR_CONTINUE:
                print(traceback.format_exc())

    def unregister(self):
        self.SYS_HOTKEY.unregister([KEY_REMAP.get(x) or x for x in self.keys])
        self.keys = None

    def set_callback(self, callback):
        self.bind_to = callback

# endregion
