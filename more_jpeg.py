import tweepy
from PIL import Image
from urllib2 import urlopen
import os

#twitter API auth
consumer_key = open("consumer_key.dat", "r").read()
consumer_secret = open("consumer_secret.dat", "r").read()
access_token = open("access_token.dat", "r").read()
access_secret = open("access_secret.dat", "r").read()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
    	#this function will excecute any time a new tweet is posted containing a tracked term
    	#print status
        #print(status.text)
        tweet_author = status.author.screen_name
        tweet_id = status.id
        try:
        	#get the image from the tweet and load it as a PIL.Image object
        	image_url = status.entities['media'][0]['media_url']
        	im = Image.open(urlopen(image_url))
        	#compress the image and save it as compressed.jpg
        	im.save('compressed.jpg', "JPEG", quality=7)
        	#prepare the reply text
        	reply_text = "@%s freshly compressed just for you!" % tweet_author
        	api.update_with_media(filename="compressed.jpg", status=reply_text, in_reply_to_status_id=tweet_id)
        except:
        	reply_text = "@%s that tweet didn't seem to contain an image, please try again" % tweet_author
        	api.update_status(reply_text, tweet_id)
        return True


    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
myStream.filter(track=['@more_jpeg'])
