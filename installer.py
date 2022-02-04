'''installs the neccessary packages and runs the script'''

import subprocess
import sys
from threading import Thread

def install(package):
    '''installs the package'''
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

packages = ('pynput', 'pyautogui')

threads = [Thread(target=install, args=(package,)) for package in packages]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

# importing this any sooner would've errored due to missing packages
# pylint: disable=C0413
import scriptshot
# pylint: enable=C0413

scriptshot.run()
