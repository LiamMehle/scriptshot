'''uninstalls the script and performs cleanup'''

import os
import package_handler

NAME = 'uninstaller'

def log(msg: str) -> None:
    '''logging function to replace print()'''
    print(f'[{NAME}] {msg}')

packages = ('pynput', 'pyautogui')

log('uninstalling packages')
package_handler.uninstall(packages)
log('done')
log('deleting scriptshot')


# delete all files
for file in os.listdir('.'):
    os.remove(file)

log('done')
log('removing folder')
os.rmdir('.')
log('done')
log('goodbye')
