import paho.mqtt.client as mqtt
import time

class MQTTClientWrapper:
    def __init__(self, broker, port, client_id, topics):
        self.broker = broker
        self.port = port
        self.topics = topics
        

        uname = 'addons'
        pw = input("Please enter the password: ")

        # Initialize Paho Client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self.client.username_pw_set(uname, pw)
        
        # Set Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected Successfully!")
            for topic in self.topics:
                self.client.subscribe(topic)
                print(f"Subscribed to: {topic}")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received: {msg.payload.decode()} on topic: {msg.topic}")

    def start(self):
        self.client.connect(self.broker, self.port, 60)
        # Use loop_start() for non-blocking background loop
        self.client.loop_start() 

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, message):
        self.client.publish(topic, message)
    def subscribe(self, topic):
        self.client.subscribe(topic)

# Usage
if __name__ == "__main__":
    broker = "192.168.3.201"
    port = 1883
    client = MQTTClientWrapper(broker, port, "class_example_id", ["zigbee2mqtt/ikea_5/set"])
    
    client.start()
    client.subscribe("zigbee2mqtt/ikea_5/set")

    client.publish("zigbee2mqtt/ikea_5/set", "OFF")
    
    time.sleep(5)  # Keep running to receive messages
    client.stop()
