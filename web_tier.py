# -*- coding: utf-8 -*-
"""
Contains flask resources to display various components of the database
Use Postman or Curl for sending the requests

"""

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from utility.mongodb_utility import *
import json

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})


class GetArticlesOnDate(Resource):
    # display the articles which for a source on a particular process date
    def get(self):
        """
        @params source: newspaper source
        @params process_date: process date of the newspaper

        return: jsonified response
        """
        source = request.args.get('source', None)
        process_date = request.args.get('process_date', None)
        collection=create_database_connection()
        response = get_articles_from_source_on_date(collection, str(source), str(process_date))
        return json.loads(response)


class GetArticlesOverTimePeriod(Resource):
    # display the articles which for a source on a particular process date over a time
    def get(self):
        """
        @params source: newspaper source
        @params process_date: process date of the newspaper
        @story_time: time to filter stories based on story_time

        return: jsonified response
        """
        source = request.args.get('source', None)
        process_date = request.args.get('process_date', None)
        story_time = request.args.get('story_time', None)
        collection=create_database_connection()
        response = get_articles_from_source_on_date_over_timeperiod(collection, str(source), str(process_date), str(story_time))
        return json.loads(response)


class ListArticlesOnDate(Resource):
    #display articles based on category for a particular date
    def get(self):
        """
        @params process_date: process date of the newspaper

        return: jsonified response
        """
        process_date = request.args.get('process_date', None)
        collection=create_database_connection()
        response = list_articles_on_date(collection, str(process_date))
        return json.loads(response)


class ListArticlesFromNewsSource(Resource):
    #display articles based on source
    def get(self):
        """
        @params source: newspaper source

        return: jsonified response
        """
        source = request.args.get('source', None)
        collection=create_database_connection()
        response = list_articles_from_source_categorically(collection,source)
        return json.loads(response)


class ListNewsSources(Resource):
    #displays the list of sources available
    def get(self):
        """
        return: jsonified response
        """
        collection=create_database_connection()
        response=list_news_sources(collection)
        return json.loads(response)


class ListNewsToday(Resource):
    #summarizes the list of news categorically captured by various sources on the current date
    def get(self):
        """
        return: jsonified response
        """
        collection=create_database_connection()
        response=get_articles_from_source_on_current_date(collection)
        return json.loads(response)


class ListArticleTitles(Resource):
    #lists the article title from news source
    def get(self):
        """
        return: jsonified response
        """
        source = request.args.get('source', None)
        collection=create_database_connection()
        response = display_article_titles(collection)
        return json.loads(response)


class ListArticle(Resource):
    #lists content of article corresponding to article title
    def get(self):
        """
        @params article_title: article title

        return: jsonified response
        """
        article_title = request.args.get('article_title', None)
        collection=create_database_connection()
        response = display_article_content(collection,str(article_title))
        if response:
            return json.loads(response)
        else:
            return json.loads('{"Message":"No Content found for the particular title"}')


api.add_resource(GetArticlesOnDate, '/get_articles_from_source_on_date/')
api.add_resource(GetArticlesOverTimePeriod, '/get_articles_from_source_on_date_over_timeperiod/')
api.add_resource(ListArticlesOnDate, '/list_articles_on_date/')
api.add_resource(ListArticlesFromNewsSource,'/list_articles_from_source_categorically/')
api.add_resource(ListNewsSources, '/list_news_sources/')
api.add_resource(ListNewsToday,'/get_articles_from_source_on_current_date/')
api.add_resource(ListArticleTitles,'/list_articles_titles/')
api.add_resource(ListArticle,'/get_article_content/')


if __name__ == "__main__":
    app.run(debug=True)