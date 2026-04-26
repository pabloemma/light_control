# this is the control of the lights on hw level



#regular imports
import os
import sys
import platform
from loguru import logger
import time
import datetime as dt
import astral as AT # to get sunrise and sunset
import control_relay as CR
from astral.sun import sun
import random as RT
# globals

class set_light(object):

    def __init__(self,start_time = None , duration = 30, astral_info = None , random_time = None):
 
        #default is 30 minutes duration
        # the light will be on friom start_time until start_time+ durration
        # the fomrat of the start_time has to be 16:30:00
        # the random_time, if set should be givenm in minutes
        # it will randomize the starttime by this amount
        super().__init__()

        #initializ the relay, there are two relays on the board
        # we initialze them to off
        self.relay = CR.MyRelay(relay_number = 1,state = 0)
 
        # the self.light_on is a toggle switch
        # tme moment the time condition is fulfilled it will be switched to True
        self.light_on = False
        self.astral_info = astral_info

        if random_time != None :
            # set the seed
            RT.seed()
            random_time_new =  RT.random()*random_time
            # using 30 , the start time now variess by the most 30 miniutes
            self.random_time = dt.timedelta(minutes = random_time_new)
        else:
            self.random_time = dt.timedelta(minutes = 0)

        # if astral_info is not None, we use sunset and sunrise
        # else we use start_time

        if(astral_info == None):


            self.duration = dt.timedelta(minutes = duration)
            #this creates a datetime.datetime obj
            self.start_time = dt.datetime.strptime(start_time, "%H:%M:%S")+ self.random_time
            self.end_time = self.start_time+self.duration
 
            #self.start_time.time() is then a datetime.time 

        else:
        #set up the system for sunrise and sunset
            self.setup_astral()
            self.duration = dt.timedelta(minutes = duration)
            self.start_time = dt.datetime.strptime(self.my_sunset, "%H:%M:%S")+self.raandom_time
            self.end_time = self.start_time+self.duration

    
    def run_loop(self,loop_time = 1):
        # here we coontinually loop over time
        # loop_time is how often in units of minutes
        while True:
            self.check_time()
            time.sleep(loop_time*60)

    def setup_astral(self):
        '''uses dictionary to fill astral location info'''

        myl = AT.LocationInfo()
        myl.name        = self.astral_info['name']
        myl.region      = self.astral_info['region']
        myl.timezone    = self.astral_info['timezone']
        myl.latitude    = self.astral_info['latitude']
        myl.longitude   = self.astral_info['longitude']
    
        self.myl        = myl

        self.Get_Sun()
        return 
    
    def Get_Sun(self):
        s_tmp = sun(self.myl.observer,date=dt.datetime.today(),tzinfo=self.myl.timezone)
        self.my_sunrise     = s_tmp['sunrise'].strftime('%H:%M:%S')
        self.my_sunset      = s_tmp['sunset'].strftime('%H:%M:%S')
        return
    



    def check_time(self):

        now = dt.datetime.now()
        current_time = now.time()

        if(current_time > self.start_time.time() and current_time <= self.end_time.time()):
            self.light_on = True
            self.relay.SetRelayOn()
            print(" we have success")

        else: # we only do something if lights are on
            if(self.light_on):
                self.light_on = False
                self.relay.SetRelayOff()
 
      

    def turn_off_light(self):

        print("we turn off the light")
        return

if __name__ == "__main__":
    set_my_time = "15:40:00"
    # info for astral to get sunrise and sunset
    astral_info={'name':'Basel','region':'Switzerland','timezone':'Europe/Paris', \
                 'latitude':47.55224, \
                 'longitude':7.62016 }

    # use suunrise or sunset duration 30 minutess
    #SL = set_light(astral_info = astral_info)
    #SL = set_light(astral_info = astral_info, duration = 60)

    # use start time, duration is 15 minutes
    SL = set_light(start_time = set_my_time)
    # use start time, duration is 60 minutes

    #SL = set_light(start_time = set_my_time, duration =60)
    SL.run_loop()

