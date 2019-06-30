import pychrome

def Listener():
    
    # start chrome --remote-debugging-port=9222
    def __init__(self, url="http://127.0.0.1:9222"):
        self.browser = pychrome.Browser(url=url)
        self.tab = self.browser.new_tab()
        self.tab.set_listener("Network.requestWillBeSent", self.request_will_be_sent)
        self.tab.set_listener("Network.webSocketFrameReceived", self.web_socket_created)

    def start(self):
        self.tab.start()
        self.tab.call_method("Network.enable")
        self.tab.Page.navigate(url="https://www.nitrotype.com/race", _timeout=5)

    @staticmethod
    def request_will_be_sent(**kwargs):
        print("loading: %s" % kwargs.get('request').get('url'))

    @staticmethod
    def web_socket_created(**kwargs):
        print("entered")
        print(kwargs.get('response').get('payloadData'))
