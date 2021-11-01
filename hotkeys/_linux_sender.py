import os
import time

from . import _sender
from Xlib.display import Display
from Xlib import X, display
import Xlib.XK


# Taken from PyKeyboard's ctor function.
_display = Display(os.environ['DISPLAY'])
root = _display.screen().root
keyboardMapping = dict([(key, None) for key in _sender.KEY_NAMES])
keyboardMapping.update({
    'backspace': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('BackSpace')),
    '\b': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('BackSpace')),
    'tab': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Tab')),
    'enter': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
    'return': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
    'shift': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_L')),
    'ctrl': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_L')),
    'alt': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_L')),
    'pause': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Pause')),
    'capslock': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Caps_Lock')),
    'esc': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
    'escape': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
    'pgup': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Up')),
    'pgdn': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Down')),
    'pageup': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Up')),
    'pagedown': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Down')),
    'end': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('End')),
    'home': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Home')),
    'left': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Left')),
    'up': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Up')),
    'right': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Right')),
    'down': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Down')),
    'select': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Select')),
    'print': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'execute': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Execute')),
    'prtsc': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'prtscr': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'prntscrn': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'printscreen': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'insert': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Insert')),
    'del': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Delete')),
    'delete': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Delete')),
    'help': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Help')),
    'win': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_L')),
    'winleft': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_L')),
    'winright': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_R')),
    'apps': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Menu')),
    'num0': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_0')),
    'num1': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_1')),
    'num2': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_2')),
    'num3': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_3')),
    'num4': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_4')),
    'num5': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_5')),
    'num6': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_6')),
    'num7': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_7')),
    'num8': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_8')),
    'num9': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_9')),
    'multiply': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Multiply')),
    'add': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Add')),
    'separator': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Separator')),
    'subtract': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Subtract')),
    'decimal': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Decimal')),
    'divide': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Divide')),
    'f1': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F1')),
    'f2': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F2')),
    'f3': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F3')),
    'f4': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F4')),
    'f5': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F5')),
    'f6': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F6')),
    'f7': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F7')),
    'f8': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F8')),
    'f9': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F9')),
    'f10': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F10')),
    'f11': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F11')),
    'f12': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F12')),
    'f13': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F13')),
    'f14': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F14')),
    'f15': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F15')),
    'f16': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F16')),
    'f17': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F17')),
    'f18': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F18')),
    'f19': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F19')),
    'f20': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F20')),
    'f21': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F21')),
    'f22': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F22')),
    'f23': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F23')),
    'f24': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F24')),
    'numlock': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Num_Lock')),
    'scrolllock': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Scroll_Lock')),
    'shiftleft': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_L')),
    'shiftright': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_R')),
    'ctrlleft': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_L')),
    'ctrlright': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_R')),
    'altleft': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_L')),
    'altright': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_R')),
    # These are added because unlike a-zA-Z0-9, the single characters do not have a
    ' ': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('space')),
    'space': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('space')),
    '\t': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Tab')),
    '\n': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
    # for some reason this needs to be cr, not lf
    '\r': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
    '\e': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
    '!': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('exclam')),
    '#': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('numbersign')),
    '%': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('percent')),
    '$': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('dollar')),
    '&': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('ampersand')),
    '"': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('quotedbl')),
    "'": _display.keysym_to_keycode(Xlib.XK.string_to_keysym('apostrophe')),
    '(': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('parenleft')),
    ')': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('parenright')),
    '*': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('asterisk')),
    '=': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('equal')),
    '+': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('plus')),
    ',': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('comma')),
    '-': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('minus')),
    '.': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('period')),
    '/': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('slash')),
    ':': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('colon')),
    ';': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('semicolon')),
    '<': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('less')),
    '>': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('greater')),
    '?': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('question')),
    '@': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('at')),
    '[': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('bracketleft')),
    ']': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('bracketright')),
    '\\': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('backslash')),
    '^': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('asciicircum')),
    '_': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('underscore')),
    '`': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('grave')),
    '{': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('braceleft')),
    '|': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('bar')),
    '}': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('braceright')),
    '~': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('asciitilde')),
})
keyboardMapping['control'] = keyboardMapping['ctrl']


class LinuxSender(_sender.SendBase):

    hotkey_map = {
        '^': X.ControlMask,
        'ctrl': X.ControlMask,
        'control': X.ControlMask,
        '+': X.ShiftMask,
        'shift': X.ShiftMask,
        '!': X.Mod1Mask,
        'alt': X.Mod1Mask,
    }

    def _compile_hotkey(self, hotkey):
        mask = 0
        for x in hotkey:
            mask |= self.hotkey_map.get(x, 0)
        self._compile_keydown(hotkey[-1], mask=mask)
        self._compile_keyup(hotkey[-1], mask=mask)

    def _compile_keydown(self, key, sleep=True, mask=0):
        is_shift = self.is_shift_character(key)
        if is_shift:
            mask |= X.ShiftMask
        key_codes = self.key_codes
        x = keyboardMapping.get(key)
        if not x:
            keyboardMapping[key] = x = \
                _display.keysym_to_keycode(Xlib.XK.string_to_keysym(key))
            if not x:
                raise ValueError(f'Unknown Key {key}')
        key_codes.append((x,
                          True,
                          sleep or len(key_codes) < 3,
                          mask))

    def _compile_keyup(self, key, sleep=True, mask=0):
        is_shift = self.is_shift_character(key)
        if is_shift:
            mask |= X.ShiftMask
        x = keyboardMapping.get(key)
        if not x:
            keyboardMapping[key] = x = \
                _display.keysym_to_keycode(Xlib.XK.string_to_keysym(key))
            if not x:
                raise ValueError(f'Unknown Key {key}')
        self.key_codes.append((x,
                               False,
                               sleep or len(self.key_codes) < 3,
                               mask))

    def _compile_press(self, x):
        self._compile_keydown(x, False)
        self._compile_keyup(x)

    def _compile_end(self):
        pass

    def send(self, send_delay=0.003):
        # Ensure focused
        focus = _display.get_input_focus()
        _display.set_input_focus(focus.focus, focus.revert_to, X.CurrentTime)
        window = focus.focus
        send_event = getattr(
            window,
            'send_event',
            lambda ev: _display.send_event(window, ev, propagate=True))
        for key, press, delay, mods in self.key_codes:
            event = display.event.KeyPress if press else display.event.KeyRelease
            send_event(event(
                detail=key,
                state=mods,
                time=X.CurrentTime,
                root=root,
                window=window,
                same_screen=0,
                child=Xlib.X.NONE,
                root_x=0, root_y=0, event_x=0, event_y=0))
            if delay:
                time.sleep(send_delay)
            _display.sync()

    def get_active_win(self):
        return _display.get_input_focus().focus