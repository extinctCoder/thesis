import paho.mqtt.client as mqtt
"""import cv2
img = cv2.imread("cover.jpeg") 
f=open("cover.jpeg","rb")
fileContent = f.read()
byteArr = bytearray(fileContent)"""
broker_address="192.168.0.101"
client= mqtt.Client("p1")
client.connect(broker_address)
#client.subscribe("test/message")
client.publish("test/message","working",0)
client.loop()