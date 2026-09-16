# This file is part of ChemPy.
# Copyright (C) 2026 Chem
#
# ChemPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ChemPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ChemPy. If not, see <http://www.gnu.org/licenses/>.

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
