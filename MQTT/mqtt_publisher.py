###Standalone Publisher Script
import paho.mqtt.publish as publish

mqtt_server = "192.168.43.23"
mqtt_path = "test_channel"

publish.single(mqtt_path,"Text Message",hostname = mqtt_server)
