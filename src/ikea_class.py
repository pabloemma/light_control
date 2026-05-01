# class to tunr the ikea outlest on and off
#very simple code

import platform
import subprocess


class IkeaControl(object):

    def __init__(self, host=None, username=None, password=None):
        self.host = host
        self.username = username
        if password is None:
            if platform.system() == 'Darwin':
                f = open("/Users/klein/git/light_control/config/light.txt")
            elif platform.system() == 'Linux':
                f = open("/home/klein/git/light_control/config/light.txt")

            self.password = f.read().strip()  
            f.close()  
        else:
            self.password = password

    def turn_on(self, device):
        command = f'mosquitto_pub -h {self.host} -t \'zigbee2mqtt/{device}/set\' -m "ON" -d -u \'{self.username}\' -P \'{self.password}\''
        subprocess.Popen(command, shell=True)

    def turn_off(self, device):
        command = f'mosquitto_pub -h {self.host} -t \'zigbee2mqtt/{device}/set\' -m "OFF" -d -u \'{self.username}\' -P \'{self.password}\''
        subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    host = '192.168.3.201'
    username = 'addons'
    IKC = IkeaControl( host = host,username=username)
    IKC.turn_on('ikea_5')
    IKC.turn_off('ikea_5')