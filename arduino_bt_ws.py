import sys, os, datetime, time, random, json, socket
import asyncio, websockets, threading, bluetooth
import subprocess as sp
import sounddevice as sd
import numpy as np

connections = []
volume_norm = 0
gsr_value = b'0'

bd_addr = "98:D3:51:FE:29:E3" #HC-05 address
port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

def connectBluetooth():
    global  bd_addr, port, sock
    try:
        sock.connect((bd_addr, port))
        print('Connecting to Bluetooth '+bd_addr)
        sock.settimeout(1.0)
    except Exception as e:
        print("Error Exception")
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        stdoutdata = sp.getoutput("hcitool scan")
        if bd_addr in stdoutdata.split():
            print("Bluetooth device is still out there")
            # port = port+1
            sock.shutdown(socket.SHUT_RDWR)
            # sock.close()
            sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            connectBluetooth()
        else:
            print("Bluetooth device not found")
            # print('Cannot connect to Bluetooth '+bd_addr)
        # sock.quit()
        # sock.close()
        # sock.shutdown(socket.SHUT_RDWR)
        # sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

def print_sound(indata, outdata, frames, time, status):
    global volume_norm
    volume_norm = np.linalg.norm(indata)*10
    # print("|" * int(volume_norm))

async def process(websocket, path):
    print("someone's connecting")
    connections.append(websocket)
    print(connections)
    while True:
        # msg = await websocket.recv()
        try:
            msg = await websocket.recv()
        except:
            break
        if msg is not None:
            print(msg)
        else:
            connections.remove(websocket)
            break

async def send_data():
    global  bd_addr, sock

    msg = ""
    data_gsr = "0"
    data_sound = "0"
    with sd.Stream(callback=print_sound):
        while True:
            await asyncio.sleep(0.01)
            try:
                data = sock.recv(1)
                data = data.decode("utf-8")
            except:
                data = ""
                stdoutdata = sp.getoutput("hcitool con")
                if bd_addr in stdoutdata.split():
                    print("Bluetooth device is still connected")
                else:
                    connectBluetooth()

            # print("msg = "+msg)
            if msg.find('\r\n') > 0:
                msg = msg.split('\r')[0]
                # print("msg = "+msg)
                # data_gsr = "0"
                # data_sound = "0"
                try:
                    data_gsr = msg.split('#')[0]
                    # data_sound = msg.split('#')[1]
                except:
                    data_gsr = "0"
                    # data_sound = "0"
                msg = ""
            else:
                msg = msg+data

            data_sound = str(volume_norm)
            print('{"data_sound": "'+data_sound+'", "data_gsr": "'+data_gsr+'"}')
            for connection in connections:
                try:
                    await connection.send('{"data_sound": "'+data_sound+'", "data_gsr": "'+data_gsr+'"}')
                except:
                    connections.remove(connection)
while 1:
    stdoutdata = sp.getoutput("hcitool con")
    if bd_addr in stdoutdata.split():
        break
    else:
        connectBluetooth()
start_server = websockets.serve(process, "0.0.0.0", 1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.ensure_future(send_data())
asyncio.get_event_loop().run_forever()