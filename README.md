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
We will look at 2 games to demonstrate this application.

First, the Manchester derby. Manchester United traveled to the Etihad Stadium to face Manchester City on March 7, 2021. **Manchester United won 2-0 on the night** with goals from Bruno Fernandes and Luke Shaw. 

There are 5,013 user comments in the match thread on [/r/RedDevils](https://www.reddit.com/r/reddevils/). Here's the analysis:

* Percentage of positive comments: 34.27%
* Percentage of negative comments: 24.90%
* Plot:  
![Manchester Ciry vs Manchester United](images/PLOT-ManchesterCityvsManchesterUnited.png)
* Match Result: Manchester City 0-2 Manchester United
* This match was one of the good ones from the season.


Let me now compare with another game, the Europa League final between Manchester United and Villareal. The match was played on May 26, 2021. Manchester United lost the match on penalties after both teams were tied in normal and extra time.

There are a whopping 15,571 user comments in the match thread on [/r/RedDevils](https://www.reddit.com/r/reddevils/). Here's the analysis:

* Percentage of positive comments: 26.74%
* Percentage of negative comments: 31.43%
* Plot:  
![Villareal vs Manchester United](images/PLOT-VillarrealvsManchesterUnited.png)
* Match Result: Villareal 1-1 Manchester United (Villareal won 11-10 on penalties)
* Clearly, it was a game to forget.

### Some other plots

* Manchester United 2-1 Liverpool (2018)
![Manchester United vs Liverpool](images/PLOT-ManchesterUtdvsLiverpool.png)

* Tottenham Hotspurs 2-0 Manchester United (2018)
![Tottenham Manchester United](images/PLOT-TottenhamvsManchesterUtd.png)

* Wolves 1-2 Manchester United (2021)
![Wolves vs Manchester United](images/PLOT-WolvesvsManchesterUnited.png)
