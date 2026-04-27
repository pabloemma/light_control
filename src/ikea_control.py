import subprocess

a = 'mosquitto_pub -h 192.168.3.201  -t '

b = '\'zigbee2mqtt/ikea_5/set\' '

c =  '-m \"ON\" -d -u \'addons\' -P \'phooGhu0au4zaem3ooB5yapheM1oXaifishiubooH0quio2Ziig2OorohC1oShen\' '

d = a+b+c

subprocess.Popen(d,shell=True)
