#!/usr/bin/env python3

from picture import Picture
from PIL import Image
import math
class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
   

    def smallest(self, arg1, arg2, arg3, arg4, cumulativeTable, is_vertical):
        if is_vertical:
            row = arg4
            if (cumulativeTable[arg1, row] <= cumulativeTable[arg2, row]and cumulativeTable[arg1, row] <= cumulativeTable[arg3, row]):
                return arg1
            if (cumulativeTable[arg2, row] <= cumulativeTable[arg1, row]and cumulativeTable[arg2, row] <= cumulativeTable[arg3, row]):
                return arg2
            if (cumulativeTable[arg3, row] <= cumulativeTable[arg1, row]and cumulativeTable[arg3, row] <= cumulativeTable[arg2, row]):
                return arg3
        else:
            col = arg4
            if (cumulativeTable[col, arg1] <= cumulativeTable[col, arg2]and cumulativeTable[col, arg1] <= cumulativeTable[col, arg3]):
                return arg1
            if (cumulativeTable[col, arg2] <= cumulativeTable[col, arg1]and cumulativeTable[col, arg2] <= cumulativeTable[col, arg3]):
                return arg2
            if (cumulativeTable[col, arg3] <= cumulativeTable[col, arg1]and cumulativeTable[col, arg3] <= cumulativeTable[col, arg2]):
                return arg3

    def smaller(self, arg1, arg2, arg3, cumulativeTable, is_vertical):  
        if is_vertical:
            row = arg3
            return arg1 if cumulativeTable[arg1, row] <= cumulativeTable[arg2, row] else arg2
        else:
            col = arg3
            return arg1 if cumulativeTable[col, arg1] <= cumulativeTable[col, arg2] else arg2


    def energy(self, i: int, j: int) -> float:
        """
        Return the energy of pixel at column i and row j
        """
        if i < 0 or j < 0 or i >= self.width() or j >= self.height():
            raise IndexError
        if i < 0 or j < 0 or i >= self.width() or j >= self.height():
            raise IndexError

        up = self[i, (j - 1) % self.height()]
        down = self[i, (j + 1) % self.height()]
        right = self[(i + 1) % self.width(), j]
        left = self[(i - 1) % self.width(), j]

        deltaXRed = abs(right[0] - left[0])
        deltaXGreen = abs(right[1] - left[1])
        deltaXBlue = abs(right[2] - left[2])
        deltaYRed = abs(down[0] - up[0])
        deltaYGreen = abs(down[1] - up[1])
        deltaYBlue = abs(down[2] - up[2])

        sumX = deltaXBlue**2 + deltaXGreen**2 + deltaXRed**2
        sumY = deltaYBlue**2 + deltaYGreen**2 + deltaYRed**2

        return (sumX + sumY) ** 0.5


    def find_vertical_seam(self) -> list[int]:
        cumulativeTable = {}
        seam = []

        # Fills in the cumulative energy table
        # First row of Cumulative table is just equal to its energy
        for i in range(0, self.width()):  # O(W)
            cumulativeTable[i, 0] = self.energy(i, 0)
            
        # Succeeding rows energy is equal to its
        # energy + minimum between the cumulative energies of the 3 upper adjacent
        for i in range(1, self.height()):  # O(WH)
            for j in range(self.width()):
                if j == 0:  
                    cumulativeTable[j, i] = self.energy(j, i) + min(cumulativeTable[j, i - 1], cumulativeTable[j + 1, i - 1])
                elif j == self.width() - 1:
                    cumulativeTable[j, i] = self.energy(j, i) + min(cumulativeTable[j, i - 1], cumulativeTable[j - 1, i - 1])
                else:
                    cumulativeTable[j, i] = self.energy(j, i) + min(cumulativeTable[j, i - 1],cumulativeTable[j - 1, i - 1],cumulativeTable[j + 1, i - 1])
                    
        # Gets the smallest cumulative energy in the last row
        smallestLastRow = math.inf
        for j in range(self.width()): 
            if cumulativeTable[j, self.height() - 1] < smallestLastRow:
                smallestLastRow = cumulativeTable[j, self.height() - 1]
                indexOfSmallest = j
        seam.append(indexOfSmallest)
        currentCol = indexOfSmallest
        for i in range(self.height() - 1, 0, -1): 
            if currentCol == 0 or currentCol == self.width() - 1:  
                if currentCol == 0:
                    currentCol = self.smaller(currentCol, currentCol + 1, i - 1, cumulativeTable, True)
                else:
                    currentCol = self.smaller(currentCol, currentCol - 1, i - 1, cumulativeTable, True)
            else:
                currentCol = self.smallest(currentCol,currentCol + 1, currentCol - 1,i - 1,cumulativeTable,True)
            seam.append(currentCol)
        return seam[::-1]

    def find_horizontal_seam(self) -> list[int]:
        return list(reversed((SeamCarver(self.picture().transpose(Image.ROTATE_90)).find_vertical_seam())))
    
    def remove_vertical_seam(self, seam: list[int]):
        """
        Remove the vertical seam from the picture.
        The seam is a list of x-coordinates for each row of the image.
        After removing the seam, the width of the image should be reduced by one.
        """
        if self.width() == 1 or len(seam) != self.height():
            raise SeamError()
        for i in range(1, self.height()):
            if abs(seam[i] - seam[i - 1]) > 1:
                raise SeamError()
        for j in range(self.height()):
            for i in range(seam[j], self.width() - 1):
                self[i, j] = self[i + 1, j]
        self._width -= 1
        for j in range(self.height()):
            del self[self._width, j]
    def remove_horizontal_seam(self, seam: list[int]):
        """
        Remove a horizontal seam from the picture.
        The seam is a list of y-coordinates for each column of the image.
        After removing the seam, the height of the image should be reduced by one.
        """
        rotated = SeamCarver(self.picture().transpose(Image.ROTATE_90))
        rotated.remove_vertical_seam(list(reversed(seam)) )
        self.clear()
        self.__init__(rotated.picture().transpose(Image.ROTATE_270))

class SeamError(Exception):
    pass
