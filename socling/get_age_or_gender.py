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

def get_demographic(image_url,demographic,threshold):

    # Create the AlchemyAPI Object
    alchemyapi = AlchemyAPI()

    #New alchemyapi_python package
    response = alchemyapi.face_tagging('url', image_url)

    if response['status'] == 'OK':
        print('## Image Information ##\n')
    else:
        print('noooo')

    found=False
    for keyword in response['imageFaces']:
        found=True
        if demographic == "gender":
            gender=keyword['gender']['gender']
            genderscore=keyword['gender']['score']
            print("Gender: "+gender)
            print("Score: "+genderscore)
            if genderscore >= threshold:
                return gender
        elif demographic == "age":
            age=keyword['age']['ageRange']
            agescore=keyword['age']['score']
            print("Age: "+age)
            print("Score: "+agescore)
            if agescore >= threshold:
                return age
        print("Score less than threshold")
        return -1

    if not found:
        print ("Could not determine gender or age")
        return -1
