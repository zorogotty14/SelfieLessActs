import glob, os
import base64
import requests
import time

os.chdir("/home/anudeep/Desktop/Images")

files=[]
for file in glob.glob("*"):
	if(file!='upload.py'):
		files.append(file)


no = 3000
cc = 1
cat = ["social_responsibility","cooking","friendship"]
usr=["dinesh","anudeep","deekshith","aswath"]

c=0
u=0

k=0

for FILE in files:
	with open(FILE,"rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
			encoded_string = str(encoded_string)
			encoded_string = encoded_string[2:(len(encoded_string)-1)]
			#print(encoded_string)
			
			inp = {"actId":no,"caption":"hey this caption" + str(cc),"categoryName":cat[c],"username":usr[u],"timestamp":"01-01-2019:45-23-03","imgB64":encoded_string}
			no=no+1
			cc=cc+1
			u=(u+1)%len(usr)
			c=(c+1)%len(cat)
			print(inp)
			req = requests.post("http://107.20.32.130/api/v1/acts", json = inp)
			print(req.status_code)

			if(k==42):
				time.sleep(130)
			print(k)
			k=k+1


