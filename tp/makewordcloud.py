from __future__ import print_function
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
from nltk.corpus import stopwords
import json
import sys
import warnings

warnings.simplefilter("ignore")

def makecloud(name):
	cnt=0
	#file=open('age_over54_train/KABarron.txt')
	file=open(name+".txt")
	demo_text=""
	stop=stopwords.words('english')
	for line in file:
		if cnt<2:
			cnt+=1
		elif cnt<52:
			line=line.strip().replace("'", "").replace('"', '')
			if str(line).startswith("RT"):
				continue
			else:
				newline=[i for i in line.split() if i not in stop]
				finsent=""
				for word in newline:
					if "@" in word or "https" in word or ".co" in word or "http" in word:
						continue
					else:
						finsent+=word+" "
					
				demo_text+=finsent+" "
			cnt+=1
		else:
			break
		
		
	tags = make_tags(get_tag_counts(demo_text), maxsize=80)

	create_tag_image(tags, 'static/'+name+'_cloud.png', size=(900, 600), fontname='Lobster')
	#import webbrowser
	#webbrowser.open(name+'_cloud.png')
	return str(name+'_cloud.png')
