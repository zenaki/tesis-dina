# sudo apt install libbluetooth-dev
# python3 -m pip install PyBluez

import bluetooth
import sys
bd_addr = "98:D3:51:FE:29:E3" #HC-05 address

port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print('Connected')
sock.settimeout(1.0)
#sock.send("x")
#print('Sent data')

msg = ""
while 1:
    data = sock.recv(1)
    #print(type(data))
    data = data.decode("utf-8")
    if msg.find('\r\n') > 0:
        print("msg = "+msg.split('\r')[0])
        msg = ""
    else:
        msg = msg+data
    #print("msg = "+msg) 
    #print(data)

sock.close()