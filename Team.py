NO_OF_PLAYERS = 15
NO_OF_GKS = 2
NO_OF_DEFS = 5
NO_OF_MIDS = 5
NO_OF_ATTS = 3

GK_TYPE_NAME = 'Goalkeeper'
DEF_TYPE_NAME = 'Defender'
MID_TYPE_NAME = 'Midfielder'
ATT_TYPE_NAME = 'Forward'

class Team(object):
	def __init__(self, playerList, formation='343', captain=None, viceCaptain=None):
		self.gks = []
		self.defs = []
		self.mids = []
		self.atts = []

		if self.isFormationValid(formation):
			self.formation = formation
		else:
			raise

		gkCount = 0
		defCount = 0
		midCount = 0
		attCount = 0

		if not len(playerList) == NO_OF_PLAYERS:
			raise
		for player in playerList:
			if player['type_name'] == GK_TYPE_NAME:
				gkCount += 1
				self.gks.append(player)
			elif player['type_name'] == DEF_TYPE_NAME:
				defCount += 1
				self.defs.append(player)
			elif player['type_name'] == MID_TYPE_NAME:
				midCount += 1
				self.mids.append(player)
			elif player['type_name'] == ATT_TYPE_NAME:
				attCount += 1
				self.atts.append(player)
			else:
				raise

		if not gkCount == NO_OF_GKS:
			raise
		if not defCount == NO_OF_DEFS:
			raise
		if not midCount == NO_OF_MIDS:
			raise
		if not attCount == NO_OF_ATTS:
			raise

		if captain is not None:
			self.captain = captain
		else:
			self.captain = self.atts[0]		

		if viceCaptain is not None:
			self.viceCaptain = viceCaptain
		else:
			self.viceCaptain = self.atts[1]

	def transferPlayer(self, playerOut, playerIn):
		'''
		Raises an exception if playerOut is not in the team or if playerOut and playerIn
		don't play in the same position.
		'''
		if not playerOut['type_name'] == playerIn['type_name']:
			raise

		if playerOut['type_name'] == GK_TYPE_NAME:
			i = self.gks.index(playerOut)
			self.gks.remove(playerOut)
			self.gks.insert(playerIn, i)
		elif playerOut['type_name'] == DEF_TYPE_NAME:
			i = self.defs.index(playerOut)
			self.defs.remove(playerOut)
			self.defs.insert(playerIn, i)
		elif playerOut['type_name'] == MID_TYPE_NAME:
			i = self.mids.index(playerOut)
			self.mids.remove(playerOut)
			self.mids.insert(playerIn, i)
		elif playerOut['type_name'] == ATT_TYPE_NAME:
			i = self.atts.index(playerOut)
			self.atts.remove(playerOut)
			self.atts.insert(playerIn, i)
		else:
			raise

	def isFormationValid(self, formation):
		nDefs = int(formation[0])
		nMids = int(formation[1])
		nAtts = int(formation[2])

		if not nDefs + nMids + nAtts == 10:
			return False

		if (nDefs <= 5 and nDefs >= 3) and (nMids <= 5 and nMids >= 2) and (nAtts <= 3 and nAtts >= 1):
			return True
		else:
			return False


