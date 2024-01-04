import pygame
import Const
import TextClass
import random

class Cell():
	def __init__(self, cellSize, cellCoord, cellID, isExplored):
		self.cellSize = cellSize
		self.cellCoord = cellCoord
		self.cellID = cellID

		# Explored or not
		self.isExplored = isExplored

		self.chestSize = (cellSize[0] * 70 / 100, cellSize[1] * 70 / 100)
		self.chestCoord = self.getItemCoord(self.chestSize)

		self.exitSize = (cellSize[0] * 70 / 100, cellSize[1] * 100 / 100)
		self.exitCoord = self.getItemCoord(self.exitSize)

		self.wumpusSize = (cellSize[0] * 80 / 100, cellSize[1] * 80 / 100)
		self.wumpusCoord = self.getItemCoord(self.wumpusSize)
		self.fillColorPadding = (cellSize[0] * 15 / 100, cellSize[1] * 15 / 100)
		
		# Cell Image
		self.unexplored_image = pygame.transform.scale(Const.CELL_IMAGE_UNEXPLORED, self.cellSize)

		# Image
		self.image = [
			pygame.transform.scale(Const.CELL_IMAGE_LIST[i], cellSize) 
		for i in range(5)]

		self.chestImage = pygame.transform.scale(Const.CELL_IMAGE_CHEST, self.chestSize) 

		self.exitImage = pygame.transform.scale(Const.CELL_IMAGE_EXIT, self.exitSize) 

		self.wumpusImage = pygame.transform.scale(Const.CELL_IMAGE_WUMPUS, self.wumpusSize) 

		self.pitImage = pygame.transform.scale(Const.CELL_IMAGE_PIT, self.cellSize) 

		self.arrowImage = pygame.transform.scale(Const.CELL_IMAGE_ARROW, self.cellSize)
		# Stench, Breeze Text
		textSize = int(80 * cellSize[0] / 130.08)
		self.stenchText = TextClass.Text(
			Const.VCR_OSD_MONO_FONT,
			Const.S_COLOR,
			textSize,
			"S",
			(cellCoord[0], cellCoord[1], cellSize[0], cellSize[0])
		)
		self.breezeText = TextClass.Text(
			Const.VCR_OSD_MONO_FONT,
			Const.B_COLOR,
			textSize,
			"B",
			(cellCoord[0], cellCoord[1], cellSize[0], cellSize[0])
		)

		# Cell Type
		self.emptyID = random.randint(0, len(self.image) - 1)
		self.isAgent = False
		self.isChest = False
		self.isWumpus = False
		self.isPit = False
		self.isStench = False
		self.isBreeze = False
		self.isExit = False
		self.isArrow = False

	def getItemCoord(self, itemSize):
		itemCoord = (self.cellCoord[0] + (self.cellSize[0] - itemSize[0]) / 2, self.cellCoord[1] + self.cellSize[1] * 60 / 100 - itemSize[1])
		return itemCoord

	def updateAgent(self, value):
		self.isAgent = value

	def updateExplored(self, value):
		self.isExplored = value

	def updateExit(self, value):
		self.isExit = value

	def updateChest(self, value):
		self.isChest = value

	def updateWumpus(self, value):
		self.isWumpus = value

	def updatePit(self, value):
		self.isPit = value

	def updateStench(self, value):
		self.isStench = value

	def updateBreeze(self, value):
		self.isBreeze = value
  
	def updateArrow(self, value):
		self.isArrow = value

	def draw(self, gameScreen):	
		if self.isExplored == False:
			gameScreen.blit(self.unexplored_image, self.cellCoord)
			if self.isArrow == True:
				gameScreen.blit(self.arrowImage, self.cellCoord)
			return

		if self.isPit == True:
			gameScreen.blit(self.pitImage, self.cellCoord)
		else:
			gameScreen.blit(self.image[self.emptyID], self.cellCoord)

		# if self.isAgent == True:
		# 	pygame.draw.rect(gameScreen, Const.COLOR_AGENT, pygame.Rect(self.cellCoord[0] + self.fillColorPadding[0], self.cellCoord[1] + self.fillColorPadding[1], self.cellSize[0] - 2 * self.fillColorPadding[0], self.cellSize[1] - 2 * self.fillColorPadding[1]))

		if self.isBreeze == True:
			self.breezeText.drawUpLeft(gameScreen)

		if self.isStench == True:
			self.stenchText.drawBottomRight(gameScreen)
   
		if self.isWumpus == True:
			gameScreen.blit(self.wumpusImage, self.wumpusCoord)

		if self.isExit == True:
			gameScreen.blit(self.exitImage, self.exitCoord)

		if self.isChest == True:
			gameScreen.blit(self.chestImage, self.chestCoord)
   
		if self.isArrow == True:
			gameScreen.blit(self.arrowImage, self.cellCoord)


