import sys
from twitter_wrapper import make_twitter_request
from functools import partial
from sys import maxsize as maxint
import twitter
from urllib.parse import unquote
import json

#User must enter following keys and tokens:
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None, friends_limit=maxint, followers_limit=maxint):

    assert (screen_name != None) != (user_id != None)

    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids, count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids, count=5000)

    friends_ids, followers_ids = [], []

    for twitter_api_func, limit, ids, label in [[get_friends_ids, friends_limit, friends_ids, "friends"], [get_followers_ids, followers_limit, followers_ids, "followers"] ]:
        if limit == 0: continue

        cursor = -1
        while cursor != 0:
            if screen_name:
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id\n",
                response = twitter_api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
            print('Fetched {0} total {1} ids for {2}'.format(len(ids), label, (user_id or screen_name)),file=sys.stderr)
            if len(ids) >= limit or response is None:
                break
    return friends_ids[:friends_limit], followers_ids[:followers_limit]


#friends_ids, followers_ids = get_friends_followers_ids(twitter_api, screen_name="AstroNETpl",friends_limit=10,followers_limit=200)
print(friends_ids)
print((followers_ids))
user=make_twitter_request(twitter_api.users.lookup,user_id=followers_ids[0])
print(user[0]["name"])
print(json.dumps(user, indent=1))

