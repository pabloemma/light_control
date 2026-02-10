import usbrelay_py
import subprocess #for cli fucntin
import argparse
class MyRelay(object):

    def __init__(self,relay_number = 1,state = None):

        #this initializes the usb relay
        #  The relay_number is the number of the relay you wasnt to control
        # But note : its starts counting from 1 and NOT 0

        self.debug = False


    

    #setup relay board

        self.relay_number = relay_number
        count = usbrelay_py.board_count()
        if(self.debug):
    
            print("Count: ",count)

        self.boards = usbrelay_py.board_details()



        self.GetCLIArgs()


        if(self.debug):
            print("Boards: ",self.boards)
        if(state == 1):
            a = self.SetRelayOn()
            if(self.debug):
                print("at set_relay_on  ",a)
        elif(state==0):
            a = self.SetRelayOff()
            if(self.debug):
                    print("at set_relay_off  ",a)
        elif(state == None):
            if(self.debug):
                    print("at relay = None  ",a)
             
            pass
 
    def GetCLIArgs(self):
        '''Gets command line arguments, the only one allowed are relay number and state
            r: relay_number, s=state'''
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--relay", help = "relay number")
        parser.add_argument("-s", "--state", help = "relay state (1 or 0)")
        # Read arguments from command line
        args = parser.parse_args()
        if(args.relay != None):

            self.relay_number = int(args.relay)
            if(args.state == '1'):
                print('state',args.state)
                self.SetRelayOn()
                exit()
            elif(args.state=='0'):
                print('state',args.state)
                self.SetRelayOff()
                exit()


    def SetRelayOn(self):
        '''This sets the relay to closed
        The relay_number is the number of the relay you wasnt to control
        But note : its starts counting from 1 and NOT 0
        '''

        
        if(self.debug):
            print(self.boards[0][0])
        result = usbrelay_py.board_control(self.boards[0][0],self.relay_number,1)
        return result

    def SetRelayOff(self):
        
        result = usbrelay_py.board_control(self.boards[0][0],self.relay_number,0)
        return result

    def GetRelayState(self):
        '''due to the fact that the python version does 
        not give the state, I have to use the commanline tool'''
        
        result = subprocess.run(['usbrelay'], stdout=subprocess.PIPE)
        s=result.stdout.decode('utf-8')
        # strip the new line
        b= s.replace('\n',',')
        # create a string tuple for this
        a = tuple(map(str,b.split(','))) # this has 3 elemnst since it creates  an elemnt for every comma
        
        # now we loop through the relays and check their state
        #if the find comes bakc negaitve it means the relay is open
        # returns a dictionary wher value 0 means open and 1 means close
        relay_state_dict={}
        for k in range(len(a)-1):
            if(self.debug):
    
                print(a[k])
            if(a[k].find('=1')) < 1 :
                print('relay ',k+1,' is open')
                temp = 'relay '+str(k+1)
                relay_state_dict[temp]=0
            else:
                print('relay ',k+1,' is closed')
                temp = 'relay '+str(k+1)
                relay_state_dict[temp]=1

        if(self.debug):
    
            print (relay_state_dict)
        return relay_state_dict



if __name__ == "__main__":

    MR = MyRelay()
    
    #MR.SetRelayOn()
    #MR.GetRelayState()
    #MR.SetRelayOff()