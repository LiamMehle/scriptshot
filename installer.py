'''installs the neccessary packages and runs the script'''

import package_handler
NAME = 'installer'

def log(msg: str) -> None:
    '''logging function to replace print()'''
    print(f'[{NAME}] {msg}')

packages = ('pynput', 'pyautogui')

log('installing packages')
package_handler.install(packages)
log('done')
log('starting up scriptshot')

# importing this any sooner would've errored due to missing packages
# pylint: disable=C0413
import scriptshot
# pylint: enable=C0413

log('done')
log('running scriptshot')

scriptshot.run()
