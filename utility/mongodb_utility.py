# -*- coding: utf-8 -*-
"""
Contains mongodb utility functions to display various components of the database
Referenced by news_server and news_scrapper module

"""

from pymongo import MongoClient
import pymongo.errors
from bson.json_util import dumps
from datetime import date

def create_database_connection():
	"""
	return: collection object referencing the database 'Articles'
	"""
	try:
		client=MongoClient('localhost',27017)
	except Exception as e:
		raise e
	else:
		db = client['News']
		collection=db['Articles']
		collection.create_index("title",unique=True)
		return collection


def insert_article(collection,article):
	"""
	@params collection: collection object referencing the database 'Articles'
	@params article: article dict containing various fields like process_date, story_date, story_time, source, category, body, title, topics
	"""
	try:
		article_id = collection.insert_one(article).inserted_id
	except pymongo.errors.DuplicateKeyError:
		pass


def get_all_documents_in_collection():

	cursor=create_database_connection()
	for document in cursor.find():
		print(document)


def get_articles_from_source_on_date(collection,source,process_date):
	"""
	@params collection: collection object referencing the database 'Articles'
	@params source: newspaper source
	@process_date: process date of the newspaper

	return : cursor containing results
	"""
	cursor=collection.aggregate([{ "$match": { "process_date": process_date ,"source":source} },{"$group": {"_id": "$source","total": { "$sum": 1 }}}] )
	return dumps(cursor)


def get_articles_from_source_on_current_date(collection):
	"""
	@params collection: collection object referencing the database 'Articles'

	return : cursor containing results
	"""
	current_date=date.today().strftime("%Y-%m-%d")
	cursor=collection.aggregate([{"$match": { "process_date": {"$eq": current_date} }},{"$group" : {"_id":"$source", "count":{"$sum":1}}}])
	return dumps(cursor)


def get_articles_from_source_on_date_over_timeperiod(collection, source, process_date, story_time):
	"""
	@params collection: collection object referencing the database 'Articles'
	@params source: newspaper source
	@process_date: process date of the newspaper
	@story_time: time to filter stories based on story_time

	return : cursor containing results
	"""
	cursor=collection.aggregate([{"$match": {"source": {"$eq": source},"process_date":{"$lte": process_date},"story_time":{"$lte": story_time}}},{"$count": "articles"}])
	return dumps(cursor)


def list_articles_on_date(collection,process_date):
	"""
	@params collection: collection object referencing the database 'Articles'
	@process_date: process date of the newspaper

	return : cursor containing results
	"""
	cursor=collection.aggregate([{"$match": { "process_date": {"$eq": process_date} }},{"$group" : {"_id":"$category", "count":{"$sum":1}}}])
	return dumps(cursor)


def list_articles_from_source_categorically(collection,source):
	"""
	@params collection: collection object referencing the database 'Articles'
	@params source: newspaper source

	return : cursor containing results
	"""
	cursor=collection.aggregate([{"$group": {"_id": {"source" : source,"category":"$category"}, "total":{"$sum" :1}}},{"$project" :{"source" :"$_id.source","category" :"$_id.category", "total" : "$total", "_id":0}},{ "$sort": { "source":1,"total":1 }}])
	return dumps(cursor)


def list_news_sources(collection):
	"""
	@params collection: collection object referencing the database 'Articles'

	return : cursor containing results
	"""
	cursor=collection.aggregate([{"$group" : {"_id":"$source", "count":{"$sum":1}}}])
	return dumps(cursor)


def display_article_titles(collection):
	"""
	@params collection: collection object referencing the database 'Articles'

	return : cursor containing results
	"""
	cursor=collection.aggregate([{"$group": {"_id": {"title":"$title"}, "total":{"$sum" :1}}},{"$project" :{"title" :"$_id.title", "total" : "$total", "_id":0}}])
	return dumps(cursor,default=dict)


def display_article_content(collection,article_title):
	"""
	@params collection: collection object referencing the database 'Articles'
	@params article_title: string containing the article title

	return : cursor containing results
	"""
	cursor=collection.find({ "title":article_title })
	#"sample title":'Infinity Pool The perfect summer cocktail recipe'
	return dumps(cursor)


def print_cursor_objects(cursor):

	for doc in cursor:
		print(doc)