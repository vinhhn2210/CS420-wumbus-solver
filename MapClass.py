import pygame
import CellClass
import Const

class Map:
	def __init__(self, mapLen, mapData, mapSize, containerInfo):
		# Map Properties
		self.mapSize = mapSize
		self.mapCoord = (containerInfo[0] + (containerInfo[2] - self.mapSize[0]) / 2, containerInfo[1] + (containerInfo[3] - self.mapSize[1]) / 2)
		
		# Backend data for map
		self.M, self.N = (mapLen[0], mapLen[1])
		self.mapData = mapData

		cellSize = (self.mapSize[0] / self.N, self.mapSize[1] / self.M)

		# Create Image for Map
		self.mapImage = []
		for X in range(self.M):
			mapImageRow = []
			for Y in range(self.N):
				curCell = CellClass.Cell(cellSize, (Y * cellSize[0] + self.mapCoord[0], X * cellSize[1] + self.mapCoord[1]), (X, Y), False)
				self.mapImage
				self.updateMapCell(X, Y, curCell)

				mapImageRow.append(curCell)

			self.mapImage.append(mapImageRow)

	def getCell(self, X, Y):
		return self.mapImage[X][Y]

	def updateMapData(self, mapData):
		self.mapData = mapData

	def updateMapCell(self, X, Y, curCell):
		if self.mapData[X][Y] != 'X': 
			curCell.updateExplored(True)

		isStench = False
		if 'S' in self.mapData[X][Y]:
			isStench = True
		curCell.updateStench(isStench)

		isBreeze = False
		if 'B' in self.mapData[X][Y]:
			isBreeze = True
		curCell.updateBreeze(isBreeze)

		isWumpus = False
		if 'W' in self.mapData[X][Y]:
			isWumpus = True
		curCell.updateWumpus(isWumpus)
		
		isPit = False
		if 'P' in self.mapData[X][Y]:
			isPit = True
		curCell.updatePit(isPit)	

		isGold = False
		# print("DATA: ", X, Y, self.mapData[X][Y])
		if 'G' in self.mapData[X][Y]:
			isGold = True
		curCell.updateChest(isGold)

	def draw(self, gameScreen):
		for mapImageRow in self.mapImage:
			for cell in mapImageRow:
				cell.draw(gameScreen)

