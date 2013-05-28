import json

class Player(object):
	def __init__(self, filename=None, fixtures=None):
		'''
		TODO: change list of past and future fixtures to lists of PastFixture and FutureFixture objects. When creating player from JSON file.
		'''
		if filename is not None:
			f = open(filename,'r')
			try:
				self.data = json.loads(f.read())
			except:
				print 'ERROR creating player from file:', filename
			f.close()
		elif fixtures is not None:
			self[fixtures] = fixtures
		else:
			raise

	def __getitem__(self,key):
		return self.data[key]

	def __setitem__(self,key,item):
		self.data[key] = item

	def __repr__(self):
		return '<Player: ' + self['web_name'] + '>'