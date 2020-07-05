from tweepy.streaming import StreamListener
from tweepy import Stream, API
import json
import cropper
import db
import os
import sys

sys.stdout.flush()


class TwitterStreamer():

    def stream_tweets(self, hash_tag_list, auth, api):
        listener = StdOutListener(api)
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


class StdOutListener(StreamListener):

    def __init__(self, api):
        self.api = api

    def on_data(self, raw_data):
        try:
            process_tweet(raw_data, self.api)
            return True
        except BaseException as e:
            print("Error : {0}".format(e), flush=True)

    def on_error(self, status_code):
        print(status_code)
        if status_code == "420":
            print("E:420 Please wait before restarting the stream", flush=True)
        return True


def saveTweet(data):
    array = json.loads(data)
    user = array["user"]["screen_name"]
    message_to_reply = array["id"]
    message_to_save = array["in_reply_to_status_id"]
    reply("Saved!", message_to_reply, user)


def reply(message, message_reply, user, api):
    api.update_status("@{0} {1}".format(user, message), message_reply)


def tweet(message, api):
    api.update_status(message)


def get_tweet(url, api):
    tweet_id = url.split('/')[-1]
    return api.get_status(tweet_id)


def get_twitter_url(user_name, status_id):
    return "https://twitter.com/" + str(user_name) + "/status/" + str(status_id)


def process_tweet(raw_data, api):
    total_pixels = 0
    media_ids = []
    data = json.loads(raw_data)
    user = data["user"]["screen_name"]
    sentence = "@{0} And here's your cropped picture!".format(user)
    original = get_tweet(get_twitter_url(data["in_reply_to_screen_name"], data["in_reply_to_status_id_str"]), api)
    try:
        media_len = len(original.extended_entities["media"])
    except:
        print("[!] No image provided by user {0}, skip".format(user), flush=True)
        return
    print("[-] {0} images requested by @{1}".format(media_len, user), flush=True)
    for x in range(media_len):
        url = original.extended_entities["media"][x]["media_url"]
        path, pixels = cropper.crop(url)
        total_pixels = total_pixels + pixels
        res = api.media_upload(filename=path)
        media_ids.append(res.media_id)
        print("[+] File {0} uploaded".format(path), flush=True)
        os.remove(path)
        print("[+] File correctly deleted", flush=True)
    status_tweet = api.update_status(status=sentence, media_ids=media_ids, in_reply_to_status_id=data["id"])
    past_tweet = get_twitter_url(user, data["id"])
    new_tweet = get_twitter_url(status_tweet.user.screen_name, str(status_tweet.id))
    user_id = data["user"]["id_str"]
    db.query(db.template_query.format(user, user_id, media_len, past_tweet, new_tweet, total_pixels))
    print('[-- + --] Tweet sent and loaded into DB ! Removed {0} pixels'.format(total_pixels), flush=True)
