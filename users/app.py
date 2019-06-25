import hashlib
import datetime
import base64
from flask import Flask, url_for,jsonify
from flask import request
import json
from flask_cors import CORS
import base64
import binascii
import re

counter=0
users_list = []
hexdigits = ['0','1','2','3',
						 '4','5','6','7','8','9',
						 'a','b','c','d','e','f',
						 'A','B','C','D','E','F']

app = Flask(__name__)
CORS(app)



data1={}
data1['people']=[]

with open('data.txt') as json_file:
	data = json.load(json_file)
	if(not data['people']):
			data['people'] = []
	for p in data['people']:
			data1['people'].append({'username':p['username'],'password':p['password']})


 # API 1 - add a username, password, List all users

@app.route('/api/v1/users',methods=['GET','POST'])
def profile():
	global counter
	counter+=1
	if request.method == 'POST':
		name=request.json['username']
		password =request.json['password']
		print(name, password)
		if name == '' or password=='':
				return "Something empty. Bad request", 400
		for i in data1['people']:
				if i['username'] == name:
						return "Username exists. Bad request", 400
		if(len(password)!=40):
				return "Not SHA password length. Bad request", 400
		for ch in password:
				if(ch not in hexdigits):
						return "Not SHA password. Bad request", 400
		data1['people'].append({'username':name,'password':password})
		with open('data.txt', 'w') as outfile:
				json.dump(data1, outfile)
		return jsonify({}),201
	elif(request.method=='GET'):
		user_list = []
		for i in data1['people']:
				user_list.append(i['username'])
		if(not user_list):
				return jsonify([]), 204
		return jsonify(user_list), 200
	else:
		return "Method not allowed", 405



# API 2 - delete a user

@app.route('/api/v1/users/<user>',methods=['DELETE'])
def remove_user(user):
	global counter
	counter+=1
	if request.method == 'DELETE':
			f=0
			for i in data1['people']:
					if i['username'] == user:
							data1['people'].remove(i)
							f=1
			if f==0:
					return "Username not present. Bad request", 400
			with open('data.txt', 'w') as outfile:
					json.dump(data1, outfile)
			return jsonify({}),200
	else:
			return "Method not allowed",405


# API 3,4 - Get total HTTP requests made to microservice

@app.route('/api/v1/_count',methods=['GET', 'DELETE'])
def countHTTP():
	global counter
	if request.method=="GET":
		return jsonify([counter]), 200
	elif request.method=="DELETE":
		counter=0
		return jsonify([]), 200
	else:
		return "Method not allowed", 405 


if(__name__=="__main__"):
		app.run(host="0.0.0.0", port=8080, debug=True)

