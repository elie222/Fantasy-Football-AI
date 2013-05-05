import os
import sys
import requests
import urllib
import time
from datetime import date
from progressbar import ProgressBar

d = date.today()
t = d.timetuple()
directory = str(t[2])+"_"+str(t[1])+"_"+str(t[0])

#remove else block to rewrite already created dir
if not os.path.exists(directory):
    os.makedirs(directory)
    print 'created directory.'
else:
    print 'directory already exists'
    sys.exit()

html = urllib.urlopen("http://www.premierleague.com/en-gb/matchday/league-table.html?season=2012-2013&month=JULY&tableView=HOME_VS_AWAY").read()
f = open(directory+"/tableHomeAndAway.html", 'w')
f.write(html)
f.close()

print 'saved home and away table.'

pbar = ProgressBar(maxval=700).start()

errorList = []

for i in range(1,700):
    try:
        response = requests.get('http://fantasy.premierleague.com/web/api/elements/'+str(i)+'/')
    except:
        errorList.append(i);
        print 'there was an error downloading i=' + str(i)
        print 'Error: ', sys.exc_info()[0]
        print 'will try download this file again afterwards.'
        continue
    if response.status_code == 200:
        html = response.text
    elif response.status_code == 500:
        print '500 error. finished at i= ' + str(i)
        break
    else:
        #shouldn't happen
        print str(response.status_code)+' status code at i= ' + str(i)
        break
    f = open(directory+"/"+ str(i), 'w')
    try:
        f.write(html)
    except:
        #should close and delete file really
        print 'there was an error for i=' + str(i)
        print "Error: ", sys.exc_info()[0]
    f.close()
    pbar.update(i + 1)
    
pbar.finish()

#try downloading files that weren't downloaded successfully again. else do it manually.
while not len(errorList) == 0:
    for i in errorList:
        try:
            response = requests.get('http://fantasy.premierleague.com/web/api/elements/'+str(i)+'/')
        except:
            print 'there was an error downloading i=' + str(i)
            print 'Error: ', sys.exc_info()[0]
            continue
        if response.status_code == 200:
            html = response.text
            errorList.remove(i)
        else:
            #shouldn't happen
            print str(response.status_code)+' status code at i= ' + str(i)
        f = open(directory+"/"+ str(i), 'w')
        try:
            f.write(html)
        except:
            #should close and delete file really
            print 'there was an error for i=' + str(i)
            print "Error: ", sys.exc_info()[0]
        f.close()
