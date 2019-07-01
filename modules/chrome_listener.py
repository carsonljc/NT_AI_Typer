import pychrome

class Listener():
    # start chrome --remote-debugging-port=9222
    def __init__(self, url="http://127.0.0.1:9222", 
                    _request_will_be_sent=None, 
                    _web_socket_created=None):
        if _web_socket_created is None:
            _web_socket_created = self.web_socket_created
        if _request_will_be_sent is None:
            _request_will_be_sent = self.request_will_be_sent

        self.browser = pychrome.Browser(url=url)
        self.tab = self.browser.new_tab()
        self.tab.set_listener("Network.requestWillBeSent", _request_will_be_sent)
        self.tab.set_listener("Network.webSocketFrameReceived", _web_socket_created)

    def start(self):
        print("Starting tab")
        self.tab.start()
        self.tab.call_method("Network.enable")
        self.tab.Page.navigate(url="https://www.nitrotype.com/race", _timeout=5)

    def request_will_be_sent(self, **kwargs):
        #print("loading: %s" % kwargs.get('request').get('url'))
        pass

    def web_socket_created(self, **kwargs):
        print(kwargs.get('response').get('payloadData'))
