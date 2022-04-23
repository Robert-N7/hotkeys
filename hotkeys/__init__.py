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

    def run(hk):
        return hk.bound_method_callback(hk)
elif platform.system() == "Windows":
    from ._win_sender import WinSender as Sender
    from ._win_sender import KEY_REMAP

    def run(hk):
        # On windows, if we finish quickly send any modifier keys again
        # This allows us to hold modifiers down
        start = time.time()
        result = hk.bound_method_callback(hk)
        # 0.25 secs is about the shortest amount of time to hold a key
        # Any shorter press will result in the key remaining in the held down state
        # Any execution time longer than 0.25 will have to re-press the modifiers down
        # In the future, it would be better to detect what state the key is in and match it
        if time.time() - start < 0.25:
            keys = Sender(['{' + hk.keys[i] + ' down}' for i in range(len(hk.keys) - 1)])
            keys.send()
        return result

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
    hk_quit_callback = None
    paused = []
    err_handler = ON_ERR_CONTINUE

    @staticmethod
    def wait():
        while not Hotkey.hk_quit:
            time.sleep(0.2)

    @staticmethod
    def quit(hotkey=None):
        Hotkey.hk_quit = True
        Hotkey.paused = None
        Hotkey.SYS_HOTKEY = None
        if Hotkey.hk_quit_callback:
            Hotkey.hk_quit_callback()

    @staticmethod
    def set_quit(fptr):
        Hotkey.hk_quit_callback = fptr

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

    def __init__(self, keys, bind=None, raw=True, delay=-1.0, overwrite=False):
        self.overwrite = overwrite
        self.__run_method = run
        self.is_registered = False
        if delay < 0.0:
            delay = 0.03
        self.__sleep_delay = delay
        if bind:
            self.bind_to(bind, raw)
        self.set_keys(keys)

    def register(self):
        if self.is_registered:
            return
        try:
            keys = [KEY_REMAP.get(x) or x for x in self.keys]
            self.SYS_HOTKEY.register(keys, callback=self, overwrite=self.overwrite)
            self.is_registered = True
        except KeyError as e:
            raise InvalidKeyError(str(e), self)

    def set_keys(self, text):
        if self.is_registered:
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
        if self.hk_pause and self.bound_method_callback not in (self.toggle_pause, self.quit, self.unpause):
            self.unregister()
            self.paused.append(self)
            time.sleep(0.01)
            send(self.original_keys)
            return
        # quick pause to release key
        if self.__sleep_delay > 0:
            time.sleep(self.__sleep_delay)
        if self.reset_keys:
            self.reset_keys.send()
        try:
            self.__run_method(self)
        except Exception as e:
            if self.bound_method_callback is self.quit:
                # quit method failed, try direct approach
                sys.exit(1)
            elif self.err_handler == self.ON_ERR_QUIT:
                Hotkey.quit(self)
                raise e
            elif self.err_handler == self.ON_ERR_CONTINUE:
                print(traceback.format_exc())

    def unregister(self):
        if not self.is_registered:
            return
        self.SYS_HOTKEY.unregister([KEY_REMAP.get(x) or x for x in self.keys])
        self.is_registered = False

    def bind_to(self, bind, raw=True):
        try:
            some_object_iterator = iter(bind)
            if raw and ALLOW_PASTE and len(bind) > 9:
                self.bound_method_callback = lambda *args, **kwargs: send_paste(bind)
            else:
                self.bound_method_callback = Sender(bind, raw)
        except TypeError as te:
            self.bound_method_callback = bind


# endregion

if platform.system() == "Linux":
    # Note only works if using xcb lib
    from system_hotkey.xpybutil_keybind import get_min_max_keycode, __kbmap, get_keysym
    from system_hotkey.keysymdef import keysyms

    def set_key_map(mods=None, ignore_mods=None, reset=False):
        if mods:
            mods = {x.lower(): mods[x] for x in mods}
            modders = Hotkey.SYS_HOTKEY.modders
            if reset:
                modders.clear()
            reversed = {v: k for k, v in modders.items()}
            for x in mods:
                if mods[x] in reversed:
                    KEY_REMAP[x] = reversed[mods[x]]
                else:
                    modders[x] = mods[x]
            Hotkey.SYS_HOTKEY.get_modifiersym = lambda state: [
                k for k, v in Hotkey.SYS_HOTKEY.modders.items() if state & v
            ]
            Sender.hotkey_map.update(mods)

        if ignore_mods:
            for i in range(len(ignore_mods) - 1):
                x = ignore_mods[i]
                for j in range(i + 1, len(ignore_mods)):
                    x |= ignore_mods[j]
                    ignore_mods.append(x)
            ignore = set(ignore_mods)
            ignore.add(0)
            Hotkey.SYS_HOTKEY.trivial_mods = ignore


    # cache keycode lookup table
    # While this takes longer at startup,
    # it makes future lookups O(1) instead of O(i*j)
    KEYCODE_LOOKUP = {}
    mn, mx = get_min_max_keycode()
    cols = __kbmap.keysyms_per_keycode
    for i in range(mn, mx + 1):
        found = False
        for j in range(0, cols):
            ks = get_keysym(i, col=j)
            if ks:
                if found and not KEYCODE_LOOKUP.get(ks):
                    KEYCODE_LOOKUP[ks] = i
                    break
                if not KEYCODE_LOOKUP.get(ks):
                    KEYCODE_LOOKUP[ks] = i
                    found = True


    def lookup_key_code(kstr):
        if kstr in keysyms:
            return KEYCODE_LOOKUP.get(keysyms[kstr])
        elif len(kstr) > 1 and kstr.capitalize() in keysyms:
            return KEYCODE_LOOKUP.get(keysyms[kstr.capitalize()])
        return


    Hotkey.SYS_HOTKEY._get_keycode = lookup_key_code
