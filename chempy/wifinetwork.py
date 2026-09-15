class WifiNetwork:
    def __init__(self, bssid:str, ssid:str = '', mode:str = '', chan:str = '', rate:str = '', signal:str = '', security:str = '', password:str = ''):
        self.bssid = bssid
        self.ssid = ssid
        self.mode = mode
        self.chan = chan
        self.rate = rate
        self.signal = signal
        self.security = security
        self.password = password
    def __str__(self):
        return f"{'{'}'bssid': {self.bssid}, 'ssid': {self.ssid}, 'mode': {self.mode}, 'chan': {self.chan}, 'rate': {self.rate}, 'signal': {self.signal}, 'security': {self.security}, 'password': {self.password}{'}'}"
