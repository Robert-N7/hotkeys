import ctypes
import ctypes.wintypes

from ._sender import SendBase, KEY_NAMES

# Documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646304(v=vs.85).aspx
KEYEVENTF_KEYDOWN = 0x0000  # Technically this constant doesn't exist in the MS documentation. It's the lack of KEYEVENTF_KEYUP that means pressing the key down.
KEYEVENTF_KEYUP = 0x0002

keyboardMapping = dict([(key, None) for key in KEY_NAMES])
keyboardMapping.update({
    'backspace': 0x08,  # VK_BACK
    '\b': 0x08,  # VK_BACK
    'super': 0x5B,  # VK_LWIN
    'tab': 0x09,  # VK_TAB
    '\t': 0x09,  # VK_TAB
    'clear': 0x0c,  # VK_CLEAR
    'enter': 0x0d,  # VK_RETURN
    '\n': 0x0d,  # VK_RETURN
    'return': 0x0d,  # VK_RETURN
    'shift': 0x10,  # VK_SHIFT
    'ctrl': 0x11,  # VK_CONTROL
    'alt': 0x12,  # VK_MENU
    'pause': 0x13,  # VK_PAUSE
    'capslock': 0x14,  # VK_CAPITAL
    'kana': 0x15,  # VK_KANA
    'hanguel': 0x15,  # VK_HANGUEL
    'hangul': 0x15,  # VK_HANGUL
    'junja': 0x17,  # VK_JUNJA
    'final': 0x18,  # VK_FINAL
    'hanja': 0x19,  # VK_HANJA
    'kanji': 0x19,  # VK_KANJI
    'esc': 0x1b,  # VK_ESCAPE
    'escape': 0x1b,  # VK_ESCAPE
    'convert': 0x1c,  # VK_CONVERT
    'nonconvert': 0x1d,  # VK_NONCONVERT
    'accept': 0x1e,  # VK_ACCEPT
    'modechange': 0x1f,  # VK_MODECHANGE
    ' ': 0x20,  # VK_SPACE
    'space': 0x20,  # VK_SPACE
    'pgup': 0x21,  # VK_PRIOR
    'pgdn': 0x22,  # VK_NEXT
    'pageup': 0x21,  # VK_PRIOR
    'pagedown': 0x22,  # VK_NEXT
    'end': 0x23,  # VK_END
    'home': 0x24,  # VK_HOME
    'left': 0x25,  # VK_LEFT
    'up': 0x26,  # VK_UP
    'right': 0x27,  # VK_RIGHT
    'down': 0x28,  # VK_DOWN
    'select': 0x29,  # VK_SELECT
    'print': 0x2a,  # VK_PRINT
    'execute': 0x2b,  # VK_EXECUTE
    'prtsc': 0x2c,  # VK_SNAPSHOT
    'prtscr': 0x2c,  # VK_SNAPSHOT
    'prntscrn': 0x2c,  # VK_SNAPSHOT
    'printscreen': 0x2c,  # VK_SNAPSHOT
    'insert': 0x2d,  # VK_INSERT
    'del': 0x2e,  # VK_DELETE
    'delete': 0x2e,  # VK_DELETE
    'help': 0x2f,  # VK_HELP
    'win': 0x5b,  # VK_LWIN
    'winleft': 0x5b,  # VK_LWIN
    'winright': 0x5c,  # VK_RWIN
    'apps': 0x5d,  # VK_APPS
    'sleep': 0x5f,  # VK_SLEEP
    'num0': 0x60,  # VK_NUMPAD0
    'num1': 0x61,  # VK_NUMPAD1
    'num2': 0x62,  # VK_NUMPAD2
    'num3': 0x63,  # VK_NUMPAD3
    'num4': 0x64,  # VK_NUMPAD4
    'num5': 0x65,  # VK_NUMPAD5
    'num6': 0x66,  # VK_NUMPAD6
    'num7': 0x67,  # VK_NUMPAD7
    'num8': 0x68,  # VK_NUMPAD8
    'num9': 0x69,  # VK_NUMPAD9
    'multiply': 0x6a,  # VK_MULTIPLY  ??? Is this the numpad *?
    'add': 0x6b,  # VK_ADD  ??? Is this the numpad +?
    'separator': 0x6c,  # VK_SEPARATOR  ??? Is this the numpad enter?
    'subtract': 0x6d,  # VK_SUBTRACT  ??? Is this the numpad -?
    'decimal': 0x6e,  # VK_DECIMAL
    'divide': 0x6f,  # VK_DIVIDE
    'f1': 0x70,  # VK_F1
    'f2': 0x71,  # VK_F2
    'f3': 0x72,  # VK_F3
    'f4': 0x73,  # VK_F4
    'f5': 0x74,  # VK_F5
    'f6': 0x75,  # VK_F6
    'f7': 0x76,  # VK_F7
    'f8': 0x77,  # VK_F8
    'f9': 0x78,  # VK_F9
    'f10': 0x79,  # VK_F10
    'f11': 0x7a,  # VK_F11
    'f12': 0x7b,  # VK_F12
    'f13': 0x7c,  # VK_F13
    'f14': 0x7d,  # VK_F14
    'f15': 0x7e,  # VK_F15
    'f16': 0x7f,  # VK_F16
    'f17': 0x80,  # VK_F17
    'f18': 0x81,  # VK_F18
    'f19': 0x82,  # VK_F19
    'f20': 0x83,  # VK_F20
    'f21': 0x84,  # VK_F21
    'f22': 0x85,  # VK_F22
    'f23': 0x86,  # VK_F23
    'f24': 0x87,  # VK_F24
    'numlock': 0x90,  # VK_NUMLOCK
    'scrolllock': 0x91,  # VK_SCROLL
    'shiftleft': 0xa0,  # VK_LSHIFT
    'shiftright': 0xa1,  # VK_RSHIFT
    'ctrlleft': 0xa2,  # VK_LCONTROL
    'ctrlright': 0xa3,  # VK_RCONTROL
    'altleft': 0xa4,  # VK_LMENU
    'altright': 0xa5,  # VK_RMENU
    'browserback': 0xa6,  # VK_BROWSER_BACK
    'browserforward': 0xa7,  # VK_BROWSER_FORWARD
    'browserrefresh': 0xa8,  # VK_BROWSER_REFRESH
    'browserstop': 0xa9,  # VK_BROWSER_STOP
    'browsersearch': 0xaa,  # VK_BROWSER_SEARCH
    'browserfavorites': 0xab,  # VK_BROWSER_FAVORITES
    'browserhome': 0xac,  # VK_BROWSER_HOME
    'volumemute': 0xad,  # VK_VOLUME_MUTE
    'volumedown': 0xae,  # VK_VOLUME_DOWN
    'volumeup': 0xaf,  # VK_VOLUME_UP
    'nexttrack': 0xb0,  # VK_MEDIA_NEXT_TRACK
    'prevtrack': 0xb1,  # VK_MEDIA_PREV_TRACK
    'stop': 0xb2,  # VK_MEDIA_STOP
    'playpause': 0xb3,  # VK_MEDIA_PLAY_PAUSE
    'launchmail': 0xb4,  # VK_LAUNCH_MAIL
    'launchmediaselect': 0xb5,  # VK_LAUNCH_MEDIA_SELECT
    'launchapp1': 0xb6,  # VK_LAUNCH_APP1
    'launchapp2': 0xb7,  # VK_LAUNCH_APP2
})
keyboardMapping['control'] = keyboardMapping['ctrl']

for c in range(32, 128):
    keyboardMapping[chr(c)] = ctypes.windll.user32.VkKeyScanA(ctypes.wintypes.WCHAR(chr(c)))


class WinSender(SendBase):
    def _compile_hotkey(self, hotkey):
        for x in hotkey:
            self._compile_keydown(x)
        hotkey.reverse()
        for x in hotkey:
            self._compile_keyup(x)

    def _compile_press(self, key):
        self._compile_keydown(key, False)
        self._compile_keyup(key)

    def _compile_keyup(self, key, sleep=True):
        needsShift = self.is_shift_character(key)
        code = self.__get_code(key)
        mods, vkCode = divmod(code, 0x100)

        for apply_mod, vk_mod in [(mods & 4, 0x12), (mods & 2, 0x11),
                                  (mods & 1 or needsShift, 0x10)]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                self.key_codes.append((vk_mod, 0, sleep))
        self.key_codes.append((vkCode, KEYEVENTF_KEYUP, sleep))
        for apply_mod, vk_mod in [(mods & 1 or needsShift, 0x10), (mods & 2, 0x11),
                                  (mods & 4, 0x12)]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                self.key_codes.append((vk_mod, KEYEVENTF_KEYUP, sleep))

    @staticmethod
    def __get_code(key):
        code = keyboardMapping[key]
        if not code:
            raise KeyError(key)
        return code

    def _compile_keydown(self, key, sleep=True):
        needsShift = self.is_shift_character(key)
        code = self.__get_code(key)
        mods, vkCode = divmod(code, 0x100)

        for apply_mod, vk_mod in [(mods & 4, 0x12), (mods & 2, 0x11),
                                  (mods & 1 or needsShift, 0x10)]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                self.key_codes.append((vk_mod, KEYEVENTF_KEYDOWN, sleep))
        self.key_codes.append((vkCode, KEYEVENTF_KEYDOWN, sleep))

        for apply_mod, vk_mod in [(mods & 1 or needsShift, 0x10), (mods & 2, 0x11),
                                  (mods & 4, 0x12)]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                self.key_codes.append((vk_mod, KEYEVENTF_KEYUP, sleep))

    def _compile_end(self):
        pass

    def send(self, send_delay=0.003):
        for key, press, delay in self.key_codes:
            ctypes.windll.user32.keybd_event(key, 0, press, 0)

    def get_active_win(self):
        pass


# hotkey registry remapper
KEY_REMAP = {}

# Hotkeys registry remapping
from system_hotkey import vk_codes
vk_codes.update({
    'numlock': 0x90,
    'scrolllock': 0x91,
    'lshift': 0xA0,
    'rshift': 0xA1,
    'lcontrol': 0xA2,
    'rcontrol': 0xA3,
    'lmenu': 0xA4,
    'rmenu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_down': 0xAE,
    'volume_up': 0xAF,
    'media_next_track': 0xB0,
    'media_prev_track': 0xB1,
    'media_stop': 0xB2,
    'media_play_pause': 0xB3,
    'launch_mail': 0xB4,
    'launch_media_select': 0xB5,
    'launch_app1': 0xB6,
    'launch_app2': 0xB7,
    ';': 0xBA,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
    'play': 0xFA,
    'zoom': 0xFB,
    'clear': 0xFE,
})
