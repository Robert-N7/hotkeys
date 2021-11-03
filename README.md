# Intro
Hotkeys is a package for creating system hotkeys, 
and sending key-strokes to the screen.

# Hotkeys Setup
First install any dependencies for your platform, then install python packages.

## Ubuntu
```
sudo apt-get install python3-tk python3-dev xsel
```

## Windows
Supported - No dependencies

## Mac
Unsupported

## Install python packages

```
pip install -r requirements.txt
```

### Hello World example
Send the text "Hello world!" every time you place alt+d.
```
from hotkeys import Hotkey
h = Hotkey('!d', 'Hello world!', raw=True)
Hotkey.wait()
```
The first parameter to Hotkey is the key trigger, note special keys:
* ! = alt
* ^ = ctrl
* \+ = shift
    
The next parameter is what to bind to, which can be text to send, or a custom function.
`raw` tells hotkey to process it as raw text rather than binding special keys. 
`Hotkey.wait()` keeps the script running indefinitely until `Hotkey.quit()` is called.
`Shift+Escape` is set by default as the quit hotkey.

## Sending special keys
In addition to the special keys mentioned above, hotkey can send other keys in brackets.
```
send('^{end}')
```
Sends Ctrl+End to the current window.

## Pause hotkeys
Sometimes it is useful to pause hotkeys to resume normal functionality:

```
Hotkey('{pause}', Hotkey.toggle_pause)
```
Here we create a hotkey using the `pause` button that toggles all other hotkeys.
Hotkeys connected to toggle_pause, unpause, or quit will still operate as normal during pause.
