import tweepy
import urllib


def getTweeterInfo(entered):
    # Authenticate with Twitter
    auth = tweepy.OAuthHandler("wu3JYcJG4LQ2Lb71PQCDAwrRN", "2IEkOa0mE8qBdsW1HB4RmspXXX3mnbSWUW82AdMDm5SZ6PIKUs")
    auth.set_access_token("17377774-b8FFONpU6OoZ2FOcQI5GbNNaFlDJ25hubOFxU9sVi",
                          "USmuFIoC82z4ajrNb71ZfMD01v6JswRxjmBvSLFXuJOfy")

    # Connect with twitter using tweepy
    api = tweepy.API(auth)

    name = ""
    img = ""
    un = ""
    id = 0
    # t=api.user_timeline(screen_name=entered, count=200)
    tw = []
    for page in tweepy.Cursor(api.user_timeline, screen_name=entered, count=200).pages(4):
        for tweet in page:
            un = tweet.user.screen_name
            if id == 0 and un == entered:
                id = tweet.user.id
            tw.append(tweet.text)

    handle = entered

    test = api.lookup_users([id])
    for user in test:
        name = user.name
        img = user.profile_image_url
        img = img.replace("normal", "400x400")


    f = open('extracted_tweets/'+entered + '.txt', 'w')
    f.write(handle + "\n")
    f.write(img + "\n")
    for line in tw:
        f.write(line.encode("utf-8") + "\n")
    f.close()

    urllib.urlretrieve(img, "static/"+entered+".png")

    name = name.split()
    finalname = name[0].encode("utf-8")

    return finalname
