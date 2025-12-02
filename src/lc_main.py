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
        if(self.config_file == None or not os.path.isfile(self.config_file)):
            #give default name
            self.config_file = self.GetRootDir()+'config/lc_control.json'
 
            try:
                # get configuration
                self.SetupConfig
            except:
                logger.warning("error in configuration, opening dialog")
                self.config_file , filter = QFileDialog.getOpenFileName(self,
                                self.tr("Open Config file"), "~", self.tr("*.json"))


 
            


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




if __name__ == "__main__":
    app = QApplication([])
    config_file = None
    window = lc_main(config_file = config_file )
    window.show()
    app.exec()           