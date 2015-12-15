#!/usr/bin/env python

#	Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
import sys


image_url = 'https://pbs.twimg.com/profile_images/2911745249/576ef0e3f2cf7a8c51adfd981751ee03.jpeg'
#image_url= 'https://www.petfinder.com/wp-content/uploads/2012/11/140272627-grooming-needs-senior-cat-632x475.jpg'

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI("fbfba639448679ae5b19e880f162aed9d7498284")

# Old code
# response = alchemyapi.faceTagging('url', image_url)

#New alchemyapi_python package
response = alchemyapi.face_tagging('url', image_url)

if response['status'] == 'OK':
    print('## Image Information ##\n')
else:
    print('noooo')

found=False
for keyword in response['imageFaces']:
    found=True
    gender=keyword['gender']['gender']
    genderscore=keyword['gender']['score']
    age=keyword['age']['ageRange']
    agescore=keyword['age']['score']
    print("Gender: "+gender)
    print("Score: "+genderscore)
    print("")
    print("Age: "+age)
    print("Score: "+agescore)

if not found:
    print ("Could not determine gender or age")
