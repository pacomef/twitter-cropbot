import credentials
from tweepy import OAuthHandler
import tw
import db
import cropper


if __name__ == "__main__":

    open_stream = True

    auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)

    api = tw.API(auth)

    if open_stream:

        hash_tag_list = ["@CropThisBot"]
        twitter_streamer = tw.TwitterStreamer()
        twitter_streamer.stream_tweets(hash_tag_list, auth, api)

    #url = "https://pbs.twimg.com/media/EcMMdIIWkAc-Fvq?format=jpg&name=large"
    #cropper.crop(url)

