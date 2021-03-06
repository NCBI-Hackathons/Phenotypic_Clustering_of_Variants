import nltk
from Bio import Entrez
import time # We need this if we want to filter based on age
from urllib2 import HTTPError
import xml.etree.ElementTree as ET
from collections import Counter
import numpy as np
import operator
from os import path
import random

import settings
import ncbiutilsForVCF as ncbiutils
import lanprosForVCF as lanpros
import argparse
import os
import sys
# def parse_args():
#     """
#     Parse command-line arguments
#     """
#     parser = argparse.ArgumentParser(description="This script parses command-line arguments and will run the language processing script.")

#     parser.add_argument(
#             "--RS_ID", required=True,
#             help="REQUIRED. RS ID of interest. Could input one RS ID or more than one RS IDs")
#     args = parser.parse_args()
#     return args

# def main():
RS_pmids_abstracts_dict = {}
RS_ID = []
with open(sys.argv[1], "r") as file:
	for line in file:
		line = line.rstrip("\n")
		line = line.split()
		rs = str('rs')+str(line[0])
		RS_ID.append(rs)

for each_RS in RS_ID:
	pmids_dict = ncbiutils.get_pmids(each_RS)
	pmids_list = pmids_dict["IdList"]
	abstracts = ncbiutils.get_abstracts_from_list(pmids_list)
	RS_pmids_abstracts_dict[each_RS] = abstracts

tokens = lanpros.tokenize_abstracts(RS_pmids_abstracts_dict)

tagged_abstracts = lanpros.tagged_abstracts(tokens)

nouns = lanpros.extract_nouns(tagged_abstracts)
for rs, values in nouns.iteritems():
	for pmid, words in values.iteritems():
		toprint = [rs, pmid]
		for word in words:
			if len(word) != 1:
				toprint = [rs, pmid, word]
				print "\t".join(item for item in toprint)
