import tweepy
from PIL import Image
from urllib2 import urlopen
import os
from random import randint
from keys import keys

#twitter API auth
consumer_key = keys["consumer_key"]
consumer_secret = keys["consumer_secret"]
access_token = keys["access_token"]
access_secret = keys["access_secret"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

responses =    ["Freshly compressed, just for you!",
		"Let's JPEG it up!",
		"JPEG FTW!",
		"If it ain't blocky, it ain't compressed enough!",
		"Mmmm... compression artifacts!",
		"I love me some JPEG!"]

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
    	#this function will excecute any time a new tweet is posted containing a tracked term
    	#print status
        #print(status.text)
        tweet_author = status.author.screen_name
	print "Author: %s" % tweet_author
	print "Text: %s" % status.text
        tweet_id = status.id
        try:
        	#get the image from the tweet and load it as a PIL.Image object
        	image_url = status.entities['media'][0]['media_url']
        	im = Image.open(urlopen(image_url))
		print "Image URL: %s" % image_url
        	#compress the image and save it as compressed.jpg
        	im.save('compressed.jpg', "JPEG", quality=7)
        	#prepare the reply text
		snarky_response = responses[randint(0, len(responses))]
        	reply_text = "@%s %s" % (tweet_author, snarky_response)
        	api.update_with_media(filename="compressed.jpg", status=reply_text, in_reply_to_status_id=tweet_id)
        except:
        	reply_text = "@%s that tweet didn't seem to contain an image, please try again" % tweet_author
        	print "No image detected in tweet"
		api.update_status(reply_text, tweet_id)
	print
        return True


    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
myStream.filter(track=['@more_jpeg'])
