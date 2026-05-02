# this is code to control a mqtt broker system,especially the zigbee2mqtt fro homeassistant


import paho.mqtt.client as mqtt

class MyMQTTClient(mqtt.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #initialize the MQTT client and set the on_connect and on_message callbacks
        MQC = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        #MQC = mqtt.Client()

        #Set username and password
        uname = 'addons'
        pw = 'phooGhu0au4zaem3ooB5yapheM1oXaifishiubooH0quio2Ziig2OorohC1oShen'
        MQC.username_pw_set(uname, pw)

        MQC.on_connect = self.on_connect
        MQC.on_message = self.on_message
        MQC.on_publish = self.on_publish

        unacked_publish=set()
        MQC.user_data_set(unacked_publish)
        MQC.connect("192.168.3.201", 1883, 60)


        msq_info = MQC.publish('zigbee2mqtt/ikea_5/set', 'ON', qos=1)
        print(msq_info)
        unacked_publish.add(msq_info.mid)

        #msq_info = MQC.subscribe('zigbee2mqtt/ikea_5/set')
        #print(msq_info)    

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        print("on_message")
        print(msg.topic+" "+str(msg.payload))

    def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
        try:
            userdata.remove(mid)
        except KeyError:
            print("on_publish() is called with a mid not present in unacked_publish")
            print("This is due to an unavoidable race-condition:")
            print("* publish() return the mid of the message sent.")
            print("* mid from publish() is added to unacked_publish by the main thread")
            print("* on_publish() is called by the loop_start thread")
            print("While unlikely (because on_publish() will be called after a network round-trip),")
            print(" this is a race-condition that COULD happen")
            print("")
            print("The best solution to avoid race-condition is using the msg_info from publish()")
            print("We could also try using a list of acknowledged mid rather than removing from pending list,")
            print("but remember that mid could be re-used !")

    def on_subscribe(client, userdata, mid, reason_code_list, properties):
        # Since we subscribed only for a single channel, reason_code_list contains
        # a single entry
        if reason_code_list[0].is_failure:
            print(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")


if __name__ == "__main__":
    client = MyMQTTClient()
    #client.loop_forever()   