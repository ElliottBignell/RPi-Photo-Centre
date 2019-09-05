"""
A simple Python script to receive messages from a client over 
Bluetooth using PyBluez (with Python 2). 
"""

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


install_and_import('bluetooth')
# import bluetooth 

hostMACAddress = '00:1f:e1:dd:08:3d' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
port = 3 
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
	client, clientInfo = s.accept()
	while 1:
		data = client.recv(size)
		if data:
			print(data)
			client.send(data) # Echo back to client
except:	
	print("Closing socket")
	client.close()
	s.close()
