import praw                         # Python Reddit API Wrapper
import pandas as pd                 # To handle data
import numpy as np                  # For number computing

import matplotlib.pyplot as plt     # For plotting data
import matplotlib.dates as mdates   # To handle timestamps on x-axis
import datetime                     # For datetime manipulation

from textblob import TextBlob       # TextBlob provides a trained analyzer
import re                           # Regular expression used to clean comments

print('\n*** Script started at {} *** \n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

reddit = praw.Reddit(client_id = 'gGQNJa_LowQ8Zg',
                        client_secret = 'oAZBSWY8yxuC6EaRUivIdp9gaM0',
                        user_agent = 'match_thread_sa_agent')

sub = input('Enter subreddit: ')
submission_input = input('Enter submission id: ')
kickoff_time = input('Enter kick-off time (yyyy-mm-dd hh:mm) UTC: ')

print('Connecting to Reddit...')
subreddit = reddit.subreddit(sub)
submission = reddit.submission(id = submission_input)

print('Connection to Reddit established.')
# Manipulating kickoff_time to plot comments 5 mins before and after match
# Assumption - a complete match takes 2 hours
kickoff_time = pd.to_datetime(kickoff_time)
full_time = kickoff_time + datetime.timedelta(hours = 2, minutes = 5)
kickoff_time = kickoff_time + datetime.timedelta(minutes = -5)

print('Title: {}, Ups: {}, Downs: {}'.format(
                                            submission.title,
                                            submission.ups,
                                            submission.downs))

print('Pulling all comments in submission...')
submission.comments.sort = 'top'
submission.comments.replace_more(limit = None, threshold = 0)
print('Total comments in submission: {}'.format(submission.num_comments))

data = pd.DataFrame(data = [comment.body for comment in submission.comments.list()], columns = ['Text'])
data['Length'] = np.array([len(comment.body) for comment in submission.comments.list()])
data['Created'] = np.array([pd.to_datetime(comment.created_utc, unit = 's') for comment in submission.comments.list()])
data['Score'] = np.array([comment.score for comment in submission.comments.list()])
#print('Average length of comments is {}'.format(np.mean(data['Length'])))

def clean_comment(comment):
    '''
    Utility function to clean comment of links and special characters using regex
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

def get_comment_sentiment(comment, op):
    '''
    Utility function to analyze and return sentiment of comment
    '''
    analysis = TextBlob(comment)

    if op == 1:     # Return sentiment of comment
        return analysis.sentiment.polarity
    else:           # Return value based on polarity of comment
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        elif analysis.sentiment.polarity < 0:
            return -1

print('Analyzing sentiment of comments...')
data['Sentiment'] = np.array( [get_comment_sentiment(comment, 1) for comment in data['Text']] )
data['SA'] = np.array( [get_comment_sentiment(comment, 2) for comment in data['Text']] )

print('Average sentiment of comments: {0:.3f}'.format(np.mean(data['Sentiment'])))

pos_comments = [ comment for index, comment in enumerate(data['Text']) if data['SA'][index] > 0 ]
neut_comments = [ comment for index, comment in enumerate(data['Text']) if data['SA'][index] == 0 ]
neg_comments = [ comment for index, comment in enumerate(data['Text']) if data['SA'][index] < 0 ]

print("Percentage of positive comments: {0:.2f}%".format(len(pos_comments)*100/len(data['Text'])))
print("Percentage of neutral comments: {0:.2f}%".format(len(neut_comments)*100/len(data['Text'])))
print("Percentage of negative comments: {0:.2f}%".format(len(neg_comments)*100/len(data['Text'])))

# Plot line graph of comments sentiments throughout the match
tscore = pd.Series(data = data['Sentiment'].values, index = data['Created'])
tscore.sort_index(axis = 0).plot(figsize = (50,5),
                          color = 'r',
                          legend = True,
                          stacked = False,
                          label = 'Comment Sentiment')

plt.plot(data['Created'].values, [np.mean(data['Sentiment'])]*len(data['Created'].values),
         linestyle = '--', label = 'Average Sentiment')

xlocator = mdates.MinuteLocator(byminute=[0,10,20,30,40,50], interval = 1)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gca().xaxis.set_major_locator(xlocator)
plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator())
plt.xlabel('Timestamp')
plt.ylabel('Sentiment')
plt.xticks(rotation='vertical')
plt.xlim(kickoff_time, full_time)
plt.legend()
plt.savefig('images/PLOT-{}.png'.format(str(submission.title).replace(" ", "_")), dpi = 500)

print('\n*** Script completed at {} *** \n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
