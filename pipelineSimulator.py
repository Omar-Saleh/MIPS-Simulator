from Parser import *

class pipelineSimulator(object):
	"""docstring for pipelineSimulator"""
	def __init__(self):
	#	filename = raw_input("Please Write the name of the desired file to execute : ")
		i = Parser(filename)
		self.memory = i.getMemory()
		self.cycles = 0
		self.isDone = False
		self.stall = 0
		self.pc = calculateComplement(i.pc)
		self.PCSrc = 0
		self.fetchDec = FetchDecReg()
		self.decExReg = DecExReg()
		self.executeMem = ExecuteMemReg()
		self.memWrite = MemWriteReg()
		self.execStage()
	#	print self.executeMem.regValue


	def fetchStage(self):
		pc = calculateNum(self.pc)
		instr = self.memory.get(pc)
		self.fetchDec.instruction = instr
		self.pc = self.pc + 4
		binaryPC = calculateComplement(self.pc)
		self.fetchDec.incPC = binaryPC





	def decodeStage(self):	
		pass



	def execStage(self):
		src1 = self.decExReg.reg1
		if self.decExReg.ALUSrc:
			src2 = self.decExReg.offset
		else:
			src2 = self.decExReg.reg2
		if self.decExReg.RegDst:
			executeMem.rd = self.decExReg.rd
		else:
			self.executeMem.rd = self.decExReg.rt
		self.executeMem.regValue = self.decExReg.reg2
		self.executeMem.branchAddre = calculateComplement((calculateNum(self.decExReg.offset) << 2) + int(self.decExReg.incPC , 2))
		ALUControl = ALUControl(ALUOP)
		if "0100" in ALUcontrol or "0011" in ALUControl:
			src1 = self.decExReg.offset[21:26:1]
		self.executeMem.ALUResult = ALU(ALUControl , src1 , src2)
		self.executeMem.Zero = Zero(self.decExReg.reg1 , src2)

	def dataStage(self):
		if self.executeMem.branch & self.executeMem.zero:
			self.PCSrc = 1
		if(self.executeMem.memWrite):
			memory[int(self.executeMem.ALUResult , 2)] = calculateNum(self.executeMem.regValue)
		elif(self.executeMem.memRead):
			memWrite.memRead = calculateComplement(memory[int(self.executeMem.ALUResult , 2)])

	def writeBackStage(self):
		if(memWrite.regWrite):
			if(memWrite.memToReg):
				self.reg[memWrite.rd] = calculateNum(memWrite.ALUResult)
			else:	
				if "00000" not in memWrite.rd:
					self.reg[memWrite.rd] = calculateComplement(memWrite.memRead)


	def run(self):
		while not self.isDone:
			self.fetchStage()
			self.decodeStage()
			self.fetchDec.advance(decExReg)
			self.execStage()
			self.decExReg.advance(executeMem)
			self.dataStage()
			self.executeMem.advance(memWrite)
			self.writeBackStage()
			self.checkDone()


	def checkDone(self):
		pass


class FetchDecReg(object):
	"""docstring for FetchDecodeReg"""
	def __init__(self):
		self.instruction = ""
		self.incPC = ""

	def advance(self, decExReg):
		decExReg.incPC = self.incPC


	def __repr__(self):
		return "--IF/ID Register--\nInstruction:%s\nIncremented Pc:%s\n" % (self.instruction , self.incPC)




class DecExReg(object):
	"""docstring for"""
	def __init__(self):
		self.incPC = "010"
		self.reg1 = "110"
		self.reg2 = "111"
		self.offset = "1111"
		self.rd = "01010"
		self.rt = "01010"
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

	def __repr__(self):
		return "--ID/EXE Register--\nIncremented Pc:%s\nRegister 1 Value:%s\nRegister 2 Value:%s\nOffset:%s\nrt field:%s\nrd field:%s\nmemToReg:%d\nregWrite:%d\nBranch:%d\nmemWrite:%d\nmemRead:%d\nALUSrc:%d\nRegDst:%d\nALUOP:%s\n" % (self.incPC , self.reg1 , self.reg2 , self.offset , self.rd , self.rt , self.memToReg , self.regWrite , self.branch , self.memWrite , self.memRead , self.ALUSrc , self.RegDst , self.ALUOP)


class ExecuteMemReg(object):
	"""Execute/Memory Register"""
	def __init__(self):
		self.branchAddre = ""
		self.ALUResult = ""
		self.regValue = ""
		self.rd = ""
		self.zero = 0
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


	def __repr__(self):
		return "--EXE/MEM Register--\nBranch Address:%s\nALU Result:%s\nRegister Value:%s\nTarget Register:%s\nZero:%d\nBranch:%d\nMem Write:%d\nMem Read:%d\nReg Write:%d\nMem To Register:%d\n" % (self.branchAddre , self.ALUResult ,self.regValue ,self.rd,self.zero,self.branch,self.memWrite,self.memRead,self.regWrite,self.memToReg)


class MemWriteReg(object):
	"""Memory/WriteBack Register"""
	def __init__(self):
		self.ALUResult = ""
		self.memoryRead = ""
		self.rd = ""
		self.regWrite = 0
		self.memToReg = 0

	def __repr__(self):
		return "--MEM/WB Register--\nALU Result:%s\nMemory Read:%s\nTarget Register:%s\nReg Write:%d\nMem To Reg:%d\n" % (self.ALUResult , self.memoryRead , self.rd , self.regWrite , self.memToReg)




def ALUControl(ALUOp , func):
	if "000" in ALUOp:
		return "0010"
	elif "001" in ALUOp:
		return "0110"
	if "010" in ALUOp:
		# add
		if "100000" in func:
			return "0010"
		# subtract
		elif "100010" in func:
			return "0110"
		# and
		elif "100100" in func:
			return "0000"
		# nor
		elif "100111" in func:
			return "1100"
		# slt
		elif "101010" in func:
			return "0111"
		# sll
		elif "000010" in func:
			return "0011"
		# srl
		elif "000000" in func:
			return "0100"
		# sltu
		elif "101011" in func:
			return "0101"



def ALU(ALUcontrol ,src1 , src2):
	# and
	if "0000" in ALUcontrol:
		return calculateComplement(calculateNum(src2) & calculateNum(src1))
	# or
	elif "0001" in ALUcontrol:
		return calculateComplement(calculateNum(src2) | calculateNum(src1))
	# add
	elif "0010" in ALUcontrol:
		return calculateComplement(calculateNum(src2) + calculateNum(src1))
	# sll
	elif "0011" in ALUcontrol:
		return calculateComplement((calculateNum(src2) << calculateShifts(src1)))
	# srl
	elif "0100" in ALUcontrol:
		return calculateComplement((calculateNum(src2) >> calculateShifts(src1)))
	# sltu
	elif "0101" in ALUcontrol:
		if '1' in src2[0]:
			return "1"
		elif '1' in src[1]:
			return "0"
		else:
			return "1" if calculateNum(src2) > calculateNum(src1) else "0"
	# subtract
	elif "0110" in ALUcontrol:
		return calculateComplement(calculateNum(src2) - calculateNum(src1))
	# slt
	elif "0111" in ALUcontrol:
		if calculateNum(src2) > calculateNum(src1):
			return "1"
		else:
			return "0"
	# nor
	elif "1100" in ALUControl:
		return calculateComplement(~(calculateNum(src1) | calculateNum(src2)))

def zero(src1 , src2):
	if ALU("0110" , src1 , src2) == 0:
		return 1
	return 0


# Handling shifts
def calculateShifts(num):
	return int(num , 2)

# Handling Negative values
def calculateComplement(num):
	print num
	return (format(num if num >= 0 else (1 << 32) + num, '032b'))


def calculateNum(num):
	#print num
	if num[0] == '1':
		newNum = num[num.find('0')::]
		n = ""
		for i in range(len(newNum)):
			n += "1" if newNum[i] == '0' else "0"
		return (int(n , 2) + 1) * -1 
	else:
		return int(num , 2)

#p = pipelineSimulator()
# print calculateComplement(-4)
# print ALU("0100" , "000001" , calculateComplement(2))