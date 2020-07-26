import sys
from twitter_wrapper import make_twitter_request


def harvest_user_timeline(twitter_api, screen_name=None, user_id=None, max_results=1000, po_ile=1):
    assert (screen_name != None) != (user_id != None), \
    "Argumenty!"
    kw = {  # Keyword args for the Twitter API call\n",
        'count': po_ile,
        'trim_user': 'true',
        'include_rts' : 'true',
        'since_id' : 1
        }
    if screen_name:
        kw['screen_name'] = screen_name
    else:
        kw['user_id'] = user_id
    max_pages = 20
    results = []
    tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
    if tweets is None: # 401 (Not Authorized) - Need to bail out on loop entry\n",
        tweets = []
    results += tweets
    print('Fetched {0} tweets'.format(len(tweets)), file=sys.stderr)
    page_num = 1
    if max_results == kw['count']:
        page_num = max_pages # Prevent loop entry\n",
    while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:
        kw['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1
        tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
        results += tweets
        print('Fetched {0} tweets'.format(len(tweets)),file=sys.stderr)
        page_num += 1
    print('Done fetching tweets', file=sys.stderr)
    #print(results)
    return results





