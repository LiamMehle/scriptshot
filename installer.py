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

import scriptshot

scriptshot.run()