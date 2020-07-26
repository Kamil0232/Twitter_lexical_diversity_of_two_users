import twitter
from Data import harvest_user_timeline
from prettytable import PrettyTable
from collections import Counter
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

#User must enter following keys and tokens:
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

obiekt1 = 'tvp_info'
obiekt2 = 'tvn24'


def lexical_diversity(tokens):
    return len(set(tokens))/len(tokens)


def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return total_words/len(statuses)


kroki = [100,200,300,400,500,600,700,800,900,1000]
tvp_list = []
tvn_list = []

for step in kroki:
    tweets1 = harvest_user_timeline(twitter_api, screen_name=obiekt1, max_results=step, po_ile=100)
    tweets2 = harvest_user_timeline(twitter_api, screen_name=obiekt2, max_results=step, po_ile=100)

    tweet_text1 = [status['text'] for status in tweets1]
    words1 = [w for t in tweet_text1 for w in t.split()]
    hashtags1 = [hashtag['text'] for status in tweets1 for hashtag in status['entities']['hashtags']]
    tweet_text2 = [status['text'] for status in tweets2]
    words2 = [w for t in tweet_text2 for w in t.split()]
    hashtags2 = [hashtag['text'] for status in tweets2 for hashtag in status['entities']['hashtags']]

    tvp = lexical_diversity(words1)*100
    tvn = lexical_diversity(words2)*100
    tvp_list.append(tvp)
    tvn_list.append(tvn)
    for label, data in (('Słowo', words2), ('Hashtag', hashtags2)):
        pt = PrettyTable(field_names=[label, 'Liczba'])
        c = Counter(data)
        [pt.add_row(kv) for kv in c.most_common()[:100]]
        pt.align[label], pt.align['Liczba'] = 'l', 'r'
        print(pt)

    for label, data in (('Słowo', words1), ('Hashtag', hashtags1)):
        pt = PrettyTable(field_names=[label, 'Liczba'])
        c = Counter(data)
        [pt.add_row(kv) for kv in c.most_common()[:100]]
        pt.align[label], pt.align['Liczba'] = 'l', 'r'
        print(pt)


kroki_str = ['100','200','300','400','500','600','700','800','900','1000']

n_groups = len(kroki_str)
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
rects1 = plt.bar(index, tvp_list, bar_width,
alpha=opacity,
color='r',
label='@tvp_info')
rects2 = plt.bar(index + bar_width, tvn_list, bar_width,
alpha=opacity,
color='b',
label='@tvn24')

plt.xlabel('Liczba postów wstecz poddanych badaniu')
plt.ylabel('Różnorodność leksykalna w postach[%]')
plt.title('Różnorodność leksykalna @tvp_info vs @tvn24 - portal Twitter.com')
plt.xticks(index + bar_width, kroki_str)
plt.legend()
plt.tight_layout()
plt.show()




