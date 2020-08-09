# Newspaper-Management

### Objective:

The objective is to design and develop small working prototype of centralized newsfeed
system.

### Description:

One needs to design a simple newsfeed management system. The system should take simple
text file containing news sites such as follows:
  - http://in.finance.yahoo.com
  - https://www.reuters.com/places/india
  - https://timesofindia.indiatimes.com/

### Goal:
The goal is to extract individual news and store these feeds as JSON files by date. The JSON
file should contain fields such as current_date, story_date, story_time, body, title, source,
story_id  
Some fields are described here, but please feel free to add as you see fit:
  - current_date - process date
  - author - article author
  - story_date - extract story date from article
  - story_time - extract story time from article (if possible)
  - body - story text (cleaned text)
  - title - story title
  - source - newspaper (give abbreviations to newspaper)
  - category - news | rss | …
  - topics - topics from document
  
  ### Deliverable:
A stand-alone application packaged with documentation, which allows user to run code via
shell script in following manner.  

```sh
news_feed.sh - containing
python news_scrapper.py —root_dir=<output directory> —source_list=<file containing news sites>
```
For flask server component, please make sure that it’s minimal and you can showcase your
knowledge of REST APIs, etc…

```sh
./news_server.sh
```

One can check REST API calls using either curl or Postman
