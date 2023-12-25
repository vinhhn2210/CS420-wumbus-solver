import pygame
import Const
import MapClass
import AgentClass
import TextClass
import ButtonClass
import MenuClass
import json

class InGame:
	def __init__(self, menuData):
		# Init
		pygame.init()

		# Set up Game Window
		infoObject = pygame.display.Info()
		screenProportion = 1
		self.gameScreen = pygame.display.set_mode((infoObject.current_w * screenProportion, infoObject.current_h * screenProportion))
		pygame.display.set_caption("Logical Agent")
		pygame.display.flip()
		self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()

		# Running
		self.running = True

		# Menu data
		# algoName = menuData[1]
		# jsonFilePath = 'Sources/Solution/result_' + str(menuData[0]) + '_' + algoName.lower() + '.json'
		jsonFilePath = 'Sources/Solutions/result_test_dpll.json'
		self.menuData = menuData
		print(self.menuData)

		# Set up Map
		self.gameMap = []

		# Set up Agent
		self.agent = None

		# Data for ingame
		self.map = []
		self.mapVision = []
		self.mapSize = ()
		self.step = 0
		self.jsonData = []
		self.gameTime = 0
		self.gameMemory = 0

		self.jsonPath = jsonFilePath
		self.loadJsonFile(jsonFilePath)

		self.gameBackground = pygame.transform.scale(Const.INGAME_BACKGROUND, (self.screenWidth, self.screenHeight))
		self.gameScreen.blit(self.gameBackground, (0, 0))
		self.inGameContainer = (159 / 1000 * self.screenWidth, 51 / 562.71 * self.screenHeight, 542 / 1000 * self.screenWidth, 447 / 562.71 * self.screenHeight)

		# Game Properties
		# self.isPause = 0
		# self.gamePropertiesContent = (762.51 / 1000 * self.screenWidth, 51 / 562.71 * self.screenHeight, 196 / 1000 * self.screenWidth, 152 / 562.71 * self.screenHeight)
		# self.pauseButton = [
		# 	ButtonClass.Button(
		# 		(self.gamePropertiesContent[2] * 15 / 100, self.gamePropertiesContent[2] * 15 / 100),
		# 		Const.PAUSE_BUTTON[i],
		# 		(self.gamePropertiesContent[0], self.gamePropertiesContent[1], self.gamePropertiesContent[2] / 4, self.gamePropertiesContent[3] * 30 / 100)
		# 	)
		# 	for i in range(2)
		# ]
		# self.downSpeedButton = ButtonClass.Button(
		# 	(self.gamePropertiesContent[2] * 15 / 100, self.gamePropertiesContent[2] * 15 / 100),
		# 	Const.LEFT_BUTTON,
		# 	(self.gamePropertiesContent[0] + self.gamePropertiesContent[2] / 4, self.gamePropertiesContent[1], self.gamePropertiesContent[2] / 4, self.gamePropertiesContent[3] * 30 / 100)
		# )
		# self.upSpeedButton = ButtonClass.Button(
		# 	(self.gamePropertiesContent[2] * 15 / 100, self.gamePropertiesContent[2] * 15 / 100),
		# 	Const.RIGHT_BUTTON,
		# 	(self.gamePropertiesContent[0] + self.gamePropertiesContent[2] * 2 / 4, self.gamePropertiesContent[1], self.gamePropertiesContent[2] / 4, self.gamePropertiesContent[3] * 30 / 100)
		# )
		# self.menuButton = ButtonClass.Button(
		# 	(self.gamePropertiesContent[2] * 15 / 100, self.gamePropertiesContent[2] * 15 / 100),
		# 	Const.MENU_BUTTON,
		# 	(self.gamePropertiesContent[0] + self.gamePropertiesContent[2] * 3 / 4, self.gamePropertiesContent[1], self.gamePropertiesContent[2] / 4, self.gamePropertiesContent[3] * 30 / 100)
		# )

		# textPadding = self.gamePropertiesContent[2] * 5 / 100 
		# # Time Text
		# self.timeText = TextClass.Text(
		# 	Const.AMATICSC_FONT,
		# 	Const.BROWN,
		# 	20,
		# 	"Time: 0ms",
		# 	(self.gamePropertiesContent[0] + textPadding, self.gamePropertiesContent[1] + self.gamePropertiesContent[3] * 35 / 100, self.gamePropertiesContent[2] - 2 * textPadding, self.gamePropertiesContent[3] * 5 / 100)
		# )
		# # Time Text
		# self.memoryText = TextClass.Text(
		# 	Const.AMATICSC_FONT,
		# 	Const.BROWN,
		# 	20,
		# 	"Memory: 0MB",
		# 	(self.gamePropertiesContent[0] + textPadding, self.gamePropertiesContent[1] + self.gamePropertiesContent[3] * 50 / 100, self.gamePropertiesContent[2] - 2 * textPadding, self.gamePropertiesContent[3] * 5 / 100)
		# )
		# Score Text
		# self.scoreText = TextClass.Text(
		# 	Const.AMATICSC_FONT,
		# 	Const.BROWN,
		# 	20,
		# 	"Step: 0",
		# 	(self.gamePropertiesContent[0] + textPadding, self.gamePropertiesContent[1] + self.gamePropertiesContent[3] * 65 / 100, self.gamePropertiesContent[2] - 2 * textPadding, self.gamePropertiesContent[3] * 5 / 100)
		# )
		# # Score Text
		# self.floorText = TextClass.Text(
		# 	Const.AMATICSC_FONT,
		# 	Const.BROWN,
		# 	20,
		# 	"Floor: 1",
		# 	(self.gamePropertiesContent[0] + textPadding, self.gamePropertiesContent[1] + self.gamePropertiesContent[3] * 80 / 100, self.gamePropertiesContent[2] - 2 * textPadding, self.gamePropertiesContent[3] * 5 / 100)
		# )

		# Game Property
		gamePropertyCoord = (763 / 1000 * self.screenWidth, 259 / 562.71 * self.screenHeight)

		# Set up Clock
		self.clock = pygame.time.Clock()
		self.isEndGame = False
		self.initTick = pygame.time.get_ticks()
		self.stepTime = 0.3
		self.totalStep = len(self.jsonData)
		# print(self.stepTime)

		self.updateMap()

		# self.timeText.changeTextContent(f'Time: 0ms')
		# self.memoryText.changeTextContent(f'Memory: 0MB')

	def loadJsonFile(self, jsonFilePath):
		jsonFile = open(jsonFilePath)

		data = json.load(jsonFile)

		# Initial Map
		self.mapSize = (data['0']['mapSize'], data['0']['mapSize'])
		self.map = data["0"]["map"]
		self.mapVision = data['0']['vision']

		# Game Map
		inGameContainer = (159 / 1000 * self.screenWidth, 51 / 562.71 * self.screenHeight, 542 / 1000 * self.screenWidth, 447 / 562.71 * self.screenHeight)
		self.gameMap = MapClass.Map(self.mapSize, self.mapVision, (inGameContainer[2], inGameContainer[3]), inGameContainer)

		# Initial Agent
		X, Y, direction, score = data["0"]["agent"]
		X = self.mapSize[0] - X - 1

		self.agent = AgentClass.Agent(self.gameMap.getCell(X, Y))
		self.agent.updateDirection(direction)

		# Json Data
		self.jsonData = data

		# Time, memory
		self.gameTime = self.jsonData['0']['time']
		self.gameMemory = self.jsonData['0']['memory']

		jsonFile.close()

	def updateMap(self):
		# self.gameTime = self.jsonData[f'{self.step}']['time']
		# self.gameMemory = self.jsonData[f'{self.step}']['memory']
		# curTime = round(self.gameTime / self.totalStep * self.step, 2)
		# curMem = round(self.gameMemory / self.totalStep * self.step, 2)
		# self.timeText.changeTextContent(f'Time: {curTime}ms')
		# self.memoryText.changeTextContent(f'Memory: {curMem}MB')

		X, Y, direction, score = self.jsonData[f"{self.step}"]["agent"]
		X = self.mapSize[0] - X - 1
		print("Step: ", X, Y)
		self.agent.updateDirection(direction)

		self.mapVision = self.jsonData[f'{self.step}']['vision']

		# self.scoreText.changeTextContent(f"Score: {score}")

		if self.mapVision[X][Y] != 'X':
			self.gameMap.getCell(X, Y).updateExplored(True)

			if X == self.mapSize[0] - 1 and Y == 0:
				self.gameMap.getCell(X, Y).updateExit(True)
				print("OKEI HERE")

			if 'S' in self.mapVision[X][Y]:
				self.gameMap.getCell(X, Y).updateStench(True)
			if 'B' in self.mapVision[X][Y]:
				self.gameMap.getCell(X, Y).updateBreeze(True)
			if 'W' in self.mapVision[X][Y]:
				self.gameMap.getCell(X, Y).updateWumpus(True)
			if 'P' in self.mapVision[X][Y]:
				self.gameMap.getCell(X, Y).updatePit(True)

		self.gameMap.getCell(X, Y).updateAgent(True)
		self.agent.updateAgentCell(self.gameMap.getCell(X, Y))	

	# def pauseGame(self):
	# 	tmpFloor = self.curFloor

	# 	while self.isPause == 1:
	# 		for event in pygame.event.get():
	# 			if event.type == pygame.QUIT:
	# 				self.running = False
	# 				exit(0)

	# 		pauseState = self.pauseButton[0].isClicked(self.gameScreen)
	# 		if pauseState == True:
	# 			self.isPause = 1 - self.isPause	

	# 		menuState = self.menuButton.isClicked(self.gameScreen)
	# 		if menuState == True:
	# 			menu = MenuClass.Menu((self.screenWidth, self.screenHeight))
	# 			menu.run()
	# 			self.running = False
	# 			break

	# 		if self.leftButton.isClicked(self.gameScreen) == True:
	# 			if tmpFloor > 0:
	# 				tmpFloor -= 1
	# 				self.floorText.changeTextContent(f'Floor: {tmpFloor + 1}')

			
	# 		if self.rightButton.isClicked(self.gameScreen) == True:
	# 			if tmpFloor < self.totalFloor - 1:
	# 				tmpFloor += 1
	# 				self.floorText.changeTextContent(f'Floor: {tmpFloor + 1}')

	# 		self.gameScreen.blit(self.gameBackground, (0, 0))
	# 		self.pauseButton[self.isPause].draw(self.gameScreen)
	# 		self.menuButton.draw(self.gameScreen)
	# 		self.upSpeedButton.draw(self.gameScreen)
	# 		self.downSpeedButton.draw(self.gameScreen)
	# 		self.timeText.draw(self.gameScreen)
	# 		self.memoryText.draw(self.gameScreen)
	# 		self.scoreText.draw(self.gameScreen)
	# 		self.floorText.draw(self.gameScreen)
	# 		self.leftButton.draw(self.gameScreen)
	# 		self.rightButton.draw(self.gameScreen)
	# 		self.gameMap[tmpFloor].draw(self.gameScreen)
	# 		for i in self.agentList:
	# 			if i.agentFloor == tmpFloor:
	# 				i.drawWithoutFrame(self.gameScreen)
	# 		for i in self.agentPropertyList:
	# 			i.draw(self.gameScreen)
	# 		pygame.display.update()

	# 	self.initTick = pygame.time.get_ticks()
	# 	self.floorText.changeTextContent(f'Floor: {self.curFloor + 1}')


	def run(self):
		while self.running :
			self.clock.tick(10)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					exit(0)
					break

			# pauseState = self.pauseButton[0].isClicked(self.gameScreen)

			# if pauseState == True:
			# 	self.isPause = 1 - self.isPause
			# 	self.pauseGame()

			# menuState = self.menuButton.isClicked(self.gameScreen)
			# if menuState == True:
			# 	menu = MenuClass.Menu((self.screenWidth, self.screenHeight))
			# 	menu.run()
			# 	break

			# if self.upSpeedButton.isClicked(self.gameScreen) == True:
			# 	self.stepTime = max(0.01, self.stepTime - 0.1)
			# if self.downSpeedButton.isClicked(self.gameScreen) == True:
			# 	self.stepTime = min(1, self.stepTime + 0.1)


			tick = pygame.time.get_ticks()
			if tick >= self.initTick + self.stepTime * 1000:
				self.step += 1
				self.initTick += self.stepTime * 1000

				if str(self.step) in self.jsonData:
					self.updateMap()
			# 	else:
			# 		self.isEndGame = True

			# if self.isEndGame:
				# leaderboard = LeaderboardClass.Leaderboard(self.menuData)
				# leaderboard.run()
				# break

			# Draw window
			self.gameScreen.blit(self.gameBackground, (0, 0))
			# self.pauseButton[self.isPause].draw(self.gameScreen)
			# self.menuButton.draw(self.gameScreen)
			# self.upSpeedButton.draw(self.gameScreen)
			# self.downSpeedButton.draw(self.gameScreen)
			# self.timeText.draw(self.gameScreen)
			# self.memoryText.draw(self.gameScreen)
			# self.scoreText.draw(self.gameScreen)
			# self.floorText.draw(self.gameScreen)
			self.gameMap.draw(self.gameScreen)
			self.agent.draw(self.gameScreen)

			pygame.display.update()


