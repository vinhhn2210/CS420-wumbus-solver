import pygame
import Const
import MapClass
import AgentClass
import TextClass
import ButtonClass
import MenuClass
import json

MOVE = {3 : (0, -1), 2 : (1, 0), 1 : (0, 1), 0 : (-1, 0)}

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

		self.gameBackground = pygame.transform.scale(Const.INGAME_BACKGROUND, (self.screenWidth, self.screenHeight))
		self.gameScreen.blit(self.gameBackground, (0, 0))
		
		# Ingame Map
		self.inGameContainer = (195.58 / 1000 * self.screenWidth, 50.55 / 562.71 * self.screenHeight, 442.72 / 1000 * self.screenWidth, 442.72 / 562.71 * self.screenHeight)

		# Minimap
		self.minimapContainer = (748.97 / 1000 * self.screenWidth, 50.55 / 562.71 * self.screenHeight, 148 / 1000 * self.screenWidth, 148 / 562.71 * self.screenHeight)

		# Running
		self.running = True

		# Menu data
		# algoName = menuData[1]
		# jsonFilePath = 'Sources/Solution/result_' + str(menuData[0]) + '_' + algoName.lower() + '.json'
		jsonFilePath = 'Sources/Solutions/[visualize]_' + menuData[0] + '_' + menuData[1] + '.json'
		self.menuData = menuData
		print(self.menuData)

		# Set up Map
		self.gameMap = None
		self.miniMap = None

		# Set up Agent
		self.agent = None

		# Data for ingame
		self.mapSize = ()
		self.map = []
		self.mapVision = []
		self.step = 0
		self.jsonData = []
		self.gameTime = 0
		self.gameMemory = 0

		self.jsonPath = jsonFilePath
		self.loadJsonFile(jsonFilePath)

		# Set up Clock
		self.clock = pygame.time.Clock()
		self.isEndGame = False
		self.initTick = pygame.time.get_ticks()
		self.stepTime = 0.3
		self.totalStep = len(self.jsonData)

		# Game Property
		self.gamePropertyCoord = (725 / 1000 * self.screenWidth, 247 / 562.71 * self.screenHeight)
		self.gamePropertySize = (196 / 1000 * self.screenWidth, 248 / 562.71 * self.screenHeight)
		self.gamePropertiesContainer = (self.gamePropertyCoord[0], self.gamePropertyCoord[1], self.gamePropertySize[0], self.gamePropertySize[1])

		self.isPause = 0
		self.pauseButton = [
			ButtonClass.Button(
				(self.gamePropertiesContainer[2] * 15 / 100, self.gamePropertiesContainer[2] * 15 / 100),
				Const.PAUSE_BUTTON[i],
				(self.gamePropertiesContainer[0], self.gamePropertiesContainer[1], self.gamePropertiesContainer[2] / 4, self.gamePropertiesContainer[3] * 30 / 100)
			)
			for i in range(2)
		]
		self.downSpeedButton = ButtonClass.Button(
			(self.gamePropertiesContainer[2] * 15 / 100, self.gamePropertiesContainer[2] * 15 / 100),
			Const.LEFT_BUTTON,
			(self.gamePropertiesContainer[0] + self.gamePropertiesContainer[2] / 4, self.gamePropertiesContainer[1], self.gamePropertiesContainer[2] / 4, self.gamePropertiesContainer[3] * 30 / 100)
		)
		self.upSpeedButton = ButtonClass.Button(
			(self.gamePropertiesContainer[2] * 15 / 100, self.gamePropertiesContainer[2] * 15 / 100),
			Const.RIGHT_BUTTON,
			(self.gamePropertiesContainer[0] + self.gamePropertiesContainer[2] * 2 / 4, self.gamePropertiesContainer[1], self.gamePropertiesContainer[2] / 4, self.gamePropertiesContainer[3] * 30 / 100)
		)
		self.menuButton = ButtonClass.Button(
			(self.gamePropertiesContainer[2] * 15 / 100, self.gamePropertiesContainer[2] * 15 / 100),
			Const.MENU_BUTTON,
			(self.gamePropertiesContainer[0] + self.gamePropertiesContainer[2] * 3 / 4, self.gamePropertiesContainer[1], self.gamePropertiesContainer[2] / 4, self.gamePropertiesContainer[3] * 30 / 100)
		)

		textPadding = self.gamePropertiesContainer[2] * 5 / 100 
		# Time Text
		self.timeText = TextClass.Text(
			Const.AMATICSC_FONT,
			Const.BROWN,
			30,
			"Time: 0ms",
			(self.gamePropertiesContainer[0] + textPadding, self.gamePropertiesContainer[1] + self.gamePropertiesContainer[3] * 30 / 100, self.gamePropertiesContainer[2] - 2 * textPadding, self.gamePropertiesContainer[3] * 10 / 100)
		)
		# Time Text
		self.memoryText = TextClass.Text(
			Const.AMATICSC_FONT,
			Const.BROWN,
			30,
			"Memory: 0MB",
			(self.gamePropertiesContainer[0] + textPadding, self.gamePropertiesContainer[1] + self.gamePropertiesContainer[3] * 45 / 100, self.gamePropertiesContainer[2] - 2 * textPadding, self.gamePropertiesContainer[3] * 10 / 100)
		)
		# Score Text
		self.scoreText = TextClass.Text(
			Const.AMATICSC_FONT,
			Const.BROWN,
			30,
			"Score: 0",
			(self.gamePropertiesContainer[0] + textPadding, self.gamePropertiesContainer[1] + self.gamePropertiesContainer[3] * 60 / 100, self.gamePropertiesContainer[2] - 2 * textPadding, self.gamePropertiesContainer[3] * 10 / 100)
		)
		# Score Text
		self.endGameNotification = TextClass.Text(
			Const.AMATICSC_FONT,
			Const.RED,
			30,
			"Game is End!",
			(self.gamePropertiesContainer[0] + textPadding, self.gamePropertiesContainer[1] + self.gamePropertiesContainer[3] * 75 / 100, self.gamePropertiesContainer[2] - 2 * textPadding, self.gamePropertiesContainer[3] * 10 / 100)
		)

		self.timeText.changeTextContent(f'Time: 0ms')
		self.memoryText.changeTextContent(f'Memory: 0MB')
		self.scoreRecord = 0
		self.explodeCell = None
		# Update Map, Get Ready For Step 0
		self.updateMap()

	def loadJsonFile(self, jsonFilePath):
		jsonFile = open(jsonFilePath)

		data = json.load(jsonFile)

		# Json Data
		self.jsonData = data

		# Initial Map
		self.mapSize = (data['0']['mapSize'], data['0']['mapSize'])
		self.map = data["0"]["map"]
		self.mapVision = data['0']['vision']

		# Game Map
		self.gameMap = MapClass.Map(self.mapSize, self.mapVision, (self.inGameContainer[2], self.inGameContainer[3]), self.inGameContainer)

		# Initial Minimap
		self.minimap = MapClass.Map(self.mapSize, self.map, (self.minimapContainer[2], self.minimapContainer[3]), self.minimapContainer)

		# Initial Agent
		X, Y, direction, score = data["0"]["agent"]
		X = self.mapSize[0] - X - 1

		self.agent = AgentClass.Agent(self.gameMap.getCell(X, Y))
		self.agent.updateDirection(direction)

		# Time, memory
		self.gameTime = self.jsonData['0']['time']
		self.gameMemory = self.jsonData['0']['memory']

		jsonFile.close()

	def updateMap(self):
		curTime = round(self.gameTime / self.totalStep * self.step, 2)
		curMem = round(self.gameMemory / self.totalStep * self.step, 2)
		self.timeText.changeTextContent(f'Time: {curTime}ms')
		self.memoryText.changeTextContent(f'Memory: {curMem}MB')

		X, Y, direction, score = self.jsonData[f"{self.step}"]["agent"]
		X = self.mapSize[0] - X - 1
		self.agent.updateDirection(direction)

		# Update Score For Frontend
		self.scoreText.changeTextContent(f"Score: {score}")
# {'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3}
		if score == self.scoreRecord - 100:
			self.gameMap.explodeCell(X + MOVE[0][0], Y + MOVE[0][1], score == self.scoreRecord - 100)
			self.explodeCell = (X + MOVE[0][0], Y + MOVE[0][1])
		else:
			if self.explodeCell != None:
				self.gameMap.unexplodeCell(self.explodeCell[0], self.explodeCell[1])
				self.explodeCell = None
		self.mapVision = self.jsonData[f'{self.step}']['vision']
		self.map = self.jsonData[f'{self.step}']['map']

		# Update data for backend
		self.gameMap.updateMapData(self.mapVision)
		self.minimap.updateMapData(self.map)

		# Update Ingame Map for frontend
		for row in range(self.mapSize[0]):
			for col in range(self.mapSize[1]):
				self.gameMap.updateMapCell(row, col, self.gameMap.getCell(row, col))
		# Update Minimap for frontend
		for row in range(self.mapSize[0]):
			for col in range(self.mapSize[1]):
				self.minimap.updateMapCell(row, col, self.minimap.getCell(row, col))

		# Update agent
		self.gameMap.getCell(X, Y).updateAgent(True)
		self.agent.updateAgentCell(self.gameMap.getCell(X, Y))	
		self.scoreRecord = score
	def pauseGame(self):
		while self.isPause == 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					exit(0)

			pauseState = self.pauseButton[0].isClicked(self.gameScreen)
			if pauseState == True:
				self.isPause = 1 - self.isPause	

			menuState = self.menuButton.isClicked(self.gameScreen)
			if menuState == True:
				menu = MenuClass.Menu((self.screenWidth, self.screenHeight))
				menu.run()
				self.running = False
				break

			self.gameScreen.blit(self.gameBackground, (0, 0))
			self.pauseButton[self.isPause].draw(self.gameScreen)
			self.menuButton.draw(self.gameScreen)
			self.upSpeedButton.draw(self.gameScreen)
			self.downSpeedButton.draw(self.gameScreen)
			self.timeText.draw(self.gameScreen)
			self.memoryText.draw(self.gameScreen)
			self.scoreText.draw(self.gameScreen)
			self.gameMap.draw(self.gameScreen)
			self.minimap.draw(self.gameScreen)
			self.agent.drawWithoutFrame(self.gameScreen)

			pygame.display.update()

		self.initTick = pygame.time.get_ticks()

	def run(self):
		while self.running :
			self.clock.tick(10)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					exit(0)
					break

			pauseState = self.pauseButton[0].isClicked(self.gameScreen)

			if pauseState == True:
				self.isPause = 1 - self.isPause
				self.pauseGame()

			menuState = self.menuButton.isClicked(self.gameScreen)
			if menuState == True:
				menu = MenuClass.Menu((self.screenWidth, self.screenHeight))
				menu.run()
				break

			if self.upSpeedButton.isClicked(self.gameScreen) == True:
				self.stepTime = max(0.3, self.stepTime - 0.1)
			if self.downSpeedButton.isClicked(self.gameScreen) == True:
				self.stepTime = min(1, self.stepTime + 0.1)


			tick = pygame.time.get_ticks()
			if tick >= self.initTick + self.stepTime * 1000:
				self.step += 1
				self.initTick += self.stepTime * 1000

				if str(self.step) in self.jsonData:
					self.updateMap()
				else:
					self.isEndGame = True

			# Draw window
			self.gameScreen.blit(self.gameBackground, (0, 0))
			self.pauseButton[self.isPause].draw(self.gameScreen)
			self.menuButton.draw(self.gameScreen)
			self.upSpeedButton.draw(self.gameScreen)
			self.downSpeedButton.draw(self.gameScreen)
			self.timeText.draw(self.gameScreen)
			self.memoryText.draw(self.gameScreen)
			self.scoreText.draw(self.gameScreen)
			self.gameMap.draw(self.gameScreen)
			self.minimap.draw(self.gameScreen)
			self.agent.draw(self.gameScreen)
			if self.isEndGame:
				self.endGameNotification.draw(self.gameScreen)

			pygame.display.update()


