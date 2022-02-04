'''
    a small script that takes a configurable number of screenshots on and after left click
'''

import time
import os
import asyncio as asio
from threading import Thread
import datetime
import pyautogui as pyg
from pynput.mouse import Listener, Button

# ----------------------------------------------<[ CONFIG ]>-----------------------------------------------

USERNAME       =  '<name goes here>' # your username, used only for determining `SCREENSHOT_DIR`
SCREENSHOT_DIR = f'C:\\Users\\{USERNAME}\\Pictures\\scriptshots' # [sic] output directory
DEFAULT_BURST_DELAY = 1.0                                        # delay between screenshots
DEFAULT_BURST_SIZE  = 4                                          # number of screenshots after trigger

STEAM_SCREENSHOT        = False
STEAM_SCREENSHOT_HOTKEY = 'f12'

# ---------------------------------------------------------------------------------------------------------

NAME = 'scriptshot'

def log(msg: str) -> None:
    '''logging function to replace print()'''
    print(f'[{NAME}] {msg}')

class Screenshotter:
    '''class for re-use purpose'''

    @staticmethod
    def enumerate_dir(directory: str):
        '''enumerates directory or crates it if it doesn't exist'''
        try:
            filenames = os.listdir(directory)
        except FileNotFoundError:
            os.mkdir(directory)
            filenames = os.listdir(directory)
        return filenames

    def __init__(self) -> None:
        '''(default-) init (class variables)'''
        self.username       =  USERNAME
        self.screenshot_dir = SCREENSHOT_DIR
        #SCREENSHOT_DIR = f'/home/wolf/git/personal/scriptshot' # not misspelled
        self.default_burst_delay = DEFAULT_BURST_DELAY
        self.default_burst_delay = DEFAULT_BURST_SIZE

        self.get_default_delay_set = lambda: [DEFAULT_BURST_DELAY]*max(DEFAULT_BURST_SIZE-1, 0)

    @staticmethod
    def filename_to_indicies(filename: str) -> (int, int):
        '''extracts the indicies from a filename with correct format, returns None upon failiure'''
        try:
            intermediate = filename.split('-')
            indicies     = (intermediate[0], intermediate[1].split('.')[0])
            indicies     = [int(index) for index in indicies]
            return tuple(indicies)
        except IndexError:
            return None
        except ValueError:
            return None


    def get_max_collection_number(self) -> int:
        '''returns last collection number or -1 if none exist.'''
        filenames    = self.enumerate_dir(self.screenshot_dir)
        file_numbers = (self.filename_to_indicies(file) for file in filenames)
        # filter out invalids
        file_numbers = (number[0] for number in file_numbers if number is not None)
        try:
            return max(file_numbers)
        except ValueError:
            return -1

    def get_max_in_collection_number(self, number: int) -> int:
        '''returns last number in collection or -1 if none exist.'''
        filenames    = self.enumerate_dir(self.screenshot_dir)
        file_numbers = (self.filename_to_indicies(file) for file in filenames)
        # filter out invalids
        file_numbers = (index[1] for index in file_numbers if index is not None
                                                          and int(index[0]) == number)
        try:
            return max(file_numbers)
        except ValueError:
            return -1


    def save_screenshot(self, screenshot, collection_number: int) -> None:
        '''handles screenshot saving with correct name and path'''
        index = self.get_max_in_collection_number(collection_number)+1
        screenshot.save(os.path.join(self.screenshot_dir, f'{collection_number}-{index}.jpeg'))

    async def scs_burst(self, delay_set: [float] = None) -> None:
        '''takes a configurable "burst" of screenshots'''
        if delay_set is None:
            delay_set = self.get_default_delay_set()
        delay_set         = [0, *delay_set]
        collection_number = self.get_max_collection_number() + 1
        threads           = []
        for delay in delay_set:
            asio.sleep(delay)
            if STEAM_SCREENSHOT:
                pyg.hotkey(STEAM_SCREENSHOT_HOTKEY)
            else:
                screenshot = pyg.screenshot()
                threads.append(asio.to_thread(self.save_screenshot, screenshot, collection_number))

        for thr in threads:
            await thr


    # ----------------------------------------------------------------------
    triggered = False
    terminate = False

    # ----------------------------------------------------------------------

    async def main(self):
        '''main, top-level function'''
        def on_click(xpos: int, ypos: int, button, pressed):
            '''on mouse click'''
            if xpos < 0 or ypos < 0:
                return

            if button == Button.left and pressed is True:
                self.triggered = True

        (terminator_thread := Thread(target=self.terminator)).start()
        asio.Task(self.screenshotter())

        with Listener(on_click=on_click) as listener:
            while not self.terminate:
                await asio.sleep(.25)
            listener.stop()

        terminator_thread.join()

    async def screenshotter(self):
        '''
            handles the screenshotting outside of a dedicated signal handler
            think of this as a "worker coroutine". Sleeping inside the signal
            hanlder causes untold lag even even if all cpu cores are idling.
        '''
        while not self.terminate:
            await asio.sleep(.25)
            if self.triggered:
                # intended behaveour: if triggered mid-burst, continue with another burst
                self.triggered = False
                currenttime = datetime.datetime.now().strftime('%a %H:%M:%S')
                log(f'taking screenshot burst at {currenttime}')
                await self.scs_burst()

    def terminator(self):
        '''listens for input and signals end of program when newline detected'''
        input()
        self.terminate = True

    def run(self):
        '''user-friendly wrapper'''
        asio.run(self.main())

def run():
    '''starts up the script.'''
    log('running')
    Screenshotter().run()

if __name__ == '__main__':
    run()
