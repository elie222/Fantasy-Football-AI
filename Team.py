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
	def __init__(self, playerList, formation=[3,4,3], captain=None, viceCaptain=None):
		'''
		playerList - a list of 15 Player objects.
		formation - a list of 3 ints, representing the no. of defenders, midfielders and attackers respectively.
		captain - the player to be captained. Must be a Player object contained in the playerList. Can be None.
		viceCaptain - the player to be vice-captained. Must be a Player object contained in the playerList. Can be None.
		If captain or viceCaptain are None, two strikers are chosen to be captain and Vice-captain.
		'''
		self.gks = []
		self.defs = []
		self.mids = []
		self.atts = []

		if self.isFormationValid(formation):
			self.formation = formation
		else:
			raise Exception('Invalid formation.')

		gkCount = 0
		defCount = 0
		midCount = 0
		attCount = 0

		if not len(playerList) == NO_OF_PLAYERS:
			raise  Exception('Team does not have exactly %d players.'%(NO_OF_PLAYERS))

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
				raise Exception('Invalid position.')

		if not gkCount == NO_OF_GKS:
			raise Exception('Too many keepers.')
		if not defCount == NO_OF_DEFS:
			raise Exception('Too many defenders.')
		if not midCount == NO_OF_MIDS:
			raise Exception('Too many midfielders.')
		if not attCount == NO_OF_ATTS:
			raise Exception('Too many attackers.')

		# value
		self.value = 0
		for player in playerList:
			self.value += player['now_cost']

		# captain/vc
		if captain is not None:
			if captain not in playerList:
				raise Exception('Captain is not in playerList.')
			self.captain = captain
		else:
			self.captain = self.atts[0]		

		if viceCaptain is not None:
			if captain not in playerList:
				raise Exception('Vice-captain is not in playerList.')
			self.viceCaptain = viceCaptain
		else:
			self.viceCaptain = self.atts[1]

	def transferPlayer(self, playerOut, playerIn):
		'''
		playerOut - Player object to remove the team.
		playerIn - Player object to replace him with.
		Raises an exception if playerOut is not in the team or if playerOut and playerIn
		don't play in the same position.
		'''
		if not playerOut['type_name'] == playerIn['type_name']:
			raise Exception('Transfer failed. Tried to switch a player for a player in another position.')

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
			raise Exception('Transfer failed. Tried to transfer out a player that was not in the team.')

		self.value = playerOut['now_cost'] - playerIn['now_cost']

	def isFormationValid(self, formation):
		'''
		Returns true if the formation is valid. Otherwise false.
		'''
		nDefs = formation[0]
		nMids = formation[1]
		nAtts = formation[2]

		if not nDefs + nMids + nAtts == 10:
			return False

		if (nDefs <= 5 and nDefs >= 3) and (nMids <= 5 and nMids >= 2) and (nAtts <= 3 and nAtts >= 1):
			return True
		else:
			return False

	def getPlayerIdsList(self):
		'''
		Returns a list of the ids of the players in the team.
		'''
		idsList = []

		for player in self.gks:
			idsList.append(player['id'])
		for player in self.defs:
			idsList.append(player['id'])
		for player in self.mids:
			idsList.append(player['id'])
		for player in self.atts:
			idsList.append(player['id'])

		return idsList

	def __str__(self):
		res = ''
		for gk in self.gks:
			res += (str(gk) + '\n')
		for df in self.defs:
			res += (str(df) + '\n')
		for mid in self.mids:
			res += (str(mid) + '\n')
		for att in self.atts:
			res += (str(att) + '\n')

		return res[:-1]



