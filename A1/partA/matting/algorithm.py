## CSC320 Winter 2019 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################
def solveEquation(A, B):
	AT = A.T
	ATA = np.matmul(AT, A)
	invATA = np.linalg.inv(ATA)
	ATAAT = np.matmul(invATA, AT)
	return np.matmul(ATAAT, B)
#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
	#
	# The class constructor
	#
	# When called, it creates a private dictionary object that acts as a container
	# for all input and all output images of the triangulation matting and compositing 
	# algorithms. These images are initialized to None and populated/accessed by 
	# calling the the readImage(), writeImage(), useTriangulationResults() methods.
	# See function run() in run.py for examples of their usage.
	#
	def __init__(self):
		self._images = { 
			'backA': None, 
			'backB': None, 
			'compA': None, 
			'compB': None, 
			'colOut': None,
			'alphaOut': None, 
			'backIn': None, 
			'colIn': None, 
			'alphaIn': None, 
			'compOut': None, 
		}

	# Return a dictionary containing the input arguments of the
	# triangulation matting algorithm, along with a brief explanation
	# and a default filename (or None)
	# This dictionary is used to create the command-line arguments
	# required by the algorithm. See the parseArguments() function
	# run.py for examples of its usage
	def mattingInput(self): 
		return {
			'backA':{'msg':'Image filename for Background A Color','default':None},
			'backB':{'msg':'Image filename for Background B Color','default':None},
			'compA':{'msg':'Image filename for Composite A Color','default':None},
			'compB':{'msg':'Image filename for Composite B Color','default':None},
		}
	# Same as above, but for the output arguments
	def mattingOutput(self): 
		return {
			'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
			'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
		}
	def compositingInput(self):
		return {
			'colIn':{'msg':'Image filename for Object Color','default':None},
			'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
			'backIn':{'msg':'Image filename for Background Color','default':None},
		}
	def compositingOutput(self):
		return {
			'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
		}
	
	# Copy the output of the triangulation matting algorithm (i.e., the 
	# object Color and object Alpha images) to the images holding the input
	# to the compositing algorithm. This way we can do compositing right after
	# triangulation matting without having to save the object Color and object
	# Alpha images to disk. This routine is NOT used for partA of the assignment.
	def useTriangulationResults(self):
		if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
			self._images['colIn'] = self._images['colOut'].copy()
			self._images['alphaIn'] = self._images['alphaOut'].copy()

	# If you wish to create additional methods for the 
	# Matting class, include them here

	#########################################
	## PLACE YOUR CODE BETWEEN THESE LINES ##
	#########################################

	#########################################
			
	# Use OpenCV to read an image from a file and copy its contents to the 
	# matting instance's private dictionary object. The key 
	# specifies the image variable and should be one of the
	# strings in lines 54-63. See run() in run.py for examples
	#
	# The routine should return True if it succeeded. If it did not, it should
	# leave the matting instance's dictionary entry unaffected and return
	# False, along with an error message
	def readImage(self, fileName, key):
		success = True
		msg = 'read'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		try:
			self._images[key] = cv.imread(fileName)
		except:
			success = False
			msg = 'Something wrong with reading file, please double check your inputs'
		#########################################
		return success, msg

	# Use OpenCV to write to a file an image that is contained in the 
	# instance's private dictionary. The key specifies the which image
	# should be written and should be one of the strings in lines 54-63. 
	# See run() in run.py for usage examples
	#
	# The routine should return True if it succeeded. If it did not, it should
	# return False, along with an error message
	def writeImage(self, fileName, key):
		success = True
		msg = 'write'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		try:
			cv.imwrite(fileName, self._images[key])
		except:
			success = False
			msg = 'SOmething wrong with writing file, please double check your outputs'
		#########################################
		return success, msg

	# Method implementing the triangulation matting algorithm. The
	# method takes its inputs/outputs from the method's private dictionary 
	# ojbect. 
	def triangulationMatting(self):
		"""
success, errorMessage = triangulationMatting(self)
		
		Perform triangulation matting. Returns True if successful (ie.
		all inputs and outputs are valid) and False if not. When success=False
		an explanatory error message should be returned.
		"""

		success = True
		msg = 'tri'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		backA = self._images['backA']
		backB = self._images['backB']
		compA = self._images['compA']
		compB = self._images['compB']
		try:
			col = backA.shape[0]
			row = backA.shape[1]
			colOut = np.zeros((col,row,4))
			AlphaOut = np.zeros((col, row, 4))
			for i in range(col):
				for j in range(row):
					backAR = int(backA[i,j][0])
					backAG = int(backA[i,j][1])
					backAB = int(backA[i,j][2])
					backBR = int(backB[i,j][0])
					backBG = int(backB[i,j][1])
					backBB = int(backB[i,j][2])
					compAR = int(compA[i,j][0])
					compAG = int(compA[i,j][1])
					compAB = int(compA[i,j][2])
					compBR = int(compB[i,j][0])
					compBG = int(compB[i,j][1])
					compBB = int(compB[i,j][2])
					A = np.array([[1,0,0,-backAR],[0,1,0,-backAG],[0,0,1,-backAB],[1,0,0,-backBR],[0,1,0,-backBG],[0,0,1,-backBB]])
					B = np.array([[compAR-backAR],[compAG-backAG],[compAB - backAB], [compBR- backBR], [compBG- backBG], [compBB - backBB]])
					x = np.zeros((4,1))
					x = solveEquation(A, B)
					colOut[i,j][0] = x[0] 
					colOut[i,j][1] = x[1]
					colOut[i,j][2] = x[2]
					colOut[i,j][3] = 255
					AlphaOut[i,j][0] = x[3] * 255
					AlphaOut[i,j][1] = x[3] * 255
					AlphaOut[i,j][2] = x[3] * 255
					AlphaOut[i,j][3] = 255
			self._images['colOut'] = colOut
			self._images['alphaOut'] = AlphaOut
		except:
			success = False
			msg = "Something wrong when triangulating, please double check your input"
		#########################################

		return success, msg

		
	def createComposite(self):
		"""
success, errorMessage = createComposite(self)
		
		Perform compositing. Returns True if successful (ie.
		all inputs and outputs are valid) and False if not. When success=False
		an explanatory error message should be returned.
"""

		success = True
		msg = 'Placeholder'

		#########################################
		## PLACE YOUR CODE BETWEEN THESE LINES ##
		#########################################
		alphaIn = self._images['alphaIn']
		colIn = self._images['colIn']
		backIn = self._images['backIn']
		try:
			col = backIn.shape[0]
			row = backIn.shape[1]
			compOut = np.zeros((col, row, 4))
			for i in range(col):
				for j in range(row):
					alpha = int(alphaIn[i,j][0])/255.0
					red = int(colIn[i,j][0])
					green = int(colIn[i,j][1])
					blue = int(colIn[i,j][2])
					backRed = int(backIn[i,j][0])
					backGreen = int(backIn[i,j][1])
					backBLue = int(backIn[i,j][2])
					compOut[i,j][0] = alpha*red + (1-alpha)*backRed
					compOut[i,j][1] = alpha*green + (1-alpha)*backGreen
					compOut[i,j][2] = alpha*blue + (1-alpha)*backBLue
					compOut[i,j][3] = 255
			self._images['compOut'] = compOut	
		except:
			success = False
			msg = "Error compositing image, please double check your inputs"
		#########################################

		return success, msg
