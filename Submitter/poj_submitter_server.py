#!/usr/bin/env python3
import requests, json, base64, time
import re, socket, pickle

USERNAME = ""
PASSWD = ""
PROBLEM_ID = ""
LANGUAGE = ""

#[username, passwd, problem, language, file]

def login():
	getData = {"user_id1":USERNAME, "password1":PASSWD, "B1":"login", "url":"/"}
	session = requests.session()
	session.post("http://poj.org/login", data=getData)	
	return session

def submit(session):
	source = ""
	with open("a+b.cpp") as f:
		source = base64.b64encode(f.read().encode("utf-8"))
	postData = {"problem_id":PROBLEM_ID, "language":LANGUAGE, "source":source, "submit":"Submit", "encoded":"1"}
	r = session.post("http://poj.org/submit", data=postData)
	return re.findall(r"<td>(.*?)</td>.*<font.*?>(.*?)</font>", r.text)[1][0]

def getStatus(session, runid, socketConnect):
	status = "Waiting"
	while True:
		html = session.get('http://poj.org/status?problem_id=' + PROBLEM_ID + '&user_id=' + USERNAME + '&language=' + LANGUAGE)
		statusList = re.findall("<td>(.*?)</td>.*<font.*?>(.*?)</font>", html.text)
		for result in statusList:
			if runid == result[0]:
				status = result[1]
				break
		socketConnect.send(status.encode('utf-8'))
		if status != 'Waiting' and status != 'Compiling' and status != 'Running & Judging':
			break
		time.sleep(2)

if __name__ == '__main__':
	server = socket.socket()
	server.bind(('127.0.0.1', 32768))
	server.listen(16)
	while True:
		connect, address = server.accept()
		USERNAME, PASSWD, PROBLEM_ID, LANGUAGE = pickle.loads(connect.recv(1024))
		session = login()
		runid = submit(session)
		getStatus(session, runid, connect)
	server.close()
