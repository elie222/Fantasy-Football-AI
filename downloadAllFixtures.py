import sys
import os
import urllib

DIRECTORY_NAME = 'fixtures'
NO_OF_GAMEWEEKS = 38

def main():
    #remove else block to rewrite already created dir
    if not os.path.exists(DIRECTORY_NAME):
        os.makedirs(DIRECTORY_NAME)
        print 'created directory:', DIRECTORY_NAME
    else:
        print 'directory', DIRECTORY_NAME, 'already exists.'
        sys.exit()

    for i in range(1,NO_OF_GAMEWEEKS+1):
        html = urllib.urlopen('http://fantasy.premierleague.com/fixtures/'+str(i)+'/').read()
        f = open(DIRECTORY_NAME + '/' + str(i), 'w')
        f.write(html)
        f.close()

if __name__ == '__main__':
    main()