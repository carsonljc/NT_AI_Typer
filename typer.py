import time
import numpy as np
from decode import Decoder
import re
from chrome_extractor import Listener
from pyautogui import press

DEBUG = False

class Typer(Listener, Decoder):
    def __init__(self, wpm, url="http://127.0.0.1:9222", obfuscated="2", original="a"):
        self.wpm = wpm
        self.state = "end"
        Decoder.__init__(self, obfuscated=obfuscated, original=original,)
        Listener.__init__(self, url=url, _web_socket_created=self.web_socket_created)

    def web_socket_created(self, **kwargs):
        message = kwargs.get('response').get('payloadData')
        self.extract_text(message)

    # bug: group is not always guarenteed to exist
    def extract_text(self, message):

        if DEBUG: print(message)

        if message[0] is "4":
            self.stream = re.search(r'"stream":"(\w+)",', message).group(1)
            self.msg = re.search(r'"msg":"(\w+)",', message).group(1)
            self.payload = re.search(r'"payload":{(.+)}', message).group(1)

            try:
                self.status = re.search(r'"status":"(\w+)",', self.payload).group(1)
            except:
                self.status = None

            if re.search(r'"l":"(.+)"', self.payload) is not None:
                self.line = re.search(r'"l":"(.+)"', self.payload)
                self.line = self.line.group(1)
                self.text = self.original(self.line)
                self.state = "ready"
            elif re.search(r'"startStamp":(.+),', self.payload) is not None:
                self.line = re.search(r'"startStamp":(.+),', self.payload)
                self.line = self.line.group(1)
                self.state = "start"
            elif re.search(r'"r":{(.+)}', self.payload) is not None:
                self.line = re.search(r'"r":{(.+)}', self.payload)
                self.line = self.line.group(1)
                self.state = "end"
            else:
                self.line = None

            if DEBUG: print(self.stream, " : ", self.msg, " : ", self.status, " : ", self.line)

#4{"stream":"race","msg":"update","payload":{"racers":[{"t":302,"c":1561936808890,"r":{"experience":0,"nitros":0,"money":0,"bonuses":{}},"u":"g0.496745166703221"}],"secs":53879}}

#4{"stream":"race","msg":"status","payload":{"nitros":3,"status":"countdown","l":"D2 94FD [D6EFAD:5 C@32= @E 6?F>>: E@? D: ==:ED {u} 69E [D6E2E$ 56E:?& 69E ?: D6F826= DEC@AD =2?@:DD67@CA C@;2> C69E@ 69E D2 J=E?6FB6C7 D2 E@? 98F@9E=p"}}
def master():
    type_bot = Typer(wpm=30)
    type_bot.start()
    num_races = 0

    def race():
        loc = np.random.normal(loc=0.171, scale=0.05)

        for character in type_bot.text:
            if DEBUG: print(character)
            press(character)
            amount_to_wait = np.random.normal(loc=loc,scale=0.01)
            if DEBUG: print(amount_to_wait)
            time.sleep(amount_to_wait) 

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
        press('enter')
        if DEBUG: print("RESETTING")
        num_races += 1
        print(num_races)

if __name__ == '__main__':
    master()