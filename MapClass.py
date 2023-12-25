import pygame
import CellClass
import Const

class Map:
	def __init__(self, mapLen, mapData, mapSize, containerInfo):
		self.mapSize = mapSize
		self.mapCoord = (containerInfo[0] + (containerInfo[2] - self.mapSize[0]) / 2, containerInfo[1] + (containerInfo[3] - self.mapSize[1]) / 2)
		
		self.M, self.N = (mapLen[0], mapLen[1])
		self.mapData = mapData

		print(self.M, self.N)
		print(mapData)

		cellSize = (self.mapSize[0] / self.N, self.mapSize[1] / self.M)

		# self.mapData = mapData

		# Create Image for Map
		self.mapImage = []
		for X in range(self.M):
			mapImageRow = []
			for Y in range(self.N):
				curCell = CellClass.Cell(cellSize, (Y * cellSize[0] + self.mapCoord[0], X * cellSize[1] + self.mapCoord[1]), (X, Y), False)
				self.updateMapCell(X, Y, curCell)

				mapImageRow.append(curCell)

			self.mapImage.append(mapImageRow)

	def getCell(self, i, j):
		return self.mapImage[i % self.M][j % self.N]

	def updateMapData(self, mapData):
		self.mapData = mapData

	def updateMapCell(self, X, Y, curCell):
		if self.mapData[X][Y] != "X": 
			curCell.updateExplored(True)
		if X == self.mapSize[0] - 1 and Y == 0:
			curCell.updateExit(True)
		if 'S' in self.mapData[X][Y]:
			curCell.updateStench(True)
		if 'B' in self.mapData[X][Y]:
			curCell.updateBreeze(True)
		if 'W' in self.mapData[X][Y]:
			curCell.updateWumpus(True)
		if 'P' in self.mapData[X][Y]:
			curCell.updatePit(True)	

	def draw(self, gameScreen):
		for mapImageRow in self.mapImage:
			for cell in mapImageRow:
				cell.draw(gameScreen)

