import platform

from setuptools import setup

requirements = [
        'pyperclip',
        'system_hotkey',
    ]

p = platform.system()
if p == 'Windows':
    requirements.append('pywin32')
elif p == 'Linux':
    requirements.append('xcffib')
    requirements.append('xpybutil')
    requirements.append('Xlib')

setup(
    name='hotkeys',
    version='0.1.0',
    packages=['hotkeys'],
    url='https://github.com/Robert-N7/hotkeys',
    license='GPL3',
    author='Robert',
    author_email='robert7.nelson@gmail.com',
    description='A package for hotkeys',
    install_requires=requirements
)
