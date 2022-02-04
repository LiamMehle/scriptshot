'''installs or uninstalls packages'''
import subprocess
import sys
from threading import Thread

def perform_package_actions(verb: str, packages: [str]) -> None:
    '''performs specified action on the listed packages'''
    def package_action(package: str) -> None:
        '''installs the package'''
        assert verb in ('install', 'uninstall')
        subprocess.check_call([sys.executable, '-m', 'pip', verb, package])

    threads = [Thread(target=package_action, args=(pack,)) for pack in packages]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def install(packages: [str]):
    '''installs specified packages'''
    perform_package_actions('install', packages)

def uninstall(packages: [str]):
    '''uninstalls specified packages'''
    perform_package_actions('remove', packages)
