import subprocess

a = 'mosquitto_pub -h 192.168.3.201  -t '


#b0 = 'ikea_5'
b0 = 'ikea_1' \
''

b = '\'zigbee2mqtt/'+b0+'/set\' '
#b = '\'zigbee2mqtt/'+b0 +'\' '

c = '-m \"ON" '

c0 = '-m \"OFF" '

d =  ' -d -u \'addons\' -P \'phooGhu0au4zaem3ooB5yapheM1oXaifishiubooH0quio2Ziig2OorohC1oShen\' '



e = a + b + c + d



subprocess.Popen(e,shell=True)
