import base64
import socket
import cv2
import numpy

TCP_IP = '192.168.0.101'
TCP_PORT = 5000

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
capture = cv2.imread("cover.jpeg")
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
result,imgencode = cv2.imencode('.jpg', capture)
jpg_as_text = base64.b64encode(imgencode)
print(jpg_as_text)
sock.send( jpg_as_text )
sock.close()