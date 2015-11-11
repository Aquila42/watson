import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import csv
from random import randint

#Replace these with your own OAuth info!
auth = tweepy.OAuthHandler("wu3JYcJG4LQ2Lb71PQCDAwrRN", "2IEkOa0mE8qBdsW1HB4RmspXXX3mnbSWUW82AdMDm5SZ6PIKUs")
auth.set_access_token("17377774-b8FFONpU6OoZ2FOcQI5GbNNaFlDJ25hubOFxU9sVi", "USmuFIoC82z4ajrNb71ZfMD01v6JswRxjmBvSLFXuJOfy")

api = tweepy.API(auth)

overall=0
while overall<10000:
    try:
        #generate a random user id
        rand=randint(1,1000000000)
        print rand
        n=[]
        n.append(rand)
        #check if the user id is legit; if not, make another; if so, continue
        test=api.lookup_users(user_ids=n)
        sn=""
        ln=""
        img=""
        #gathering info
        for user in test:
            sn=user.screen_name
            ln=user.lang
            img=user.profile_image_url
        if ln=="en":
            #for each tweet in the max amount (200) for the user, not including RTs
            #this will give you (Prev tweet amount)-(Tweets that were RTs), so you'll probably get back <200.
            ct=0
            for pg in xrange(1,6):
                timeline=api.user_timeline(screen_name=sn,count=200, page=pg)
                for tweet in timeline:
                    ct+=1
            print ct
            #if user set lang to english and over 100 tweets from last part
            #make file for each user found; includes screen name, pic, tweets
            if ct>=900:
                print "name: ", sn
                f=open(sn+'.txt', 'a')
                f.write(sn+"\n")
                img=img.replace("normal", "400x400")
                f.write(img+"\n")
                writect=0
                for pg in xrange(1,6):
                    timeline=api.user_timeline(screen_name=sn,count=200, page=pg) #maximumcount of tweet
                    for tweet in timeline:
                        tw = tweet.text
                        f.write(tw.encode("utf-8")+"\n")
                        writect+=1
                f.close()
                overall+=1
    except:
        print "No account found"
