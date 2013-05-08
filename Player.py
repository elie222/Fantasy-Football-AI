import json

class Player(object):
    def __init__(self, filename):
        f = open(filename,'r')
        self.data = json.loads(f.read())
        f.close()

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item