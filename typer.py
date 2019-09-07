import time
import re
import random
import numpy as np
from pyautogui import press
from modules.decode import Decoder
from modules.chrome_listener import Listener

DEBUG = False

class Typer(Listener, Decoder):
    def __init__(self, wpm, url="http://127.0.0.1:9222", obfuscated="2", original="a"):
        self.wpm = wpm
        self.loc = 60/(wpm*6) # wpm is converted to seconds/character - assuming average word length of 6
        self.state = "end"
        Decoder.__init__(self, obfuscated=obfuscated, original=original,)
        Listener.__init__(self, url=url, _web_socket_created=self.web_socket_created)

    def web_socket_created(self, **kwargs):
        # when a message is detected from a web socket, process the data
        message = kwargs.get('response').get('payloadData')
        self.extract_text(message)

    def extract_text(self, message):
        # given the message of a web socket, extract data and payload
        if DEBUG: print(message)

        # messages that start with 3 can be directly ignored
        if message[0] is "4":
            # if there is no stream, then it doesn't contain information we care about
            if re.search(r'"stream":"(\w+)",', message) is not None:
                self.stream = re.search(r'"stream":"(\w+)",', message).group(1)
                self.msg = re.search(r'"msg":"(\w+)",', message).group(1)
                if re.search(r'"payload":{(.+)}', message) is not None:
                    self.payload = re.search(r'"payload":{(.+)}', message).group(1)

                    # status may not always exist in payload
                    try:
                        self.status = re.search(r'"status":"(\w+)",', self.payload).group(1)
                    except:
                        self.status = None

                    # condition for getting typing text
                    if re.search(r'"l":"(.+)"', self.payload) is not None:
                        self.line = re.search(r'"l":"(.+)"', self.payload).group(1)
                        self.text = self.original(self.line)
                        self.state = "ready"
                    # condition for detetion the start of the race
                    elif re.search(r'"startStamp":(.+),', self.payload) is not None:
                        self.line = re.search(r'"startStamp":(.+),', self.payload).group(1)
                        self.state = "start"
                    # condition for detecting end of a race
                    elif re.search(r'"r":{(.+)}', self.payload) is not None:
                        self.line = re.search(r'"r":{(.+)}', self.payload).group(1)
                        self.state = "end"
                    else:
                        self.line = None

                    if DEBUG: print(self.stream, " : ", self.msg, " : ", self.status, " : ", self.line)


def master():
    # main program to run the algorithms for the typing AI
    type_bot = Typer(wpm=60)
    type_bot.start() # starts the browsers
    num_races = 0
    accuracy = 98

    def race():
        loc = abs(np.random.normal(loc=type_bot.loc, scale=0.01))

        for character in type_bot.text:
            amount_to_wait = abs(np.random.normal(loc=loc,scale=0.01))

            if DEBUG: 
                print(amount_to_wait, ":", character)
            # creating a random chance to make mistake
            if random.randint(0,100) > accuracy:
                press(chr(ord(character)+random.randint(-1,1)))
                time.sleep(amount_to_wait/3) # slightly less time to wait if we make a mistake

            press(character)
            time.sleep(amount_to_wait) 

    # wait commands can be combined
    def wait_for_text():
        if DEBUG: print("READY")
        while type_bot.state is not "ready":
            pass
    
    def wait_for_start():
        if DEBUG: print("START")
        while type_bot.state is not "start":
            pass

    def wait_for_end():
        if DEBUG: print("END")
        while type_bot.state is not "end":
            pass

    while True:
        wait_for_text()
        wait_for_start()
        race()
        wait_for_end()
        time.sleep(3)
        press('enter') # this starts a new race
        if DEBUG: print("RESETTING")
        num_races += 1
        print(num_races)

if __name__ == '__main__':
    master()