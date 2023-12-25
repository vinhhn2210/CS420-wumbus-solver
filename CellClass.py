import pygame
import Const
import TextClass
import random

class Cell():
	def __init__(self, cellSize, cellCoord, cellID, isExplored):
		self.cellSize = cellSize
		self.cellCoord = cellCoord
		self.cellID = cellID

		# Explore or not
		self.isExplored = isExplored

		# Properties
		self.itemPadding = cellSize[1] * 15 / 100

		self.chestSize = (cellSize[0] * 90 / 100, cellSize[1] * 120 / 100)
		self.chestCoord = self.getItemCoord(self.chestSize)

		self.wumpusSize = (cellSize[0] * 90 / 100, cellSize[1] * 120 / 100)
		self.wumpusCoord = self.getItemCoord(self.wumpusSize)

		self.fillColorPadding = (cellSize[0] * 10 / 100, cellSize[1] * 10 / 100)

		self.rect_dimensions = (self.cellCoord[0] + self.fillColorPadding[0], self.cellCoord[1] + self.fillColorPadding[1], self.cellSize[0] - 2 * self.fillColorPadding[0], self.cellSize[1] - 2 * self.fillColorPadding[1])
		self.rect_surface = pygame.Surface((self.rect_dimensions[2], self.rect_dimensions[3]), pygame.SRCALPHA)

		# Cell Image
		self.unexplored_image = pygame.transform.scale(Const.CELL_IMAGE_UNEXPLORED, self.cellSize)

		# Image
		self.image = [
			pygame.transform.scale(Const.CELL_IMAGE_LIST[i], cellSize) 
		for i in range(5)]

		self.chestImage = pygame.transform.scale(Const.CELL_IMAGE_CHEST, self.chestSize) 

		self.wumpusImage = pygame.transform.scale(Const.CELL_IMAGE_CHEST, self.wumpusSize) 

		self.pitImage = pygame.transform.scale(Const.CELL_IMAGE_PIT, self.cellSize) 

		# Stench, Breeze Text
		self.stenchText = TextClass.Text(
			Const.VCR_OSD_MONO_FONT,
			Const.WHITE,
			20,
			"S",
			(cellCoord[0], cellCoord[1], cellSize[0], cellSize[1])
		)

		self.breezeText = TextClass.Text(
			Const.VCR_OSD_MONO_FONT,
			Const.WHITE,
			20,
			"B",
			(cellCoord[0], cellCoord[1], cellSize[0], cellSize[1])
		)

		# Cell Type
		self.emptyID = random.randint(0, len(self.image) - 1)
		self.isAgent = False
		self.isChest = False
		self.isWumpus = False
		self.isPit = False
		self.isStench = False
		self.isBreeze = False

	def getItemCoord(self, itemSize):
		itemCoord = (self.cellCoord[0] + (self.cellSize[0] - itemSize[0]) / 2, self.cellCoord[1] + self.cellSize[1] * 60 / 100 - itemSize[1])
		return itemCoord

	def updateAgent(self, value):
		self.agentID = value
		curColor = Const.COLOR_AGENT
		self.rect_surface.fill((curColor[0], curColor[1], curColor[2]))

	def updateExplored(self, value):
		self.isExplored = value

	def updateChest(self, value):
		self.chestID = value

	def updateWumpus(self, value):
		self.isWumpus = value

	def updatePit(self, value):
		self.isPit = value

	def updateStench(self, value):
		self.isStench = value

	def updateBreeze(self, value):
		self.isBreeze = value

	def draw(self, gameScreen):	
		if self.isExplored == False:
			gameScreen.blit(self.unexplored_image, self.cellCoord)
			return

		if self.isPit == True:
			gameScreen.blit(self.pitImage, self.cellCoord)
		else:
			gameScreen.blit(self.image[self.emptyID], self.cellCoord)

		if self.isWumpus == True:
			gameScreen.blit(self.wumpusImage, self.wumpusCoord)

		if self.isAgent == True:
			gameScreen.blit(self.rect_surface, (self.rect_dimensions[0], self.rect_dimensions[1]))

		if self.isChest == True:
			gameScreen.blit(self.chestImage, self.chestCoord)

		if self.isBreeze == True:
			self.breezeText.drawUpLeft(gameScreen)

		if self.isStench:
			self.stenchText.drawBottomRight(gameScreen)

