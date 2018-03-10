import praw             # Python Reddit API Wrapper
import pandas as pd     # To handle data
import numpy as np      # For number computing

from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime

from textblob import TextBlob
import re

print('\n*** SCRIPT STARTED AT {} *** \n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


reddit = praw.Reddit(client_id = 'gGQNJa_LowQ8Zg',
                        client_secret = 'oAZBSWY8yxuC6EaRUivIdp9gaM0',
                        user_agent = 'match_thread_sa_agent')

sub = 'reddevils' #input('Enter subreddit: ')
subreddit = reddit.subreddit(sub)

#Palace 828ner
#Chelsea 804id0
#Sevilla 7z87nq
#Spurs 7uckkc
#Arsenal 7h3qsg
#Liverpoo 83erhf
submission_input = '83erhf' #'83fq8m'#input('Enter submission id: ')
submission = reddit.submission(id = submission_input)

print('Title: {}, Ups: {}, Downs: {}'.format(
                                            submission.title,
                                            submission.ups,
                                            submission.downs))
submission.comments.sort = 'top'
submission.comments.replace_more(limit = None, threshold = 0)
print('Total comments: {}'.format(submission.num_comments))

data = pd.DataFrame(data = [comment.body for comment in submission.comments.list()], columns = ['Text'])

data['Length'] = np.array([len(comment.body) for comment in submission.comments.list()])
#data['Created'] = np.array([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(comment.created_utc)) for comment in submission.comments.list()])
data['Created'] = np.array([pd.to_datetime(comment.created_utc, unit = 's') for comment in submission.comments.list()])
data['Score'] = np.array([comment.score for comment in submission.comments.list()])
#print('Average length of comments is {}'.format(np.mean(data['Length'])))

#tlen = pd.Series(data = data['Length'].values, index = data['Created'])
#tlen.plot(figsize = (15,5), color = 'b', legend = True, label = 'Length', kind = 'area')
'''
tlen = pd.Series(data = data['Length'].values, index = data['Created'])
tlen.sort_index(axis = 0).plot(figsize = (15,5), 
                          color = 'b', 
                          legend = True, 
                          label = 'Length', 
                          stacked = False,
                          kind = 'bar')
'''
def clean_comment(comment):
    '''
    Utility function to clean comment of links and special characters using regex
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

def get_comment_sentiment(comment):
    '''
    Utility function to analyze and return sentiment of comment
    '''
    analysis = TextBlob(comment)
    return analysis.sentiment.polarity

def get_comment_polarity(comment):
    '''
    Utility function to analyze and return sentiment of comment
    '''
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    elif analysis.sentiment.polarity < 0:
        return -1

data['Sentiment'] = np.array( [get_comment_sentiment(comment) for comment in data['Text']] )
data['SA'] = np.array( [get_comment_polarity(comment) for comment in data['Text']] )

#display(data.head(5))
print('Average sentiment: {0:.3f}'.format(np.mean(data['Sentiment'])))
#.resample('3T').mean()
tscore = pd.Series(data = data['Sentiment'].values, index = data['Created'])
tscore.sort_index(axis = 0).plot.area(figsize = (100,5), 
                          color = 'r', 
                          legend = True,
                          stacked = False,
                          label = 'Comment Sentiment')


pos_comments = [ comment for index, comment in enumerate(data['Text']) if data['SA'][index] > 0 ]
neut_comments = [ comment for index, comment in enumerate(data['Text']) if data['SA'][index] == 0 ]
neg_comments = [ comment for index, comment in enumerate(data['Text']) if data['SA'][index] < 0 ]

print("Percentage of positive comments: {0:.2f}%".format(len(pos_comments)*100/len(data['Text'])))
print("Percentage of neutral comments: {0:.2f}%".format(len(neut_comments)*100/len(data['Text'])))
print("Percentage of negative comments: {0:.2f}%".format(len(neg_comments)*100/len(data['Text'])))

''' print('Positive comments: {}'.format((data['SA'] == 1).sum()))
print('Neutral comments: {}'.format((data['SA'] == 0).sum()))
print('Negative comments: {}'.format((data['SA'] == -1).sum())) '''

goals = np.array([pd.to_datetime('14:52:00') ])

plt.plot(data['Created'].values, [np.mean(data['Sentiment'])]*len(data['Created'].values), 
         linestyle = '--', label = 'Average Sentiment')

xlocator = mdates.MinuteLocator(byminute=[0,10,20,30,40,50], interval = 1)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gca().xaxis.set_major_locator(xlocator)
plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator())
plt.xlabel('Timestamp')
plt.ylabel('Sentiment')
plt.xticks(rotation='vertical')
plt.legend()
#plt.figsize(50, 20)
#plt.show()
plt.savefig('PLOT-{}.png'.format(str(submission.title).replace(" ", "_")), dpi = 500)

print('\n*** SCRIPT FINISHED AT {} *** \n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))