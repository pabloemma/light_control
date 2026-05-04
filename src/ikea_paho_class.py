# this is a class to use the paho library for my ikea control system. I will use this class to create an 
# instance of the MQTT client and use it to publish messages to the MQTT broker.

import paho.mqtt.client as mqtt #import the client
from loguru import logger
import os
import sys
import platform
import json
import time
import random as RND


#My imports, I am using the config mechanism from lc_main_nogui
import lc_config as LC

class IkeaPahoClient:
    def __init__(self,config_file=None):
        #super().__init__(*args, **kwargs)


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
        else:
            logger.error(f"Unsupported operating system: {platform.system()}")
            sys.exit(1) 

        
        pw = f.read().strip()  
        f.close()  

 
        uname = self.myconf.username
        
        host = self.myconf.host
        port = 1883  

        #Create unit id with random number to avoid conflicts with other clients

        client_id = "ikea_paho_client"+str(RND.randint(0,1000))
 
        #initialize the MQTT client and set the on_connect and on_message callbacks
        self.MQC=MQC = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

        # now we connect to the broker

        #Set username and password

        MQC.username_pw_set(uname, pw)
        #MQC.connect(host, port, 60)
        #MQC.publish("zigbee2mqtt/ikea_5/set", "OFF")
        #self.mysubscribe("zigbee2mqtt/ikea_5/set")
        #self.mypublish("zigbee2mqtt/ikea_5/set", "OFF")


        MQC.on_connect = self.on_connect
        MQC.on_message = self.on_message
        #MQC.on_publish = self.on_publish
        MQC.on_subscribe = self.on_subscribe   
        # 
        self.MQC.connected_flag = False 



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

    def on_connect( self,client, userdata, flags, rc,properties):
        if rc == 0:
            self.MQC.connected_flag = True
            logger.info(f"Connected with result code {rc}") 
        else:
            logger.error(f"Failed to connect, return code {rc}")
        return

    def on_message( self,client, userdata, msg):
        logger.info(f"Received message on topic {msg.topic} with payload {msg.payload}") 
        a=str(msg.payload.decode("utf-8"))
        print(f"Decoded message: {a}")
        return  
    
    def on_publish(self,client, userdata, mid, reason_code, properties):
        # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3

        try:
            userdata.remove(mid)
        except KeyError:
            logger.warning("on_publish() is called with a mid not present in unacked_publish")
        
    def mypublish(self, topic, payload, qos=0, retain=False):
        msg_info = self.MQC.publish(topic, payload, qos, retain)
        print(f"Published message to topic {topic} with payload {payload}, mid: {msg_info.mid}, result: {msg_info.rc}")
        #let's make sure it gets published before we return
        msg_info.wait_for_publish()
        print(msg_info.is_published()) 
        return msg_info
    
    def mysubscribe(self, topic, qos=0):
        result, mid = self.MQC.subscribe(topic, qos)
        return result, mid

    def on_subscribe(self,client, userdata, mid, reason_code_list, properties):
        # Since we subscribed only for a single channel, reason_code_list contains only one item.
        logger.info(f"Subscribed with mid {mid}, reason code {reason_code_list[0]}")
        return

    def start(self):
        self.MQC.loop_start()

        self.MQC.connect(self.myconf.host, 1883, 60)
        while not self.MQC.connected_flag:
            logger.info("Waiting for connection...")
            time.sleep(1)
        return

    def stop(self):
        self.MQC.loop_stop()
        self.MQC.disconnect()

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
    client.start() #start the loop
    # first we subscribe to the topic we want to listen to, in this case we want to listen to the topic that the ikea outlet is publishing to, which is zigbee2mqtt/ikea_5/set
    client.mysubscribe("zigbee2mqtt/ikea_2/set")
    #client.mysubscribe("zigbee2mqtt/ikea_2")
    # now publish something to the broker
    client.mypublish("zigbee2mqtt/ikea_2/set", "OFF")   
    #client.mypublish("zigbee2mqtt/ikea_2", payload=None)   # this retunrs the state of the ikea_2
    time.sleep(20)
    #client.mypublish("zigbee2mqtt/ikea_4/set", "OFF")   
 
    client.stop()
                   

        