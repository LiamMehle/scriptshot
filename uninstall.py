import subprocess
import sys
from threading import Thread

def uninstall(package):
    '''uninstalls the package'''
    subprocess.check_call([sys.executable, '-m', 'pip', 'remove', package])

packages = ('pynput', 'pyautogui')

threads = [Thread(target=install, args=(package,)) for package in packages]
for thread in threads:
    thread.start()

import os

for thread in threads:
    thread.join()

# delete all files
for file in os.listdir('.'):
    os.remove(file)
# delete the folder
os.rmdir('.')
