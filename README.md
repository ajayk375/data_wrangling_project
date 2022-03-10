CONTENTS OF THE FILE
=======================
* Introduction
* Requirements
* What's Included
* File Description
* Summary of results
* Licensing, Author(s) and Acknowledgement(s)


Introduction
-------------
This project is to showcase the Data Wrangling concepts on Twitter Data and as part of that following steps will be performed 
on the Twitter Data:

Step 1: Gathering data
Step 2: Assessing data
Step 3: Cleaning data
Step 4: Storing data
Step 5: Analyzing, and visualizing data
Step 6: Reporting

As part of this exercise we also want to find out the top 10 favourite dogs based on retweets and favourite count.


Requirements
-------------
To analyze and prepare data we have used Jupyter Notebook and following libraries:
Pandas
Numpy
Seaborn
Matplotlib

What's Included
----------------
1. File: wrangle_act.ipynb
2. File: wrangle_act.html 
3. File: act_report.pdf
4. File: README.md
5. File: twitter_archive_enhanced.csv
6. File: image_predictions.tsv
7. File: tweet_json.txt
8. File: twitter_archive_master.csv

File Description
-----------------
File: wrangle_act.ipynb - Jupyter notebook where whole data wrangling 
File: wrangle_act.html - This file is the html version of Jupyter notebook.
File: act_report.pdf - Documentation of analysis and insight on data
File: README.md - Contains information about the project and GitHub Repo structure.
File: twitter_archive_enhanced.csv - Downloaded from provided URL by Udacity
File: image_predictions.tsv - Downloaded from provided URL by Udacity
File: tweet_json.txt - Downloaded tweets data using Tweepy (Tweet ID provided from twitter_archive_enhanced.csv)
File: twitter_archive_master.csv - Final master data prepared by joing 3 files

Summary of results
--------------------
Here is the image showing top 10 Dog Breed based on number of tweets -

![Top 10 Dogs - Number of Tweets](https://github.com/ajayk375/data_wrangling_project/blob/main/Screenshot%202022-03-10%20at%2017.45.40.png)

Price of the listings are consistently high from June until December, and price is at peak during December and cheapest during January. This clearly visible
from the following plot -

![Top 10 Dogs - Aggregate Fav Count](https://github.com/ajayk375/data_wrangling_project/blob/main/Screenshot%202022-03-10%20at%2017.46.24.png)

On both the counts Golden Retriever:

![Golden Retriever](https://github.com/ajayk375/data_wrangling_project/blob/main/golen_retriever.jpeg)


Licensing, Author(s) and Acknowledgement(s)
--------------------------------------------
Licensing: Open Source and available in public GitHub Repository - https://github.com/ajayk375/data_wrangling_project

Author: Ajay Kumar

Acknowledgements: Udacity (Citizen Data Scientist)
