import socket
import tqdm
import os
import sys

# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

SEPARATOR = "<SEPARATOR>" # separator for filename and size transferring
BUFFER_SIZE = 4096 # send 4096 bytes each time step

args = sys.argv

# the ip address or hostname of the server, the receiver
# 192.168.31.151 - my local ip
host = args[2] 
# the port
port = args[3]
# the name of file we want to send, make sure it exists
filename = args[1]

# print out received port, host
print("host %s, port %s, file %s" % (host, port, filename))

# transferring
# host - where to send
# port - receiving port on host
# filename - file to be transferred
def transfer(host, port, filename):
	# get the file size
	filesize = os.path.getsize(filename)
	# create the client socket
	s = socket.socket()

	port = int(port)

	# connection to host:port
	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.")

	# send the filename and filesize
	s.send(f"{filename}{SEPARATOR}{filesize}".encode())

	# start sending the file
	progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	with open(filename, "rb") as f:
	    for _ in progress:
	        # read the bytes from the file
	        bytes_read = f.read(BUFFER_SIZE)
	        if not bytes_read:
	            # file transmitting is done
	            break
	        # we use sendall to assure transimission in 
	        # busy networks
	        s.sendall(bytes_read)
	        # update the progress bar
	        progress.update(len(bytes_read))
	# close the socket
	s.close()

transfer(host, port, filename)