# this is a class to use the paho library for my ikea control system. I will use this class to create an 
# instance of the MQTT client and use it to publish messages to the MQTT broker.

import paho.mqtt.client as mqtt #import the client
from loguru import logger
import os
import sys
import platform
import json



#My imports, I am using the config mechanism from lc_main_nogui
import lc_config as LC

class IkeaPahoClient(mqtt.Client):
    def __init__(self,config_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.SetupLogger()

        self.config_file = config_file
        if(self.config_file == None or not os.path.exists(self.config_file)):
            #give default name
            logger.error(f"Error loading configuration file: ,selected file {self.config_file} does not exist ")
            sys.exit(1)
 



        else:
            try:
                self.myconf = LC.lc_config(config_file = self.config_file)
            except Exception as e:
                logger.error(f"Error loading configuration file: {e}")
                sys.exit(1)


 
        #Get configuration for the MQTT client from the config file
        self.PWfile = self.myconf.PWfile

        # get password from file
        if platform.system() == 'Darwin':
            f = open("/Users/klein/git/light_control/config/light.txt")
        elif platform.system() == 'Linux':
            f = open("/home/klein/git/light_control/config/light.txt")

        self.password = f.read().strip()  
        f.close()  

 
        self.user_name = self.myconf.username
        self.password = self.password
        self.host = self.myconf.host
        self.port = 1883  


 
        #initialize the MQTT client and set the on_connect and on_message callbacks
        MQC = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # now we connect to the broker

        #Set username and password

        MQC.username_pw_set(self.user_name, self.password)
        MQC.connect(self.host, self.port, 60)



        MQC.on_connect = self.on_connect
        MQC.on_message = self.on_message
        MQC.on_publish = self.on_publish



    def SetupLogger(self):
        logger.remove(0)
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green>    {function}   {line}    {level}     <level>{message}</level>" ,
                level = "DEBUG")



        fmt =  "{time} - {name}-   {function} -{line}- {level}    - {message}"
        if platform.system() == 'Darwin':

            logger.add('/Users/klein/git/light_control/info.log', format = fmt , level = 'INFO',rotation="1 day")
        else:
            logger.add('/home/klein/git/light_control/info.log', format = fmt , level = 'INFO',rotation="1 day")


        # set the colors of the different levels
        logger.level("INFO",color ='<black>')
        logger.level("WARNING",color='<green>')
        logger.level("ERROR",color='<red>')
        logger.level("DEBUG",color = '<blue>')
 
        return



if __name__ == "__main__":

    conf = 'light_control.json'


    if platform.system() == 'Darwin':
        config_file = '/Users/klein/git/light_control/config/'+conf
    elif platform.system() == 'Linux':
        config_file = '/home/klein/git/light_control/config/'+ conf
    else:
        print(' This os is not supported %s' % platform.system())
        sys.exit(1) 


    client = IkeaPahoClient(config_file=config_file)
    
                   

        