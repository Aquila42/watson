import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import csv
from random import randint

#entered="mammal_champ"

def tweets(entered):
	#Replace these with your own OAuth info!
	auth = tweepy.OAuthHandler("wu3JYcJG4LQ2Lb71PQCDAwrRN", "2IEkOa0mE8qBdsW1HB4RmspXXX3mnbSWUW82AdMDm5SZ6PIKUs")
	auth.set_access_token("17377774-b8FFONpU6OoZ2FOcQI5GbNNaFlDJ25hubOFxU9sVi", "USmuFIoC82z4ajrNb71ZfMD01v6JswRxjmBvSLFXuJOfy")
	api = tweepy.API(auth)
	un=""
	id=0
	t=api.user_timeline(screen_name=entered, count=200)
	f=open(entered+'.txt', 'w')
	for tweet in t:
		un = tweet.user.screen_name
		if id==0 and un== entered:
			id=tweet.user.id
		tw = tweet.text
		f.write(tw.encode("utf-8")+"\n")
	f.close()	
	print id










