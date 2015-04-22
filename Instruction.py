class Instruction(object):
	"""Parsing Instructions and converting them into binary and storing them in array to be used by the simulator
	Supported Instructions:
		R-type: add , sub , and , slt , sltu , nor , sll , srl , jr
		I-type: addi , beq , bne , lw , lbu , sw , sb , lui
		J-type: j , jal
	"""
	def __init__(self , filename):
		self.noop = ['add' , 'sub' , 'and' , 'slt' , 'sltu' , 'nor' , 'sll' , 'srl' , 'jr']
		self.reg = {'$0':"00000" ,'$zero':"00000" ,'$at':"00001" ,'$v0':"00010" ,
					'$v1':"00011" ,'$a0':"00100" ,'$a1':"00101" ,'$a2':"00110" ,
					'$a3':"00111" ,'$t0':"01000" ,'$t1':"01001" ,'$t2':"01010" ,'$t3':"01011" ,
					'$t4':"01100" ,'$t5':"01101" ,'$t6':"01110" ,'$t7':"01111" ,
					'$s0':"10000" ,'$s1':"10001" ,'$s2':"10010" ,'$s3':"10011" ,
					'$s4':"10100" ,'$s5':"10101" ,'$s6':"10110" ,'$s7':"10111" ,
					'$t8':"11000" ,'$t9':"11001" ,'$k0':"11010" ,'$k1':"11011" ,
					'$gp':"11100" ,'$sp':"11101" ,'$fp':"11110" ,'$ra':"11111" }
		self.op = { 'addi':"001000" , 'beq':"000100", 'bne':"000101" , 'lw':"100011" , 'lbu':"100100" , 
					'sw':"101011" , 'sb':"101000" , 'lui':"001111" , 'j':"000010" , 'jal':"000010" , 'lb':""}
		self.func = {'add':"100000" , 'and':"100100" , 'jr':"001000" , 'nor':"100111" , 'slt':"101010" ,
					 'sltu':"101011" , 'srl':"000010" , 'sll':"000000" , 'sub':"100010" }
		self.labels = {}
		self.memory = {}
		

		with open(filename , "r+") as my_file:
			lines = my_file.read().splitlines()	

		#print lines
		#finding where is .data	
		for i in range(len(lines)):
			if "data" in lines[i]:
				begin_data = i + 1
				break

		#reading data	
		i = begin_data	
		while "start" not in lines[i].lower():
			if lines[i]:
				info = lines[i].split()
				self.memory[info[0]] = info[1]
			i = i + 1

		instructions = [lines[i].replace(',' , ' ') for i in range(i , len(lines))]
		self.scan(instructions)
		self.instr = [self.translate(instructions[i] , i - 1) for i in range(1 , len(instructions))]
		# Adding translated instructions to the main memory starting from the pc value specified by the user
		for i in range(len(self.instr)):
			self.memory[self.pc + (i  * 4)] = self.instr[i]

	# Translates instructions into binary
	def translate(self , instr , count):
		ans = ""
		# Removing labels if there is any
		split_Index = instr.find(':')
		if split_Index > 0:
			instr = list(instr)
			instr[split_Index - 1] = ' '
			instr[split_Index + 1] = ' '
			instr = "".join(instr)
		instr = instr.split()
		if split_Index > 0:
			instr = instr[instr.index(':') + 1::1]

		# Handling R-Type instructions
		if instr[0] in self.noop:
			ans =  "000000"  + self.reg[instr[2]] + self.reg[instr[3]] + self.reg[instr[1]] + "00000" + self.func[instr[0]]

		# Handling Jumps	
		elif len(instr) == 2 and instr[0] in self.op:
			if len(bin(self.labels[instr[1]] >> 2)) < 28:
				ans = "0" * (28 - len(bin(self.labels[instr[1]] >> 2)))
			ans = self.op[instr[0]] + ans + bin(self.labels[instr[1]] >> 2).replace("0b" , "")

		elif instr[0] in self.op:
			# Handling immediate aritmatic instructions
			if instr[0] == 'addi':
				print calculateOffSet(int(instr[3]))
				ans = self.op[instr[0]] + self.reg[instr[2]] + self.reg[instr[1]] + calculateOffSet(int(instr[3]))

			# Handling Memory Loads/Stores
			elif instr[0] == 'lw' or instr[0] == 'sw' or instr[0] ==  'lbu' or instr[0] == 'sb' or instr[0] == 'lb' or instr[0] == 'lui':
				target = instr[2].replace('(' , ' ').replace(')' , ' ').split()
				ans = self.op[instr[0]] + self.reg[target[1]] + self.reg[instr[1]] + ans + calculateOffSet(int(target[0]))

			# Handling branches
			else:
				ans = self.op[instr[0]] + self.reg[instr[1]] + self.reg[instr[2]] + calculateOffSet(self.labels[instr[3]] - self.pc - (count * 4) - 4)
		return ans

	# Index labels to their addresses
	def scan(self , lines):
		counter = -5
		for line in lines:
			if counter >= -4:
				counter = counter + 4
			if "start" in line.lower():
				start = line.replace(':' , ' ').split()
				#print start
				self.pc = int(start[1] , 16)
				counter = self.pc - 4
			elif ':' in line:
				self.labels[line.replace(':' , '').split()[0]] = counter

	def getMemory(self):
		return self.memory

	def getRegMap(self):
		return self.reg

	def getPC(self):
		return self.PC


def calculateOffSet(num):
	return (format(num if num >= 0 else (1 << 16) + num, '016b'));


#i = Instruction("text.txt")
#print i.memory
# print i.labels
# x = calculateOffSet(7)
# test = x[x.find('0')::]
# print x
# print test
# ans = ""
# for i in range(len(test)):
# 	ans += "1" if test[i] == '0' else "0"
# print ans
# print (int(ans , 2)) + 1

# # print len(calculateOffSet(-5))
# # print int(calculateOffSet(-5) , 2)

# # print ~x + 1
