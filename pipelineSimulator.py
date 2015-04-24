from Parser import *

class pipelineSimulator(object):
	"""docstring for pipelineSimulator"""
	def __init__(self):
		#filename = raw_input("Please Write the name of the desired file to execute : ")
		i = Parser("text.txt")
		self.memory = i.getMemory()
		self.cycles = 0
		self.isDone = False
		self.stall = 0
		self.pc = calculateComplement(i.pc)
		self.PCSrc = 0
		self.reg = {'11110':0 , '00001':0, '11111':0, '11100':0, '00100':0, '00101':0, '00110':0, '00111':0, '10001':0, '00000':0
		, '01100':0, '11101':0, '11010':0, '11011':0, '10110':0, '01111':0, '10100':0, '10101':0, '10010':0, '10011':0, '10000':8
		, '01110':0, '11001':0, '11000':0, '10111':0, '01011':0, '01010':0, '01001':0, '01000':0, '00011':0, '00010':0, '01101':0
		, '00000':0}
		self.fetchDec = FetchDecReg()
		self.decExReg = DecExReg()
		self.executeMem = ExecuteMemReg()
		self.memWrite = MemWriteReg()
		print self.memory
		self.run()
		print self.reg
	#	print self.executeMem.regValue


	def fetchStage(self):
		if self.PCSrc:
			print "here"
			pc = calculateNum(self.branchAddre)
		else:
			pc = calculateNum(self.pc)
		if pc in self.memory:
			instr = self.memory[pc]
			print instr
			self.fetchDec.instruction = instr
			self.pc = calculateNum(self.pc) + 4
			self.pc = calculateComplement(self.pc)
			self.fetchDec.incPC = self.pc
			self.fetchDec.start = True
		else:
			self.fetchDec.instruction = "1" * 32

	def decodeStage(self):
		if self.fetchDec.start:
			instr = self.fetchDec.instruction
			if "1" * 32 in instr:
				pass
			else:
				opcode = instr[0:6]
				self.decExReg.reg1 = instr[6:11]
				self.decExReg.reg2 = instr[11:16]
				self.decExReg.offset = extender(instr[16:32])
				# print instr
				self.decExReg.rd = instr[16:21]
				self.decExReg.rt = instr[11:16]
				# print self.decExReg.rt
				self.control(opcode)
				self.decExReg.start = True
				self.fetchDec.advance(self.decExReg)


	def execStage(self):
		if self.decExReg.start:
			src1 = calculateComplement(self.reg[self.decExReg.reg1])
			if self.decExReg.ALUSrc:
				src2 = self.decExReg.offset
			else:
				src2 = calculateComplement(self.reg[self.decExReg.reg2])
			if self.decExReg.RegDst:
				self.executeMem.rd = self.decExReg.rt
			else:
				self.executeMem.rd = self.decExReg.rd
			self.executeMem.regValue = self.decExReg.reg2
			self.executeMem.branchAddre = calculateComplement(((calculateNum(self.decExReg.offset) << 2) + int(self.decExReg.incPC , 2)))
			# print calculateNum(self.decExReg.offset)
			# print (calculateNum(self.decExReg.offset) << 2) 
			# print calculateNum(self.executeMem.branchAddre)
			self.branchAddre = self.executeMem.branchAddre
			ALUcontrol = ALUControl(self.decExReg.ALUOP , self.decExReg.offset[26:32])
			# print self.decExReg.ALUOP
			# print ALUcontrol
			# print ALUcontrol
			if "0100" in ALUcontrol or "0011" in ALUcontrol:
				# print "here"
				src1 = self.decExReg.offset[21:26:1]
			print self.decExReg.offset[21:26:1]
			# print src1
			# print src2
			self.executeMem.ALUResult = ALU(ALUcontrol , src1 , src2)
			self.executeMem.zero = Zero(src1 , src2)
			self.executeMem.start = True
			self.decExReg.advance(self.executeMem)


	def dataStage(self):
		if self.executeMem.start:
			if self.executeMem.branch and self.executeMem.zero:
				print "here"
				self.PCSrc = 1
			if self.executeMem.notBranch and not self.executeMem.zero:
				self.PCSrc = 1
			if(self.executeMem.memWrite):
				if self.executeMem.swByte:
					self.memory[int(self.executeMem.ALUResult , 2)] = calculateNum(unextendByte(self.executeMem.regValue))
				else:
					self.memory[int(self.executeMem.ALUResult , 2)] = calculateNum(self.executeMem.regValue)
			elif(self.executeMem.memRead):
				if self.executeMem.signExtend:
					self.memWrite.memRead = signExtend(calculateComplement(int(self.memory[str(int(self.executeMem.ALUResult , 2))])))
				else:
					self.memWrite.memRead = calculateComplement(int(self.memory[str(int(self.executeMem.ALUResult , 2))]))
			self.memWrite.start = True
			self.executeMem.advance(self.memWrite)

	def writeBackStage(self):
		if self.memWrite.start:
			if(self.memWrite.regWrite):
				if(self.memWrite.memToReg):
					self.reg[self.memWrite.rd] = calculateNum(self.memWrite.memRead)
				else:	
					if "00000" not in self.memWrite.rd:
						self.reg[self.memWrite.rd] = calculateNum(self.memWrite.ALUResult)


	def run(self):
		for i in range(6):
			self.writeBackStage()
	#		print self.fetchDec
	#		print self.decExReg
	#		print self.executeMem
	#		print self.memWrite
			self.dataStage()
	#		print self.fetchDec
	#		print self.decExReg
	#		print self.executeMem
	#		print self.memWrite
			self.execStage()
	#		print self.fetchDec
	#		print self.decExReg
	#		print self.executeMem
	#		print self.memWrite
			self.decodeStage()
	#		print self.fetchDec
	#		print self.decExReg
	#		print self.executeMem
	#		print self.memWrite
			self.fetchStage()
			print self.fetchDec
			print self.decExReg
			print self.executeMem
			print self.memWrite

	def checkDone(self):
		pass


	def control(self , opcode):
		#r type intstr
		if "000000" in opcode:
			self.decExReg.regWrite = 1
			self.decExReg.RegDst = 0
			self.decExReg.ALUSrc = 0
			self.decExReg.memToReg = 0
			self.decExReg.memWrite = 0
			self.decExReg.memRead = 0
			self.decExReg.ALUOP = "010"
			self.decExReg.PCSrc = 0
			self.decExReg.branch = 0
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 0	
			self.decExReg.signExtend = 0
		#addi
		elif "001000" in opcode:
			self.decExReg.regWrite = 1 
			self.decExReg.RegDst = 1
			self.decExReg.ALUSrc = 1
			self.decExReg.memRead = 0
			self.decExReg.memWrite = 0
			self.decExReg.memToReg = 0
			self.decExReg.ALUOP = "100"
			self.decExReg.PCSrc = 0
			self.decExReg.branch = 0
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 0	
			self.decExReg.signExtend = 0
		# lw/lbu
		elif "100011" in opcode or "100100" in opcode:
			self.decExReg.regWrite = 1
			self.decExReg.RegDst = 1
			self.decExReg.ALUSrc = 1
			self.decExReg.memRead = 1
			self.decExReg.memWrite = 0
			self.decExReg.memToReg = 1
			self.decExReg.ALUOP = "000"
			self.decExReg.PCSrc = 0
			self.decExReg.branch = 0
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 0	
			self.decExReg.signExtend = 0
		# lb
		elif "100000" in opcode:
			self.decExReg.regWrite = 1
			self.decExReg.RegDst = 1
			self.decExReg.ALUSrc = 1
			self.decExReg.memRead = 1
			self.decExReg.memWrite = 0
			self.decExReg.memToReg = 1
			self.decExReg.ALUOP = "000"
			self.decExReg.PCSrc = 0
			self.decExReg.branch = 0
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 0	
			self.decExReg.signExtend = 1
		#sw
		elif "101011" in opcode:
			self.decExReg.regWrite = 0
			self.decExReg.RegDst = 1
			self.decExReg.ALUSrc = 1
			self.decExReg.memRead = 0
			self.decExReg.memWrite = 1
			self.decExReg.memToReg = 0
			self.decExReg.ALUOP = "000"
			self.decExReg.PCSrc = 0
			self.decExReg.branch = 0
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 0	
			self.decExReg.signExtend = 0
		#sb
		elif "101000" in opcode:
			self.decExReg.regWrite = 0
			self.decExReg.RegDst = 1
			self.decExReg.ALUSrc = 1
			self.decExReg.memRead = 0
			self.decExReg.memWrite = 1
			self.decExReg.memToReg = 0
			self.decExReg.ALUOP = "000"
			self.decExReg.PCSrc = 0
			self.decExReg.branch = 0
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 1
			self.decExReg.signExtend = 0
		#lui
		elif "001111" in opcode:
			self.decExReg.regWrite = 1
			self.decExReg.RegDst = 1
			self.decExReg.ALUSrc = 1
			self.decExReg.memRead = 0
			self.decExReg.memWrite = 0
			self.decExReg.memToReg = 0
			self.decExReg.ALUOP = "011"
			self.decExReg.PCSrc = 0
			self.decExReg.branch = 0
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 0
			self.decExReg.signExtend = 0	
		#beq
		elif "000100" in opcode:
			self.decExReg.regWrite = 0
			self.decExReg.RegDst = 1
			self.decExReg.ALUSrc = 0
			self.decExReg.memRead = 0
			self.decExReg.memWrite = 0
			self.decExReg.memToReg = 0
			self.decExReg.ALUOP = "001"
			self.decExReg.branch = 1
			self.decExReg.notBranch = 0
			self.decExReg.swByte = 0
			self.decExReg.signExtend = 0	
		


		

class FetchDecReg(object):
	"""docstring for FetchDecodeReg"""
	def __init__(self):
		self.instruction = ""
		self.incPC = ""
		self.start = False

	def advance(self, decExReg):
		decExReg.incPC = self.incPC


	def __repr__(self):
		return "--IF/ID Register--\nInstruction:%s\nIncremented Pc:%s\n" % (self.instruction , self.incPC)




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
		self.notBranch = 0
		self.memWrite = 0
		self.memRead = 0
		self.ALUSrc = 0
		self.RegDst = 0
		self.swByte = 0
		self.signExtend = 0	
		self.PCSrc = 0
		self.ALUOP = ""
		self.start = False

	def advance(self, executeMemReg):
		executeMemReg.memWrite = self.memWrite
		executeMemReg.regWrite = self.regWrite
		executeMemReg.memToReg = self.memToReg
		executeMemReg.branch = self.branch
		executeMemReg.notBranch = self.notBranch
		executeMemReg.memRead = self.memRead
		executeMemReg.swByte = self.swByte
		executeMemReg.signExtend = self.signExtend	
		executeMemReg.PCSrc = self.PCSrc

	def __repr__(self):
		return "--ID/EXE Register--\nIncremented Pc:%s\nRegister 1 Value:%s\nRegister 2 Value:%s\nOffset:%s\nrd field:%s\nrt field:%s\nmemToReg:%d\nregWrite:%d\nBranch:%d\nmemWrite:%d\nmemRead:%d\nALUSrc:%d\nRegDst:%d\nALUOP:%s\n" % (self.incPC , self.reg1 , self.reg2 , self.offset , self.rd , self.rt , self.memToReg , self.regWrite , self.branch , self.memWrite , self.memRead , self.ALUSrc , self.RegDst , self.ALUOP)


class ExecuteMemReg(object):
	"""Execute/Memory Register"""
	def __init__(self):
		self.branchAddre = ""
		self.ALUResult = ""
		self.regValue = ""
		self.rd = ""
		self.zero = 0
		self.branch = 0
		self.notBranch = 0
		self.memWrite = 0
		self.memRead = 0
		self.regWrite = 0
		self.memToReg = 0
		self.swByte = 0
		self.signExtend = 0	
		self.PCSrc = 0
		self.start = False

	def advance(self , memWriteReg):
		memWriteReg.ALUResult = self.ALUResult
		memWriteReg.rd = self.rd
		memWriteReg.regWrite = self.regWrite
		memWriteReg.memToReg = self.memToReg
		memWriteReg.PCSrc = self.PCSrc


	def __repr__(self):
		return "--EXE/MEM Register--\nBranch Address:%s\nALU Result:%s\nRegister Value:%s\nTarget Register:%s\nZero:%d\nBranch:%d\nMem Write:%d\nMem Read:%d\nReg Write:%d\nMem To Register:%d\n" % (self.branchAddre , self.ALUResult ,self.regValue ,self.rd,self.zero,self.branch,self.memWrite,self.memRead,self.regWrite,self.memToReg)


class MemWriteReg(object):
	"""Memory/WriteBack Register"""
	def __init__(self):
		self.start = False
		self.ALUResult = ""
		self.memRead = ""
		self.rd = ""
		self.regWrite = 0
		self.memToReg = 0
		self.PCSrc = 0

	def __repr__(self):
		return "--MEM/WB Register--\nALU Result:%s\nMemory Read:%s\nTarget Register:%s\nReg Write:%d\nMem To Reg:%d\n" % (self.ALUResult , self.memRead , self.rd , self.regWrite , self.memToReg)




def ALUControl(ALUOp , func):
	# lw/lbu/lb/sw/sb
	if "000" in ALUOp:
		return "0010"
	# beq/bne
	elif "001" in ALUOp:
		return "0110"
	# lui
	elif "011" in ALUOp:
		return "1000"
	# addi
	elif "100" in ALUOp:
		return "0010"	
	elif "010" in ALUOp:
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
		elif "000000" in func:
			# print "here"
			return "0011"
		# srl
		elif "000010" in func:
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
	# lui
	elif "1000" in ALUcontrol:
		return calculateComplement((calculateNum(src2) << 16))
	# nor
	elif "1100" in ALUControl:
		return calculateComplement(~(calculateNum(src1) | calculateNum(src2)))

def Zero(src1 , src2):
	print calculateNum(ALU("0110" , src1 , src2)) 
	if calculateNum(ALU("0110" , src1 , src2)) == 0:
		return 1
	return 0


# Handling shifts
def calculateShifts(num):
	return int(num , 2)

# Handling Negative values
def calculateComplement(num):
	# print num
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

def extender(num):
	return num[0] * 16 + num


def signExtend(num):
	num = unextendByte(num)
	return num[0] * 24 + num

def unextendByte(num):
	return num[24:]

p = pipelineSimulator()
# print calculateComplement(-4)
# print ALU("0100" , "000001" , calculateComplement(2))
# print unextendByte(calculateComplement(5))