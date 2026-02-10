 
# just a stub

def ControlValve(self,valve_state):
        '''this sends a command of either open or close a relay and cosequently
        opens or closes the valve. A relay value of 1 means open heat valve, 0 means close heat valve'''
        if(valve_state == 0):
            #close the valve
            COMMAND = 'python3 /home/pi/git/Thermostat/src/control_relay.py -r 1 -s 0'
            ssh = subprocess.Popen(["ssh", "%s" % self.relay_ip, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
            result = ssh.stdout.readlines()
            if result == []:
                error = ssh.stderr.readlines()
                print("close valve",error)
                sys.exit(0)
            else:
                print(result)

        
        elif(valve_state == 1):
            #open the valve
            COMMAND = 'python3 /home/pi/git/Thermostat/src/control_relay.py -r 1 -s 1'
            ssh = subprocess.Popen(["ssh", "%s" % self.relay_ip, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
            result = ssh.stdout.readlines()
            if result == []:
                error = ssh.stderr.readlines()
                print("open valve",error)
                sys.exit(0)
            else:
                print(result)


        else:
            print(valve_state,' not defined')
            pass
