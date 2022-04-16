# This can be used to modify the xlib key modifiers to use specific modifiers by hotkeys
# It only needs to be ran when changing your key binding configuration

import os
import sys


def set_key_map(mods, clear=None, add=None):
    commands = ['clear ' + x for x in mods]
    if clear:
        commands.extend(['clear ' + x for x in clear])
    commands.extend(['add ' + x + ' = ' + mods[x] for x in mods])
    if add:
        commands.extend(['add ' + x + ' = ' + add[x] for x in add])
    local_file = '\n'.join(commands)

    home = os.getenv('HOME')
    local_file_path = f'{home}/.Xmodmap'
    profile_path = f'{home}/.bashrc'
    auto_load = '''
    # Load custom key modifiers
    xmodmap "$HOME/.Xmodmap"
    '''
    with open(local_file_path, 'w') as f:
        f.write(local_file)

    contents = ''
    if os.path.exists(profile_path):
        with open(profile_path) as f:
            contents = f.read()
        if auto_load in contents:
            return
    contents += auto_load
    with open(profile_path, 'w') as f:
        f.write(contents)
    os.system('. ' + profile_path)


if __name__ == '__main__':
    mods = {
        'Control': 'Control_L',
        'mod1': 'Alt_L',
        'mod2': 'Alt_R',
        'mod3': 'Control_R',
        'mod4': 'Super_L',
        'mod5': 'Super_R',
    }
    clear = [

    ]
    add = {

    }
    set_key_map(mods, clear, add)
