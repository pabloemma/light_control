# class to read light control configuration



import json
import os
import sys
import platform
from loguru import logger

class lc_config(object):

    def __init__(self,config_file = None):

        super().__init__()

        self.config_file = config_file

        # default config_file
        #if(self.config_file == None or not os.path.isfile(self.config_file)):
        if(self.config_file == None ):
            #give default name
            self.config_file = self.GetRootDir()+'../config/light_control.json'
 
            try:
                with open(self.config_file) as f:
                    myconfig = json.load(f)
                    self.DecodeVariables(myconfig)
            except Exception as e:
                logger.error(f"Error loading configuration file: {e}")
                sys.exit(1)
        else:
                with open(self.config_file) as f:
                    myconfig = json.load(f)
 
                    self.DecodeVariables(myconfig)

    def GetRootDir(self):
        return os.path.dirname(os.path.abspath(__file__)) + '/'
    
    def DecodeVariables(self, myconfig):
        # this function decodes the variables from the config file and sets them as attributes of the class
        # it also checks if the variables are valid and if not it gives an error message and exits the program
        try:
            self.name  = myconfig['system']['name']
            self.version  = myconfig['system']['version']
            self.description  = myconfig['system']['description']
            print(f"\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n{self.name} - Version {self.version}\n{self.description}\n\n")
            print(f"\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")

            self.host = myconfig['settings']['host']
            self.PWfile = myconfig['settings']['PWfile']
            self.username = myconfig['settings']['username']
            self.loop_time = myconfig['settings']['loop_time']*60 # convert minutes to seconds

            self.astral_info = myconfig['astral_info']
            self.astral_name = myconfig['astral_info']['name']
            self.astral_region = myconfig['astral_info']['region']
            self.astral_latitude = myconfig['astral_info']['latitude']
            self.astral_longitude = myconfig['astral_info']['longitude']
            self.astral_timezone = myconfig['astral_info']['timezone']

            self.active_sensors = myconfig['mysensors']['active_sensors']

            self.ikea_1_start = myconfig['devices']['sensor_1']['ikea_1']['start_time']
            self.ikea_1_end = myconfig['devices']['sensor_1']['ikea_1']['end_time']
            self.ikea_1_window = myconfig['devices']['sensor_1']['ikea_1']['window']*60    
            self.ikea_1_action = myconfig['devices']['sensor_1']['ikea_1']['action']

            self.ikea_2_start = myconfig['devices']['sensor_2']['ikea_2']['start_time']
            self.ikea_2_end = myconfig['devices']['sensor_2']['ikea_2']['end_time']
            self.ikea_2_window = myconfig['devices']['sensor_2']['ikea_2']['window']*60     
            self.ikea_2_action = myconfig['devices']['sensor_2']['ikea_2']['action']

            self.ikea_3_start = myconfig['devices']['sensor_3']['ikea_3']['start_time']
            self.ikea_3_end = myconfig['devices']['sensor_3']['ikea_3']['end_time']
            self.ikea_3_window = myconfig['devices']['sensor_3']['ikea_3']['window']*60    
            self.ikea_3_action = myconfig['devices']['sensor_3']['ikea_3']['action']

            self.ikea_4_start = myconfig['devices']['sensor_4']['ikea_4']['start_time']
            self.ikea_4_end = myconfig['devices']['sensor_4']['ikea_4']['end_time']
            self.ikea_4_window = myconfig['devices']['sensor_4']['ikea_4']['window']*60    
            self.ikea_4_action = myconfig['devices']['sensor_4']['ikea_4']['action']

            self.ikea_5_start = myconfig['devices']['sensor_5']['ikea_5']['start_time']
            self.ikea_5_end = myconfig['devices']['sensor_5']['ikea_5']['end_time']
            self.ikea_5_window = myconfig['devices']['sensor_5']['ikea_5']['window']*60    
            self.ikea_5_action = myconfig['devices']['sensor_5']['ikea_5']['action']

            self.ikea_6_start = myconfig['devices']['sensor_6']['ikea_6']['start_time']
            self.ikea_6_end = myconfig['devices']['sensor_6']['ikea_6']['end_time']
            self.ikea_6_window = myconfig['devices']['sensor_6']['ikea_6']['window']*60    
            self.ikea_6_action = myconfig['devices']['sensor_6']['ikea_6']['action']

        except KeyError as e:
            logger.error(f"Missing configuration variable: {e}")
            sys.exit(1)


if __name__ == "__main__":
    config = lc_config()
    print(config.name)
    print(config.version)
    print(config.description)
    print(config.host)
    print(config.PWfile)
    print(config.loop_time)
    print(config.ikea_6_window)