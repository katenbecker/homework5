from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk
nltk.download('stopwords')


## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Tuesday 2-3:30
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET



#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching

CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {'screen_name': username, 'count': num_tweets}
        response = requests.get(base_url, params, auth = auth)

        CACHE_DICTION[unique_ident] = json.loads(response.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]




#Code for Part 1:Get Tweets

base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {'screen_name': username, 'count': num_tweets}
response = requests.get(base_url, params, auth = auth)
responsee = json.loads(response.text)
responsed = json.dumps(responsee, indent = 5)
#print(responsed)
#res_list = json.dumps(response)
#print(res_list)


#fw = open('tweet.json', 'w')
#fw.write(responsed)
#fw.close()


make_request_using_cache(base_url, params = {'username' : username, 'num_tweets': num_tweets})

#Code for Part 2:Analyze Tweets
#for x in responsed:
#	tokens = nltk.word_tokenize(x['text'])
#print 
listt = ""
for x in responsee:
	listt += x['text']
#print(listt)
tokens = nltk.word_tokenize(listt)
fdist = nltk.FreqDist(tokens)

abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']



from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
 
 
stop_words = set(stopwords.words('english'))
 
filtered_sentence = []
 

#for w in fdist:
for w in tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

filtered_sentence2 = []

for w in filtered_sentence:
	if w[0] in abc:
		filtered_sentence2.append(w)

filtered_sentence3 = []

for w in filtered_sentence2:
	if w[:4] != "http":
		filtered_sentence3.append(w)

filtered_sentence4 = []

for w in filtered_sentence3:
	if w[:5] != "https":
		filtered_sentence4.append(w)

filtered_sentence5 = []

for w in filtered_sentence4:
	if w[:2] != "RT":
		filtered_sentence5.append(w)

fdist2 = nltk.FreqDist(filtered_sentence5)
mcommon = fdist2.most_common(5)

print(mcommon)














if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()