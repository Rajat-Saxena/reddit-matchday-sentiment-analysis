# Reddit Matchday Sentiment Analysis
Python script to analyze sentiments of comments made by Redditors during a football match on a desired subreddit and submission.

The script uses [PRAW](https://praw.readthedocs.io) to connect to Reddit and pull comments from specified submission. [TextBlob](https://textblob.readthedocs.io/en/dev/) is used for text processing.

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

## Analysis
So I will start by analyzing the biggest game in English football, the North-West derby - **Manchester United vs Liverpool**. The match was played on March 10, 2018 at 12:30 UTC. Manchester United led in the first half through two goals by Marcus Rashford in the 14th and 24th minute. Liverpool pulled one back via an Eric Bailly own goal after 66 minutes.

There are 3,515 user comments in the [match thread](https://www.reddit.com/r/reddevils/comments/83erhf/match_thread_manchester_utd_vs_liverpool/) on [/r/RedDevils](https://www.reddit.com/r/reddevils/). Here's the analysis:

* Average sentiment: 0.042
* Percentage of positive comments: 34.52%
* Percentage of neutral comments: 42.20%
* Percentage of negative comments: 23.28%
* Plot:  
![Manchester United vs Liverpool](/images/PLOT-[Match_Thread]_Manchester_Utd_vs_Liverpool.png)
Format: ![Manchester United vs Liverpool]()
* Match Result: Manchester United 2-1 Liverpool
* Clearly, the sentiment is positive, especially towards and after the end of the game.


Let me now compare with another game, **Tottenham Hotspur vs Manchester United**. The match was played on January 31, 2018 at 20:00 UTC. Christian Eriksen scored 30 seconds into the match! Phil Jones scored an own goal in the 28th minute.

There are 4,313 user comments in the [match thread](https://www.reddit.com/r/reddevils/comments/83erhf/match_thread_manchester_utd_vs_liverpool/) on [/r/RedDevils](https://www.reddit.com/r/reddevils/). Here's the analysis:

* Average sentiment of comments: -0.020
* Percentage of positive comments: 33.00%
* Percentage of neutral comments: 31.10%
* Percentage of negative comments: 35.91%
* Plot:  
![Tottenham Hotspur vs Manchester United](/images/PLOT-[Match_Thread]_Tottenham_vs_Manchester_Utd.png)
Format: ![Tottenham Hotspur vs Manchester United]()
* Match Result: Tottenham Hotspur 2-0 Manchester United
* As is evident from the high concentration of negative sentiments, it was a game to forget. 
