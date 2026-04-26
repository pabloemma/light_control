# light control_main ist the main control for the random light at a house
# it will be connected to a push button to turn it on and off
#there will be a list of how many toime windows and when
# which will be controlled thorugh a config json filerurrently there are 6 ikea outlets defined in the config file;
#however I have only 5, #3 does not exist
# A switch is used in the system if it has an action eithe ON or OFF.
#if the action is blank then that switch is not being used.
# There is a start and end time and a window. If the widonw is 0, it means to use the exact start and end time
# if the winodw has a value this is used to set a start time and endtime randomly within that window, if the window is astral, it determines the sunset
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

# my imports
import lc_config as LC
import ikea_class as IKC  
import lc_control as LCO 

# globals



#pyside block
from PySide6.QtWidgets import (QApplication,
                               QFileDialog,
                               QDialog, 
                               QLabel,
                                QMainWindow, 
                                QMenu,
                                QPushButton,
                                QVBoxLayout,
                                QWidget)



class lc_main(QMainWindow):
    def __init__(self,config_file = None):


        super().__init__()

    #setup pyside6
        self.setWindowTitle("Light Control")
        myLabel = QLabel("light control vs 1.0")
        myCloseButton = QPushButton("Close")
        myCloseButton.clicked.connect(self.CloseApp)
        layout= QVBoxLayout()
        layout.addWidget(myLabel)
        layout.addWidget(myCloseButton)


        widget = QWidget()
        widget.setLayout(layout)

 

        self.setCentralWidget(widget)
        self.show()


    # setup system

    # the logger
        self.SetupLogger()

    # the configuration
        self.config_file = config_file

        # default config_file
        if(self.config_file == None) :
            #give default name
  


            try:
                logger.warning("error in configuration, opening dialog")
                self.config_file , filter = QFileDialog.getOpenFileName(self,
                                self.tr("Open Config file"), "~", self.tr("*.json"))
                
                self.myconf = LC.lc_config(config_file = self.config_file)

            except Exception as e:
                logger.error(f"Error loading configuration file: {e}")
                sys.exit(1)
        else:
            self.myconf = LC.lc_config(config_file = self.config_file)



        #initialze astral
        self.SetupAstral()

        #initialize the IKEA class
        self.IKC = IKC.IkeaControl( host = self.myconf.host,username=self.myconf.username)
        #self.IKC.turn_on('ikea_5')
        self.IKC.turn_off('ikea_5')




    def CloseApp(self):
        logger.info("closing down")
        self.close()
     


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
        logger.add('info.log', format = fmt , level = 'INFO',rotation="1 day")


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
        return
    






if __name__ == "__main__":
    app = QApplication([])
    config_file = "/Users/klein/git/light_control/config/light_control.json"
    window = lc_main(config_file = config_file )
    window.show()
    app.exec()           