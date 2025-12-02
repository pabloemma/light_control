"""Class to configure the test_speed program
Using json (sigh); look al;so at
https://www.quora.com/How-do-I-loop-through-a-JSON-file-with-multiple-keys-sub-keys-in-Python"""


import json
import os
import sys
import platform
import socket
import inspect

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class MyConfig():

    def __init__(self,config_file):
        """ config_file contains all the infor for light_control program"""

 
       
        
        # Open config file
        #print('Directory Name:     ', os.path.dirname(config_file))
       

        if os.path.exists(config_file) :
            self.ReadJsonNew(config_file)
        else:
            print(" Config file does not exist, exiting     ", config_file)
            sys.exit(0)

    def ReadJson(self,file_path):

        print("reading config file ", file_path)    
        with open(file_path, "r") as f:
            myconf = json.load(f)

            self.DecodeVariables(myconf)
    def ReadJsonNew(self,file_path):
        with open(config_file,"r", encoding = "utf-8") as f:
            data = json.load(f)

    # now manipulate data
    # example:
        a = data['Control']
        b = data['logging']
        tc = data['time_control']
        tw = data['time_window']
    # now a is a new dictionary , can loop through its value
    #Control block
        self.debug = a['debug']


    #logging block
        self.log_level = b['log_level']
        self.log_output = b['log_output']

    #timing block
        self.times = []
    #iterate throug the times
        for key in tc:
            self.times.append(tc[key])
        print(self.times)
        self.time_window = []

        for key in tw:
            self.time_window.append(tw[key])
        return






if __name__ == '__main__':
    mysystem = platform.system()

    if mysystem == 'Darwin':
        conf_dir = '/Users/klein/git/light_control/config/'
    elif mysystem == 'Linux':
        conf_dir = '/home/klein/git/light_control/config/'
    else:
        print(' This os is not supported %s' % mysystem)
    config_file = conf_dir + 'lc_control.json'
    MyC = MyConfig(config_file)
