# light control_main ist the main control for the random light at a house
# it will be connected to a push button to turn it on and off
#there will be a list of how many toime windows and when
# which will be controlled thorugh a config json filerurrently there are 6 ikea outlets defined in the config file;
#however I have only 5, #3 does not exist
# A switch is used in the system if it has an action eithe ON or OFF.
#if the action is blank then that switch is not being used.
# There is a start and end time and a window. If the widonw is 0, it means to use the exact start and end time
# if the winodw has a value this is used to set a start time and endtime randomly within that window, if the window is -1, it determines the sunset
#for the location and then uses this as the start time and then the end time is determined by the window.
# So the window can either be for randomness or length of action .
# The window is used to make the light more random and less predictable.
# as an example: starttime = 18:00, window :60 will mean that the start time will be somewhere between 17:30 and 18:30 and the same for the
# end time. This is to make the light more random and less predictable.
# the loop time is in munutes and is used to determine how often the system checks the time and the actions. The system will check every loop time if any of the actions need to be performed.
# NOTE: Currently the system has only two actions either OFF or ON. The beavior is that the action selected is valid for the chosen time windwo.
#
# The system controls throgh zigbee2mqtt and mosquitto_pub, the ikea outlets. The system is designed to be run on a raspberry pi, 
# but it can be run on any system that has python and the required libraries installed. However it communicates with a MQTT dongle, in my case
# connected to a raspberry pi 4 which is running home assistant
# the system is designed to be run as a service on the raspberry pi, but it can also be run as a standalone application.
# In the json file you select which sensor is active in the active senor list

#regular imports
import os
import sys
import platform
from loguru import logger
import astral as AT
from astral.sun import sun
import datetime as dt
import random as RT
import time

# my imports
import lc_config as LC
import ikea_class as IKC  
import lc_control as LCO 

# globals



#pyside block

class lc_main(object):
    def __init__(self,config_file = None):


        super().__init__()

  

    # setup system

    # the logger
        self.SetupLogger()

    # the configuration
        self.config_file = config_file

        # default config_file
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

        #initialze astral
        self.SetupAstral()

        #initialize the IKEA class
        self.IKC = IKC.IkeaControl( host = self.myconf.host,username=self.myconf.username)
        #self.IKC.turn_on('ikea_5')
        #self.IKC.turn_off('ikea_5')

        self.device_on = {device: False for device in self.myconf.active_sensors}



        # here we start
        self.RunLoop()


    def CloseApp(self):
        logger.info("closing down")
        self.close()
        sys.exit()
     


    def GetRootDir(self):
        """determines the root directory of the lc_main, depending on the OS"""
        #determine the platform, Darwin for OS
 
 
        if platform.system() == 'Darwin':
            return '/Users/'+os.getlogin()+'/git/light_control/'
        elif platform.system() == 'Linux': 
            return '/home/'+os.getlogin()+'/git/light_control/'
        else:
            logger.error("OS not supported")
            sys.exit()
            

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

    def SetupAstral(self):
        myl = AT.LocationInfo()
        myl.name        = self.myconf.astral_name
        myl.region      = self.myconf.astral_region
        myl.timezone    = self.myconf.astral_timezone
        myl.latitude    = self.myconf.astral_latitude
        myl.longitude   = self.myconf.astral_longitude
    
        self.myl        = myl

        self.Get_Sun()
        return 
    
    def Get_Sun(self):
        s_tmp = sun(self.myl.observer,date=dt.datetime.today(),tzinfo=self.myl.timezone)
        self.my_sunrise     = s_tmp['sunrise'].strftime('%H:%M:%S')
        self.my_sunset      = s_tmp['sunset'].strftime('%H:%M:%S')
        print(f"\n\n*************************************************************\n\n")
        print(f"sunrise is at {self.my_sunrise} and sunset is at {self.my_sunset}")
        print(f"\n\n*************************************************************\n\n") 
        
        return
    

    def RunLoop(self):
        # first we turn all the sensors off and initailze the device properties in a dictionary for easy access later
        self.device_properties = {}
        for device in self.myconf.active_sensors:
            self.IKC.turn_off(device)
            self.device_on[device] = False
            self.device_properties[device]= {"start_time": getattr(self.myconf, f"{device}_start"),
                                        "end_time": getattr(self.myconf, f"{device}_end"),
                                        "window": getattr(self.myconf, f"{device}_window"),
                                        "action": getattr(self.myconf, f"{device}_action")}
        self.SetupDevices()

            

       # here we continually loop over time
        # loop_time is how often in units of minutes
        while True:
            # iterate over all the acive devices
            #  
            for device in self.myconf.active_sensors:
                    # check the time for each device
                    self.check_time(device)

            time.sleep(self.myconf.loop_time*60)
            #time.sleep(1)
        return

    def SetupDevices(self):  
        # here we calculate the times for each device and store them in a dictionary for easy access later   
        #    
        for device in self.myconf.active_sensors:
            start_time =self.device_properties[device]["start_time"]
            end_time = self.device_properties[device]["end_time"]
            mywindow = self.device_properties[device]["window"]
            action = self.device_properties[device]["action"]

            # if the action is blank, we do not use this device
            if action == "":
                return

        # if the window is not 0, we use it to set a random start and end time
            if mywindow > 0:
                random_time_new_start = RT.uniform(-mywindow/120., mywindow/120.) # get back to minutes
                random_time_new_end = RT.uniform(-mywindow/120., mywindow/120)
            elif mywindow == -1:
                random_time_new_start = RT.uniform(-20./2, 20./2)  # with sunset we also ransomize but a smaller window
                random_time_new_end = RT.uniform(-20./2, 20./2)
                start_time = self.my_sunset
            else:
                random_time_new_start = 0
                random_time_new_end = 0

            start_time = dt.datetime.strptime(start_time, "%H:%M:%S") + dt.timedelta(minutes = random_time_new_start)
        
            end_time = dt.datetime.strptime(end_time, "%H:%M:%S")+ dt.timedelta(minutes = random_time_new_end)
            # put the new values back into the dictionary
            print(start_time.strftime('%H:%M:%S'),end_time.strftime('%H:%M:%S'))
            self.device_properties[device]["start_time"] = start_time
            self.device_properties[device]["end_time"] = end_time

        return


    def check_device(self,device):
        # this checks the time for a given device and performs the action if the time is within the window
        # we get the start time, end time, window and action for the device from the config file
        start_time = getattr(self.myconf, f"{device}_start")
        end_time = getattr(self.myconf, f"{device}_end")
        mywindow = getattr(self.myconf, f"{device}_window")
        action = getattr(self.myconf, f"{device}_action")

        print(device,start_time)


        # if the action is blank, we do not use this device
        if action == "":
            return

        # if the window is not 0, we use it to set a random start and end time
        if mywindow > 0:
            random_time_new_start = RT.uniform(-mywindow/2, mywindow/2)
            random_time_new_end = RT.uniform(-mywindow/2, mywindow/2)
        elif mywindow == -1:
            random_time_new_start = RT.uniform(-20/2, 20/2)  # with sunset we also ransomize but a smaller window
            random_time_new_end = RT.uniform(-20/2, 20/2)
            start_time = self.my_sunset
        else:
            random_time_new_start = 0
            random_time_new_end = 0

        self.start_time = dt.datetime.strptime(start_time, "%H:%M:%S") #+ dt.timedelta(minutes = random_time_new_start)
        self.end_time = dt.datetime.strptime(end_time, "%H:%M:%S")#+ dt.timedelta(minutes = random_time_new_end)

 
        print(device)
        self.check_time(device)
        return

    #def check_time(self,device):
    def check_time(self,device):

        now = dt.datetime.now()
        current_time = now.time()


        if(self.device_properties[device]["start_time"].time() > self.device_properties[device]["end_time"].time()):
            # we are going over midnight, so need to correct this
            # we run anyway until we go thorugh midnight and then we move over to end_time
            if current_time > self.device_properties[device]["start_time"].time() or current_time <= self.device_properties[device]["end_time"].time():
                if(self.device_on[device] == False):
                    self.IKC.turn_on(device)
                    self.device_on[device] = True
                    return
            else: # we are outside the time window, so we turn off the device if it is on
                if(self.device_on[device] == True):
                    self.IKC.turn_off(device)
                    self.device_on[device] = False
                    return
            return
        

         

        if(current_time > self.device_properties[device]["start_time"].time() and current_time <= self.device_properties[device]["end_time"].time()):
            if(self.device_on[device] == False):
                
                self.IKC.turn_on(device)
                self.device_on[device] = True


        else: # we only do something if lights are on
            if(self.device_on[device] == True):
                self.IKC.turn_off(device)
                self.device_on[device] = False
        return

if __name__ == "__main__":
    #conf = 'lc_debug.json'
    conf = 'light_control.json'


    if platform.system() == 'Darwin':
        config_file = '/Users/klein/git/light_control/config/'+conf
    elif platform.system() == 'Linux':
        config_file = '/home/klein/git/light_control/config/'+ conf
    else:
        print(' This os is not supported %s' % platform.system())
        sys.exit(1) 
    
    lc_main(config_file = config_file)