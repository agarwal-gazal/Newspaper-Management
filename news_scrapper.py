# -*- coding: utf-8 -*-
"""
Calls the necessary utilities for building newspaper source, downloading and loading the articles

@required parameters : 'root_dir' : output_directory
						'source_list' : text file containing news sites

Please run the news_feed.sh file to execute the module

"""

import argparse
from utility.newspaper_utility import *

input_parser = argparse.ArgumentParser()
input_parser.add_argument('--root_dir', action='store', default=r'resource\\output\\', help='output_directory', required=True)
input_parser.add_argument('--source_list', action='store', default=r'resource\\input\\file.txt', help='text file containing news sites',required=True)

def fetch_news_url(input_file,output_dir):
	"""
	
	@param input_file: location to the input text file containing the newspaper sites
	@param output_dir: output_directory to write the json

	"""
	try:
		f=open(input_file,'r')
	except Exception as e:
		raise e
	else:
		list_of_url=[line.strip() for line in f.readlines()]
		print(list_of_url)	
		build_newspaper(list_of_url,output_dir)



if __name__=="__main__":

	args = input_parser.parse_args()
	fetch_news_url(args.source_list,args.root_dir)