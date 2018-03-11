# Reddit Matchday Sentiment Analysis
Python script to analyze sentiments of comments made by Redditors during a football match on a desired subreddit and submission.

The script uses [PRAW](https://praw.readthedocs.io) to connect to Reddit and pull comments from specified submission.

## Preface
This project was inspired from the comments I read during matches on Reddit. There is always such a stark contrast in the opinions of people, irrespective of a positive or negative result.

By performing a sentiment analysis, I am hoping to identify a correlation between match results and overall sentiment of the comments.

## FAQ
**Question:** What all information is pulled from Reddit?
**Answer:** Using PRAW, the script pulls *title of submission*, *submission upvotes*, *submssion downvotes*, and *all the comments* along with *length of comment* and *timestamp of comment*.

**Question:** Which subreddit can the script analyze?
**Answer:** Initially I had written the script for */r/RedDevils*, but now it is a general script that will prompt user for desired subreddit and submission.

**Question:** Which information should the end user have?
**Answer:** The end user will need to enter *subreddit*, *submission id*, and *kick off time*.

**Question:** What will the script return?
**Answer:** The script returns *average sentiment of comments*, *percentage of positive, neutral and negative comments*, and a *line graph plotting sentiment over the course of the match*. 
