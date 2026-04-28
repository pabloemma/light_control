import subprocess

a = 'mosquitto_sub -h 192.168.3.201  -t '


#b0 = 'ikea_5'
#b0 = 'ikea_2'
b0 = '\'zigbee2mqtt/ikea_5/set\''
#b = '\'zigbee2mqtt/'+b0+' '
b = b0+' '

#c = '-m \"ON" '

#c0 = '-m \"OFF" '
# -W means exit after x seconds timeout
d =  ' -d -u \'addons\' -P \'phooGhu0au4zaem3ooB5yapheM1oXaifishiubooH0quio2Ziig2OorohC1oShen\' -W 60 -C 1'



e = a + b + d
print(e)



subprocess.Popen(e,shell=True)
