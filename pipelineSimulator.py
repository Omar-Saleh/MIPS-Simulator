from Instruction import *

class pipelineSimulator(object):
	"""docstring for pipelineSimulator"""
	def __init__(self):
		filename = raw_input("Please Write the name of the desired file to execute : ")
		i = Instruction(filename)
		memory = i.getMemory()
		cycles = 0
		self.isDone = False
		self.pc = i.pc
		executeMem = executeMemReg()
		memWrite = memWriteReg()
		executeMem.advance(memWrite)








class executeMemReg(object):
	"""Execute/Memory Register"""
	def __init__(self):
		self.branchAddre = ""
		self.zero = 0
		self.ALUResult = 0
		self.regValue = 0
		self.rd = ""
		self.branch = 0
		self.memWrite = 0
		self.memRead = 0
		self.regWrite = 0
		self.memToReg = 0

	def advance(self , memWriteReg):
		memWriteReg.ALUResult = self.ALUResult
		memWriteReg.rd = self.rd
		memWriteReg.regWrite = self.regWrite
		memWriteReg.memToReg = self.memToReg



class memWriteReg(object):
	"""Memory/WriteBack Register1"""
	def __init__(self):
		self.ALUResult = 0
		self.memoryRead = 0
		self.rd = ""
		self.regWrite = 0
		self.memToReg = 0


def ALU(ALUcontrol ,src1 , src2):
	if "0000" in ALUcontrol:
		return bin(int(src2 , 2) & int(src1 , 2)).replace('0b' , '')
	elif "0001" in ALUcontrol:
		return bin(int(src2 , 2) | int(src1 , 2)).replace('0b' , '')
	elif "0010" in ALUcontrol:
		return bin(int(src2 , 2) + int(src1 , 2)).replace('0b' , '')
	elif "0110" in ALUcontrol:
		return bin(int(src2 , 2) - int(src1 , 2)).replace('0b' , '')
	elif "0111" in ALUcontrol and int(src2 , 2) > int(src1 , 2):
		return 1
	else:
		return bin(not(int(src1 , 2) | int(src2 , 2))).replace('0b' , '')

p = pipelineSimulator()