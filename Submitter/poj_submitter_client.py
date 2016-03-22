#!/usr/bin/env python3
import socket, pickle

# USERNAME = input("username = ")
# PASSWD = input("passwd = ")
# PROBLEM_ID = input("problem_id = ")
# LANGUAGE = input("language = ")
client = socket.socket()
client.connect(('127.0.0.1', 32768))
data = ["yourusername", "yourpasswd", "1000", "0"]
#client.sendall(pickle.dumps([USERNAME, PASSWD, PROBLEM_ID, LANGUAGE]))
client.sendall(pickle.dumps(data))

while True:
	status = client.recv(1024).decode('utf-8')
	print(status)
	if status != 'Waiting' and status != 'Compiling' and status != 'Running & Judging':
			break
client.close()
