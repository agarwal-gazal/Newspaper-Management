# -*- coding: utf-8 -*-
"""
Containss the necessary utilities for building newspaper source, downloading and loading the articles

Referenced by news_scrapper module
"""
import newspaper
from multiprocessing import Pool
from newspaper import Article
import json
from newspaper import news_pool
import datetime
import os
import re
from urllib.parse import urlparse
from utility.mongodb_utility import *


def build_newspaper(list_of_newspaper_url,output_dir):
	"""
	@params list_of_newspaper_url: list containing the various newspaper URLs
	@params output_dir: folder to store the json generated for articles
	"""
	
	#print('inside build_newspaper for ',list_of_newspaper_url)

	paper_obj=['paper'+str(i) for i in range(len(list_of_newspaper_url)) ] #builds paper object list

	for i in range(len(list_of_newspaper_url)):
		paper_obj[i] = newspaper.build(list_of_newspaper_url[i],memoize_articles=False) #builds newspaper for each newspaper

	news_pool.set(paper_obj, threads_per_source=3) #news_pool to multi-thread article downloads

	for i in range(len(list_of_newspaper_url)):
		print('calling convert_article_to_json')
		convert_article_to_json(paper_obj[i],output_dir) 


def convert_article_to_json(paper_object,output_dir):
	"""
	@params paper_obj: paper object containing the newspaper build representing a newspaper source
	@params output_dir: folder to store the json generated for articles
	"""
	print('inside convert_article_to_json')

	article_url=[[article.url,paper_object.brand,output_dir] for article in paper_object.articles] #get the article URLs for a particular source

	#multiprocessing the various article URLs simultaneously

	p = Pool(10)
	p.map(get_article_content, article_url)

	p.terminate()
	p.join()

	
def get_article_content(feed_url):
	"""
	@params feed_url: article URL to download and explore
	"""

	print('inside get_article_content for',feed_url)

	article={}
	regex = r"([.,;:''\"!@#$%^&*()?`~/\n\?])"

	try:
		#download the article and parse it
		content=Article(url=feed_url[0],language='en')
		content.download()
		content.parse()
		content.nlp()

	except Exception as e:
		print(e)

	else:
		#create an article dict to store relevant information about the article
		#process_date, story_date, story_time, category,authors, title,text, topics, source
		
		article['process_date']=datetime.date.today().strftime("%Y-%m-%d")
		if content.publish_date:
			article['story_date']=content.publish_date.strftime("%Y-%m-%d")
			article['story_time']=content.publish_date.strftime("%H:%M:%S")
		if urlparse(feed_url[0]).path:
			article['category']=urlparse(feed_url[0]).path.split('/')[1]
		article['authors'] = content.authors
		article['title']=re.sub(regex, "", content.title, 0)
		article['text']=re.sub(regex, "", content.summary, 0)
		article['topics']=content.keywords
		article['source']=feed_url[1][:3]
		print(article)
		validate_article(article)
		dump_article_to_json(article,feed_url[2])


def validate_article(article):
	"""
	Creates a database object and calls mongodb utility to insert article to database
	@params article: article dict
	"""
	collection=create_database_connection()
	insert_article(collection,article)


def dump_article_to_json(article_dict,output_dir):
	"""
	@params article_dict:article dict
	@output_dir: folder location to store  the output json
	"""
	dict_name=datetime.date.today().strftime("%Y-%m-%d")

	if not os.path.exists(output_dir+dict_name):
		os.makedirs(output_dir+dict_name)
	try:
		with open(os.path.join(output_dir,dict_name,article_dict['title']+'.json'),'w') as fp:
			json.dump(str(article_dict),fp)

	except Exception as e:
		print(e)
		pass