import pygame
import CellClass
import Const

class Map:
	def __init__(self, mapLen, mapData, mapSize, containerInfo):
		self.mapSize = mapSize
		self.mapCoord = (containerInfo[0] + (containerInfo[2] - self.mapSize[0]) / 2, containerInfo[1] + (containerInfo[3] - self.mapSize[1]) / 2)
		
		self.M, self.N = (mapLen[0], mapLen[1])
		self.mapData = mapData

		cellSize = (self.mapSize[0] / self.N, self.mapSize[1] / self.M)

		# self.mapData = mapData

		# Create Image for Map
		self.mapImage = []
		for i in range(self.M):
			mapImageRow = []
			for j in range(self.N):
				if self.mapData[i][j] == "-1": 
					mapImageRow.append(CellClass.ObstacleCell(cellSize, (j * cellSize[0] + self.mapCoord[0], i * cellSize[1] + self.mapCoord[1]), (i, j)))
				else:
					mapImageRow.append(CellClass.EmptyCell(cellSize, (j * cellSize[0] + self.mapCoord[0], i * cellSize[1] + self.mapCoord[1]), (i, j)))

			self.mapImage.append(mapImageRow)

	def getCell(self, i, j):
		return self.mapImage[i % self.M][j % self.N]

	def draw(self, gameScreen):
		for mapImageRow in self.mapImage:
			for cell in mapImageRow:
				cell.draw(gameScreen)

