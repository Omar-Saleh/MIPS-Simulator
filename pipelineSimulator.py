from Instruction import *

class pipelineSimulator(object):
	"""docstring for pipelineSimulator"""
	def __init__(self):
		filename = raw_input("Please Write the name of the desired file to execute : ")
		i = Instruction(filename)
		self.memory = i.getMemory()
		cycles = 0
		self.isDone = False
		self.pc = i.pc
		self.PCSrc = 0
		fetchDec = FetchDecReg()
		decExReg = DecExReg()
		executeMem = ExecuteMemReg()
		memWrite = MemWriteReg()
		fetchDec.advance(decExReg)
		decExReg.advance(executeMem)
		executeMem.advance(memWrite)


	def fetchStage(self):
		pass


	def decodeStage(self):	
		pass



	def execStage(self):
		pass


	def dataStage(self):
		if(executeMem.memWrite):
			memory[int(executeMem.ALUResult , 2)] = int(executeMem.regValue , 2)
		elif(executeMem.memRead):
			memWrite.memRead = bin(memory[int(executeMem.ALUResult , 2)]).replace('0b' , '')
		elif branch & int(executeMem.ALUResult , 2):
			self.PCSrc = 1


	def writeBackStage(self):
		if(memWrite.regWrite):
			if(memWrite.memToReg):
				self.reg[memWrite.rd] = int(memWrite.ALUResult , 2)
			else:	
				if "00000" not in memWrite.rd:
					self.reg[memWrite.rd] = int(memWrite.memRead , 2)



class FetchDecReg(object):
	"""docstring for FetchDecodeReg"""
	def __init__(self):
		self.instruction = ""
		self.incPC = ""

	def advance(self, decExReg):
		decExReg.incPC = self.incPC




class DecExReg(object):
	"""docstring for"""
	def __init__(self):
		self.incPC = ""
		self.reg1 = ""
		self.reg2 = ""
		self.offset = ""
		self.rd = ""
		self.rt = ""
		self.memToReg = 0
		self.regWrite = 0
		self.branch = 0
		self.memWrite = 0
		self.memRead = 0
		self.ALUSrc = 0
		self.RegDst = 0
		self.ALUOP = ""

	def advance(self, executeMemReg):
		executeMemReg.rd = self.rd
		executeMemReg.memWrite = self.memWrite
		executeMemReg.regWrite = self.regWrite
		executeMemReg.memToReg = self.memToReg
		executeMemReg.branch = self.branch
		executeMemReg.memRead = self.memRead


class ExecuteMemReg(object):
	"""Execute/Memory Register"""
	def __init__(self):
		self.branchAddre = ""
		self.zero = 0
		self.ALUResult = ""
		self.regValue = ""
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



class MemWriteReg(object):
	"""Memory/WriteBack Register"""
	def __init__(self):
		self.ALUResult = ""
		self.memoryRead = ""
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
	elif "0111" in ALUcontrol:
		if int(src2 , 2) > int(src1 , 2):
			return "1"
		else:
			return "0"
	else:
		return bin(not(int(src1 , 2) | int(src2 , 2))).replace('0b' , '')

p = pipelineSimulator()