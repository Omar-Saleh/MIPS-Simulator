from Instruction import *

class pipelineSimulator(object):
	"""docstring for pipelineSimulator"""
	def __init__(self):
		filename = raw_input("Please Write the name of the desired file to execute : ")
		i = Instruction(filename)
		Memory = i.getMemory()
		cycles = 0
		self.isDone = False




p = pipelineSimulator()