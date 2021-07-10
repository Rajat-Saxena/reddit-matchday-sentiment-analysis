import requests
import os
import json
import praw
import pandas as pd
from textblob import TextBlob
import datetime
import matplotlib.pyplot as plt 
import base64
import re
import matplotlib.dates as mdates

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_comment_sentiment(comment):
    cleaned_comment = clean_comment(comment)
    analysis = TextBlob(cleaned_comment)
    return analysis.sentiment.polarity

def clean_comment(comment):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

print(f"{get_time()} Begin initialization.")
start_time = get_time()

# Read config file
with open("config.json") as f:
    config = json.load(f)

# Set parameters from config
client_secret = base64.b64decode(config["reddit_client_secret"].encode("utf-8")).decode("utf-8")
client_id = base64.b64decode(config["reddit_client_id"].encode("utf-8")).decode("utf-8")
reddit_username = base64.b64decode(config["reddit_username"].encode("utf-8")).decode("utf-8")
reddit_password = base64.b64decode(config["reddit_password"].encode("utf-8")).decode("utf-8")
user_agent = base64.b64decode(config["app_agent"].encode("utf-8")).decode("utf-8")

# Create Reddit instance using PRAW
reddit = praw.Reddit(
    user_agent=user_agent,
    client_id=client_id,
    client_secret=client_secret,
    username=reddit_username,
    password=reddit_password,
)

# Set up values for submission
subreddit = "reddevils"
submission_id = "7uckkc" # "nlobbq" # "nj97ic" # input("Enter submission id: ")
kickoff_time = "2018-01-31 20:00:00" # input("Enter kick-off time (yyyy-mm-dd hh:mm) UTC: ")

# Get instance of submission
submission = reddit.submission(id=submission_id)

# Create empty dataframe
df = pd.DataFrame()

print(f"{get_time()} Reached checkpoint 0: Initialization done. Starting comments explosion.")

# Loop over all comments in the submission
submission.comments.replace_more(limit=None)
print(f"{get_time()} Reached checkpoint 1: All nested comments have been exploded.")

for comment in submission.comments.list():
    df = df.append({
        "subreddit": subreddit,
        "submission_id": submission.id,
        "submission_created_utc": pd.to_datetime(submission.created_utc, unit = "s"),
        "submission_title": submission.title,
        "match_kickoff_time": pd.to_datetime(kickoff_time),
        "comment_text": comment.body,
        "comment_created_utc": pd.to_datetime(comment.created_utc, unit = "s").floor('min'),
        "minutes_elapsed": (pd.to_datetime(comment.created_utc, unit = "s") - pd.to_datetime(kickoff_time)).to_timedelta64().astype('timedelta64[m]')
    }, ignore_index=True)

print(f"{get_time()} Reached checkpoint 2: DataFrame created.")

# Filter comments that were posted at most 3 hours past kick-off
df = df[df['minutes_elapsed'] < pd.Timedelta(180,'m')]

# Calculate sentiment of every comment and save into a new column
df["sentiment"] = df["comment_text"].apply(lambda x: get_comment_sentiment(x))
# Calculate sentiment polarity of every comment and save into a new column
df["sentiment_polarity"] = [1 if x > 0 else (-1 if x < 0 else 0) for x in df["sentiment"]]

# Store some metadata
num_total_comments = df.shape[0]
num_positive_comments = df[df["sentiment"] > 0].shape[0]
perc_positive_comments = round(((num_positive_comments / num_total_comments) * 100), 2)
num_negative_comments = df[df["sentiment"] < 0].shape[0]
perc_negative_comments = round(((num_negative_comments / num_total_comments) * 100), 2)
average_sentiment = df["sentiment"].mean()

print(f"{get_time()} Reached checkpoint 3: Calculated sentiment of every comment and captured metadata.")

df.to_csv("data.csv")
print(f"{get_time()} Reached checkpoint 4: Saved data to a local file.")

df2 = df.groupby(["comment_created_utc"]).mean().reset_index()
df2["positive_sentiment"] = [x if x > 0 else 0 for x in df2["sentiment"]]
df2["negative_sentiment"] = [x if x < 0 else 0 for x in df2["sentiment"]]
print(f"{get_time()} Reached checkpoint 5: Grouping done based on sentiment.")

fig, ax = plt.subplots(1, figsize=(35, 3))
plt.plot(df2["comment_created_utc"], df2["positive_sentiment"], label = "Positive Sentiment", color="green")
plt.plot(df2["comment_created_utc"], df2["negative_sentiment"], label = "Negative Sentiment", color="red")
plt.plot(df2["comment_created_utc"], pd.Series(0, index=df2.index), color="yellow")
xlocator = mdates.MinuteLocator(byminute=[0,10,20,30,40,50], interval = 1)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
plt.gca().xaxis.set_major_locator(xlocator)
plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator())
plt.xlabel("Timestamp")
plt.ylabel("Sentiment")
# plt.xticks(rotation="vertical")
plt.legend()

plot_name = (str(submission.title)).replace("Match Thread", "").replace("[", "").replace("]", "").replace(" ", "")[0:30]
plt.savefig(f"images/PLOT-{plot_name}.png", dpi = 500)

print(f"{get_time()} Reached checkpoint 6: Graph plotted and saved to disk.")

print(f"{get_time()} Total comments: {num_total_comments}; positive comments: {num_positive_comments} ({perc_positive_comments}%); negative comments: {num_negative_comments} ({perc_negative_comments}%)")