''' get list of files to read '''
import os
test = []
for folder in os.listdir('/Users/andrewdo/PycharmProjects/CS121/WEBPAGES_SIMPLE/'):
    if not folder.endswith('.json') and not folder.endswith('.tsv') and not folder.endswith('.DS_Store') and not folder.endswith('.git'):
        folder = '/Users/andrew/PycharmProjects/CS121/WEBPAGES_SIMPLE/' + folder + '/'
        for f in os.listdir(folder):
            bacon = open(folder + f, 'r')
            content = bacon.read()
            test.append(content)
            bacon.close()
            print f, len(content)

condensed_milk = open('/Users/andrew/PycharmProjects/CS121/test.txt','w')

for item in test:
    print>>condensed_milk, item

''' for everyone file read and save contents '''