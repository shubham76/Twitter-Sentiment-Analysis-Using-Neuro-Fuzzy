import re
import nn3
import numpy as np
from nn3 import NeuralNetwork

def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')

    return tweet


positive = []
negative = []



with open("positive_keywords.txt") as f:
    for line in f:
        line=line.strip()
        positive.append(line)

with open("negative_keywords.txt") as f:
    for line in f:
        line=line.strip()
        negative.append(line)

data=[]
output=[]

with open("data.txt") as f:
	for line in f:
		line=line.strip("\n")
		data.append(line)

with open("target.txt") as f:
	for line in f:
		line=line.strip("\n")
		output.append(line)

posCnt=0
negCnt=0
idx=0

print len(data)
print len(output)
big=[]
op=[]
for tweet in data:
	tweet=processTweet(tweet)
	tweet=re.sub(r'[^\w\s]','',tweet)
	#print tweet
	tweet=tweet.split()
	posCnt=0
	negCnt=0
	small=[]
	for word in tweet:
		word=word.strip('\'"?,.!')
		word=word.lower()
		if word in positive:
			posCnt+=1
		if word in negative:
			negCnt+=1
	print posCnt
	print negCnt
	small.append(posCnt)
	small.append(negCnt)
	big.append(small)
	target=output[idx]
	if target=="positive":
		op.append(1)
	elif target=="negative":
		op.append(-1)
	else:
		op.append(0)
	print target
	idx=idx+1


nn = NeuralNetwork([2,2,1])

X = np.array(big)

y = np.array(op)

nn.fit(X, y)

print("Enter a statement")
stmt=raw_input()
tweet=processTweet(stmt)
tweet=re.sub(r'[^\w\s]','',tweet)
#print tweet
tweet=tweet.split()
posCnt=0
negCnt=0
small=[]
for word in tweet:
	word=word.strip('\'"?,.!')
	word=word.lower()
	if word in positive:
		posCnt+=1
	if word in negative:
		negCnt+=1
print posCnt
print negCnt
small.append(posCnt)
small.append(negCnt)

ans=nn.predict(small)
if ans >= 0.3:
	print("Positive")
elif ans<=-0.3:
	print("Negative")
else:
	print("Neutral")
print(ans)
