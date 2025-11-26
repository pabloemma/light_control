# light control_main ist the main control for the random light at a house
# it will be connected to a push button to turn it on and off
#there will be a list of how many toime windows and when
# which will be controlled thorugh a config json filer

#regular imports
import os
import sys
import platform
from loguru import logger
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



class lc_main(object):
    def __init__(self,config_file = None):




        self.config_file = config_file

        # default config_file
        if(self.config_file == None or not os.path.isfile(self.config_file)):
            #give default name
            self.config_file = self.GetRootDir()+'lm_control.json'
 
            try:
                # get configuration
                self.SetupConfig
            except:
                logger.error("error in configuration, exit now")
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
            





if __name__ == "__main__":
    app = QApplication([])
    config_file = None
    window = lc_main(config_file = config_file )
    window.show()
    app.exec()           