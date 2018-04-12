#!/usr/bin/env Python
from collections import defaultdict
import re
from porterStemmer import PorterStemmer
import sys
import gc
import os
import urllib
from bs4 import BeautifulSoup

from array import array

porter = PorterStemmer()

''' the ./createIndex.py takes options based on argv '''
class CreateIndex:

    def __init__(self):
        ''' default dict handles cases of KeyError and will
        create an entry if not found.
        '''
        self.inverted_index = defaultdict(list)

    def getstopwords(self):
        ''' get stopwords from the stop words file *NOTE* could we just hard code this instead? what is the purpose of  reading from somewhere else?'''
        file = open(self.stop_words_file, 'r')
        stopwords = [line.rstrip() for line in file]
        self.stopwords = dict.fromkeys(stopwords)
        file.close()

    def getterms(self, line):
        ''' given a stream of text, get the terms, from the text '''
        line = line.lower()         # lowercase every single word
        line = re.sub(r'[^a-z0-9 ]', ' ', line)# put spaces instead of non-alphanumeric characters
        line = line.split()
        line = [x for x in line if x not in self.stopwords] #eliminate the stopwords
        #line = [porter.stem(word, 0, len(word) - 1) for word in line]
        return line

    def readdocument(self, document,folder):
        html = urllib.urlopen('/Users/Rodrigo/Documents/UCI/winter17/cs_121/CS121PYTHON-master/WEBPAGES_SIMPLE/' + str(folder) + '/' + document)
        soup = BeautifulSoup(html,'lxml')

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        content = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in content.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        content = '\n'.join(chunk for chunk in chunks if chunk)

        return content

    def parsecollection(self, doc_id, folder):
        ''' returns the id, title and text, of the next page in the collection '''

        content = self.readdocument(doc_id, folder)

        doc = {}
        doc['id'] = doc_id
        doc['content'] = content


        return doc

    def writeindextofile(self):
        '''write the inverted index to the file'''
        file = open(self.index_file, 'w')
        for term in self.inverted_index.iterkeys():
            posting_list = []
            for p in self.inverted_index[term]:
                doc_id = p[0]
                f = p[1]
                positions = p[2]
                #TODO figure out why f: never prints
                posting_list.append(':'.join([str(doc_id), 'f:'.join(f), ','.join(map(str, positions))]))

            print >> file, ''.join((term, '|', ';'.join(posting_list)))

        file.close()

    def getparameters(self):
        ''' get the parameters stopwords file, collection file, and the output index file'''
        parameters = sys.argv
        self.stop_words_file = parameters[1]
        #self.collection_file = parameters[2]
        self.index_file = parameters[2]

    def getlistoffiles(self, folder):
        ''' get list of files to read '''
        list_of_files = []

        cake = '/Users/Rodrigo/Documents/UCI/winter17/cs_121/CS121PYTHON-master/WEBPAGES_SIMPLE/' + str(folder) + '/'
        for f in os.listdir(cake):
            list_of_files.append(f)

        return list_of_files

    def createindex(self):
        ''' creates the index'''
        self.getparameters()
        ##self.data = open(self.collection_file, 'r')
        ''' could hardcode url to get directory as opposed to argv parameter leaning towards this'''

        self.getstopwords()

        gc.disable()
        #iterate through number of folders
        for folder in range(3):
            self.list_of_files = []
            self.list_of_files = self.getlistoffiles(folder)
            #for file in directory:
            ''' process every single file in directory to create index'''
            for x in self.list_of_files:

                page_dict = self.parsecollection(x,folder)
                # loop over to create index
                while page_dict != {}:
                    lines= page_dict['content']
                    page_id = int(page_dict['id'])
                    terms = self.getterms(lines)

                    #build index for current page
                    term_dict_page = {}
                    for position, term in enumerate(terms):
                        try:
                            term_dict_page[term][1].append(position)
                        except:
                            term_dict_page[term] = [page_id, str(folder), array('I', [position])]

                    for term_page, posting_page in term_dict_page.iteritems():
                        self.inverted_index[term_page].append(posting_page)

                    #page_dict = self.parsecollection(x)

                    gc.enable()

                    self.writeindextofile()
                    page_dict = {}


if __name__ == '__main__':
    create_index = CreateIndex()
    create_index.createindex()


























