import time
import requests
import json
import os

file1 = open("input.json").read()
data = json.loads(file1)



print("************** GENERIC LOAD BALANCER **************")
print("Assumptions :
print("1. You have a docker image of your app created on an AWS instance")
print("2. This load balancer code is to be run on the instance containing the image")
print("3. Ports 8000-8020 are allowed for running the containers")
print("4. Need not have a container already running. If so, the container must be running at port 8000")


print("Image name : ", data["image_name"])
print("Triggers and actions : ")



#ip = input("enter your IP addreess you want to Load Balance->")
port_start = int(input("enter the port u want to start with"))

n = int(input("no of machines available"))

avail_ports  = [i for i in range(port_start+1,port_start+n)]

curr = [port_start]


starttime=time.time()
while True:
	total =0
	for i in curr:
		URL = "http://localhost:"+str(i)+"/api/v1/_count"
		r = requests.get(url = URL)
		data=r.json()
		total = total+data[0]
		print("in fro",curr,avail_ports)

	if(total>=10*len(curr)):
		print("start of if",curr,avail_ports)
		a=avail_ports.pop(0)
		id = os.popen("sudo docker run -d -p  "+str(a)+":80 app1").read()
		curr.append(a)
		print("end of if",curr,avail_ports)

	else:
		if(len(curr)>1):
			print("start of else",curr,avail_ports)
			a=curr.pop()
			res = os.popen("sudo docker container ls | grep -i \""+str(a)+"\"").read()
			id = str(res).split()[0]
			x1=os.popen("sudo docker stop "+ id).read()
			y1=os.popen("sudo docker rm "+id).read()
			avail_ports.append(a)
			print("end of of else",curr,avail_ports)

	time.sleep(10)


	for i in curr:
		URL_delete= "http://localhost:"+str(i)+"/api/v1/_count"
		r = requests.delete(URL_delete)
		print(r)

	print("tick")
	time.sleep(20.0 - ((time.time() - starttime) % 20.0))



# # api-endpoint 
# URL = "http://localhost:8000/api/v1/_count"
  
# # location given here 

  
# # sending get request and saving the response as response object 
# r = requests.get(url = URL)
  
# # extracting data in json format 
# data = r.json() 

# print(data)



# URL_delete= "http://localhost:8000/api/v1/_count"
# r = requests.delete(URL_delete)
# print(r)


#id = os.popen("sudo docker run -p -d "+"8009"+":80 app1").read()

res = os.popen("sudo docker container ls | grep -i \""+"8009"+"\"").read()
id = str(res).split()[0]
os.system("sudo docker stop "+ id)
os.system("sudo docker rm "+id)


