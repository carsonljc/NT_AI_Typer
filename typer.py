import time
import numpy as np
import decode
import re
from pyautogui import press

DEBUG = False

class Typer:
    def __init__(self, wpm):
        self.wpm = wpm

    # bug: group is not always guarenteed to exist
    def extract_text(self, message, decoder):
        self.stream = re.search(r'"stream":"(\w+)",', message).group(1)
        self.msg = re.search(r'"msg":"(\w+)",', message).group(1)
        self.payload = re.search(r'"payload":{(.+)}', message).group(1)
        self.status = re.search(r'"status":"(\w+)",',self.payload).group(1)

        self.line = re.search(r'"l":"(.+)"',self.payload).group(1)
        self.line = decoder.original(self.line)

        print(self.stream, " : ", self.msg, " : ", self.status, " : ", self.line)



#4{"stream":"race","msg":"status","payload":{"nitros":3,"status":"countdown","l":"D2 94FD [D6EFAD:5 C@32= @E 6?F>>: E@? D: ==:ED {u} 69E [D6E2E$ 56E:?& 69E ?: D6F826= DEC@AD =2?@:DD67@CA C@;2> C69E@ 69E D2 J=E?6FB6C7 D2 E@? 98F@9E=p"}}
def master():
    type_bot = Typer(30)
    decoder = decode.Decoder(obfuscated="2", original="a")


    if DEBUG:
        message = """#4{"stream":"race","msg":"status","payload":{"nitros":3,"status":"countdown","l":"D2 94FD [D6EFAD:5 C@32= @E 6?F>>: E@? D: ==:ED {u} 69E [D6E2E$ 56E:?& 69E ?: D6F826= DEC@AD =2?@:DD67@CA C@;2> C69E@ 69E D2 J=E?6FB6C7 D2 E@? 98F@9E=p"}}"""
    else:
        message = input ("Enter message: ")
    type_bot.extract_text(message, decoder)
    
    time.sleep(3)
    for character in type_bot.line:
        press(character)
        time.sleep(0.3)


if __name__ == '__main__':
    master()