# -*- coding: utf-8 -*-
import os
from alchemyapi import AlchemyAPI

path='gen_idk'

print path

alchemyapi = AlchemyAPI()

thresh=0.9

for filename in os.listdir(path):
	ct=0
	gender=""
	genderscore=0.0
	ok=False
	f=open(path+"/"+filename)
	for line in f:
		if ct==1:
			image_url=line.strip()
			print image_url
			response=alchemyapi.faceTagging('url', image_url)
			if response['status'] == 'OK':
				ok=True
				for keyword in response['imageFaces']:
					gender=keyword['gender']['gender']
					genderscore=float(keyword['gender']['score'])
					print "Gender: "+gender
					print "Score: "+str(genderscore)
			break
		if ct==0:
			ct+=1
	f.close()
	print filename
	if ok:
		if genderscore>=thresh:
			if gender=="FEMALE":
				os.rename(path+'/'+filename, 'gend_female/'+filename)
			elif gender=="MALE":
				os.rename(path+'/'+filename, 'gend_male/'+filename)
			else:
				os.rename(path+'/'+filename, 'gend_unknown/'+filename)
		else:
			os.rename(path+'/'+filename, 'gend_unknown/'+filename)
