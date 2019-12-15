import paho.mqtt.client as mqtt
import time

def on_msg(client,username,data):
  print("Msg:",str(msg.payload.decode("utf-8")))
  
 client = mqtt.Client("P1")
 client.on_message = on_msg
 
 client.connect("192.168.12.1")         ##IP to be changed
 client.loop_start()
 client.subscribe("a/b")
 client.publish("a/b","Harsh")          ##Name to be changed
 time.sleep(10)
 client.loop_stop()
