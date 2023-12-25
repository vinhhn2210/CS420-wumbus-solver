import pygame
import Const
import random

class Cell:
	def __init__(self, cellSize, cellCoord, cellID):
		self.cellSize = cellSize
		self.cellCoord = cellCoord

class EmptyCell(Cell):
	def __init__(self, cellSize, cellCoord, cellID):
		Cell.__init__(self, cellSize, cellCoord, cellID)

		# Properties
		self.itemPadding = cellSize[1] * 15 / 100

		self.chestSize = (cellSize[0] * 90 / 100, cellSize[1] * 120 / 100)
		self.chestCoord = self.getItemCoord(self.chestSize)

		self.fillColorPadding = (cellSize[0] * 10 / 100, cellSize[1] * 10 / 100)

		self.rect_dimensions = (self.cellCoord[0] + self.fillColorPadding[0], self.cellCoord[1] + self.fillColorPadding[1], self.cellSize[0] - 2 * self.fillColorPadding[0], self.cellSize[1] - 2 * self.fillColorPadding[1])
		self.rect_surface = pygame.Surface((self.rect_dimensions[2], self.rect_dimensions[3]), pygame.SRCALPHA)

		# Image
		self.image = [
			pygame.transform.scale(Const.CELL_IMAGE_LIST[i], cellSize) 
		for i in range(5)]

		self.chestImage = [
			pygame.transform.scale(Const.CELL_IMAGE_CHEST[i], self.chestSize) 
		for i in range(9)]

		# Cell Type
		self.emptyID = random.randint(0, len(self.image) - 1)
		self.agentID = -1
		self.chestID = -1

	def getItemCoord(self, itemSize):
		itemCoord = (self.cellCoord[0] + (self.cellSize[0] - itemSize[0]) / 2, self.cellCoord[1] + self.cellSize[1] * 60 / 100 - itemSize[1])
		return itemCoord

	def updateAgent(self, agentID):
		self.agentID = agentID
		curColor = Const.COLOR_AGENT[self.agentID]
		self.rect_surface.fill((curColor[0], curColor[1], curColor[2]))

	def updateChest(self, chestID):
		self.chestID = chestID

	def draw(self, gameScreen):	
		gameScreen.blit(self.image[self.emptyID], self.cellCoord)

		if self.agentID != -1:
			gameScreen.blit(self.rect_surface, (self.rect_dimensions[0], self.rect_dimensions[1]))

		if self.chestID != -1:
			gameScreen.blit(self.chestImage[self.chestID], self.chestCoord)

class ObstacleCell(Cell):
	def __init__(self, cellSize, cellCoord, cellID):
		Cell.__init__(self, cellSize, cellCoord, cellID)

		self.image = pygame.transform.scale(Const.CELL_IMAGE_BLOCK, cellSize) 

	def draw(self, gameScreen):
		gameScreen.blit(self.image, self.cellCoord)

