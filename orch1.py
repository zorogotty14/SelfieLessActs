import hashlib
import datetime
import base64
from flask import Flask, url_for,jsonify,abort
from flask import request
from flask import abort
import json
from flask_cors import CORS
import base64
import binascii
import re
import urllib.request
import requests 
from threading import Lock, Thread
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
lock = Lock()
lock1 = Lock()
lock2 = Lock()
lock3 = Lock()
counter = 0
active = 0

actsip = "http://127.0.0.1:"
#actsip = "http://127.0.0.1:"
pathToActsFile = "/home/anudeep/ActsFile"
app = Flask(__name__)
CORS(app)


ports = [8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010]

active_containers = [8000]

def sensor():
	global active_containers
	for i in active_containers:
		r = requests.get(actsip+str(i)+"/api/v1/_health")
		if(r.status_code==500):
			lock2.acquire()
			print("Container at", str(i), "UNhealthy")
			active_containers.remove(i)
			print("ACTIVE  - HEALTHY CONTAINERS : ", active_containers)
			res = os.popen("sudo docker container ls | grep -i \""+str(i)+"\"").read()
			id = str(res).split()[0]
			os.system("sudo docker stop "+ id)
			os.system("sudo docker rm "+id)
			os.system("sudo docker run -d -v "+pathToActsFile+":/acts/ActsFile -p "+str(i)+":80 acts")
			active_containers.append(i)
			lock2.release()
		else:
			print("[",time.ctime().split()[3],"] Container at", str(i), "healthy")


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=1)
sched.start()




def timer2min():
	global active_containers, ports, counter
	print("TIMER RUNNING - ", time.ctime().split()[3])
	running = len(active_containers)
	print("Total no of requests in the 2 mins : ", counter)
	active = 0
	if(counter<20):
		active=1
	elif(counter<40):
		active = 2
	elif(counter<60):
		active = 3
	elif(counter<80):
		active = 4
	elif(counter<100):
		active = 5
	elif(counter<120):
		active = 6
	elif(counter<140):
		active = 7
	elif(counter<160):
		active = 8
	elif(counter<180):
		active = 9
	elif(counter<=200):
		active = 10
	print("ACTIVE CONTAINERS : ", active_containers)
	if(running < active):
		add = active-running
		ports_to_run = ports[0:add]
		print("ADDING",add,"CONTAINERS AT PORTS", ports_to_run)
		for i in ports_to_run:
			id = os.popen("sudo docker run -d -v "+pathToActsFile+":/acts/ActsFile -p "+str(i)+":80 acts").read()
			lock.acquire()
			active_containers.append(i)
			ports.remove(i)
			lock.release()
		print("New active containers : ",active_containers)
	elif(running > active):
		rem = running-active
		
		cont = active_containers[-rem:]
		print("REMOVING",rem,"CONTAINERS AT PORTS",cont)
		lock.acquire()
		active_containers = active_containers[:-rem]
		lock.release()
		print("New active containers : ", active_containers)
		for top in cont:
			res = os.popen("sudo docker container ls | grep -i \""+str(top)+"\"").read()
			id = str(res).split()[0]
			os.system("sudo docker stop "+ id)
			os.system("sudo docker rm "+id)
		ports.extend(cont)
	lock.acquire()
	counter = 0
	lock.release()
	print("Resetting counter : ", counter)



@app.route('/',methods=['POST','GET','DELETE'])
def what_to_do():
	############## TO-DO ###############
	# Do nothing
	return jsonify({}), 200



# API 3, 4 - List/Add categories      

@app.route('/api/v1/categories',methods=['POST','GET'])
def add_categories():
	global counter, active_containers, active
	print("active is : ", active)
	if(active==0):
		print("Checking started")
		timer = BackgroundScheduler(daemon=True)
		timer.add_job(timer2min,'interval',minutes=2)
		timer.start()
	lock.acquire()
	counter+=1
	active = 1
	portno = active_containers.pop(0)
	active_containers.append(portno)
	lock.release() 
	print("Request made to port : ", str(portno),"count=",counter)
	API_ENDPOINT = actsip+str(portno)+"/api/v1/categories"
	if request.method == 'POST':
		data = [request.json[0]]
		r = requests.post(url = API_ENDPOINT, json = data) 
		if(r.status_code>204):
			return r.text, r.status_code
		if(r.status_code==204):
			return jsonify({}), r.status_code
		return jsonify(r.json()), r.status_code
	elif request.method == 'GET':
		r = requests.get(API_ENDPOINT)
		if(r.status_code>204):
			return r.text, r.status_code
		if(r.status_code==204):
			return jsonify({}), r.status_code
		return jsonify(r.json()), r.status_code
	else:
		return "Method not allowed", 405

# API 5 - Delete categories      

@app.route('/api/v1/categories/<categoryName>',methods=['DELETE'])
def delete_category(categoryName):
	global counter, active
	if(active==0):
		timer = BackgroundScheduler(daemon=True)
		timer.add_job(timer2min,'interval',minutes=2)
		timer.start()
	lock.acquire()
	counter+=1
	active = 1 
	portno = active_containers.pop(0)
	active_containers.append(portno)
	lock.release()
	r = requests.delete(actsip+str(portno)+"/api/v1/categories/"+categoryName)
	print(r.status_code)
	if(r.status_code>204):
		return r.text,r.status_code
	if(r.status_code==204):
		return jsonify({}), r.status_code
	return jsonify(r.json()), r.status_code


# API 6,8 - List acts in category

@app.route('/api/v1/categories/<categoryName>/acts',methods=['GET'])
def List_Acts(categoryName):
	global counter,active
	if(active==0):
		timer = BackgroundScheduler(daemon=True)
		timer.add_job(timer2min,'interval',minutes=2)
		timer.start()
	lock.acquire()
	counter+=1
	active = 1 
	portno = active_containers.pop(0)
	active_containers.append(portno)
	lock.release()
	if request.method!="GET":
		return "Method not allowed", 405
	list2 = request.args
	if(len(list2)==2):
		r = requests.get(actsip+str(portno)+"/api/v1/categories/"+categoryName+"/acts?start="+list2['start']+"&end="+list2['end'])
		if(r.status_code>204):
			return r.text, r.status_code
		if(r.status_code==204):
			return jsonify({}), r.status_code
		return jsonify(r.json()), r.status_code
	elif(len(list2)==0):
		r = requests.get(actsip+str(portno)+"/api/v1/categories/"+categoryName+"/acts")
		if(r.status_code > 204):
			return r.text, r.status_code
		if(r.status_code==204):
			return jsonify({}), r.status_code
		return jsonify(r.json()), r.status_code
	else:
		return "Method not allowed", 405


# API 7 - list no of acts for a given category

@app.route('/api/v1/categories/<categoryName>/acts/size',methods=['GET'])
def No_Acts_Category(categoryName):
	global counter, active
	if(active==0):
		timer = BackgroundScheduler(daemon=True)
		timer.add_job(timer2min,'interval',minutes=2)
		timer.start()
	lock.acquire()
	active = 1
	counter+=1
	portno = active_containers.pop(0)
	active_containers.append(portno)
	lock.release() 
	API_ENDPOINT = actsip+str(portno)+"/api/v1/categories/"+categoryName+"/acts/size"
	if(request.method!="GET"):
		return "Method not allowed", 405
	r = requests.get(API_ENDPOINT)
	if(r.status_code>204):
		return r.text, r.status_code
	if(r.status_code==204):
		return jsonify({}), r.status_code
	return jsonify(r.json()), r.status_code

	
# API 9 - Upvote an act

@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote():
	global counter, active
	if(active==0):
		timer = BackgroundScheduler(daemon=True)
		timer.add_job(timer2min,'interval',minutes=2)
		timer.start()
	lock.acquire()
	active = 1
	counter+=1 
	portno = active_containers.pop(0)
	active_containers.append(portno)
	lock.release()
	if request.method != 'POST':
		return "Method not allowed", 405
	API_ENDPOINT = actsip+str(portno)+"/api/v1/acts/upvote"
	data = [request.json[0]]
	r = requests.post(url = API_ENDPOINT, json = data) 
	if(r.status_code>204):
		return r.text, r.status_code
	if(r.status_code==204):
		return jsonify({}), r.status_code
	return jsonify(r.json()), r.status_code	


# API 10 - Remove an act

@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_act(actId):
	global counter, active
	if(active==0):
		timer = BackgroundScheduler(daemon=True)
		timer.add_job(timer2min,'interval',minutes=2)
		timer.start()
	lock.acquire()
	active = 1
	counter+=1
	portno = active_containers.pop(0)
	active_containers.append(portno)
	lock.release() 
	if request.method!='DELETE':
		return "Method not allowed", 405
	API_ENDPOINT = actsip+str(portno)+"/api/v1/acts/"+actId
	r = requests.delete(API_ENDPOINT)
	print("here delete.......", r.text, r.status_code)
	if(r.status_code>204):
		return r.text, r.status_code
	if(r.status_code==204):
		return jsonify({}), r.status_code
	return jsonify(r.json()), r.status_code


# API 11 - Upload an act

@app.route('/api/v1/acts',methods=['POST'])
def upload_acts():
	lock3.acquire()
	global counter, active, active_containers
	if(active==0):
		timer = BackgroundScheduler(daemon=True)
		timer.add_job(timer2min,'interval',minutes=2)
		timer.start()
	active = 1
	counter+=1
	portno = active_containers.pop(0)
	active_containers.append(portno)
	API_ENDPOINT = actsip+str(portno)+"/api/v1/acts"
	if(request.method!="POST"):
			return "Method not allowed", 405
	r = requests.post(url = API_ENDPOINT, json = request.json)
	lock3.release()
	if(r.status_code>204):
		return r.text, r.status_code
	if(r.status_code==204):
		return jsonify({}), r.status_code
	return jsonify(r.json()), r.status_code


if __name__=="__main__":
	app.run(host="0.0.0.0", port=80, debug=True)
