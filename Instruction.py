class Instruction(object):
	"""Parsing Instructions and converting them into binary and storing them in array to be used by the simulator
	Supported Instructions:
		R-type: add , sub , and , slt , sltu , nor , sll , srl , jr
		I-type: addi , beq , bne , lw , lbu , sw , sb , lui
		J-type: j , jal
	"""
	def __init__(self):
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
		with open("text.txt" , "r+") as my_file:
			lines = my_file.read().splitlines()	
		instr = [self.translate(line.replace(',' , ' ')) for line in lines]
		for m in instr:
			print m
			
	

	# Translates instructions into binary
	def translate(self , instr):
		instr = instr.split()
		#Handling R-Type instructions
		ans = ""
		print instr
		if instr[0] in self.noop:
			ans =  "000000"  + self.reg[instr[2]] + self.reg[instr[3]] + self.reg[instr[1]] + "00000" + self.func[instr[0]]

		# Handling Jumps	
		elif len(instr) == 2:
			ans = self.op[instr[0]] + "label"

		elif instr[0] in self.op:
			# Handling immediate aritmatic instructions
			if instr[0] == 'addi':
				if len(bin(int(instr[3]))) < 18:
					ans = "0" * (18 - len(bin(int(instr[3])))) + bin(int(instr[3])).replace("0b" , "")
				ans = self.op[instr[0]] + self.reg[instr[2]] + self.reg[instr[1]] + ans

			# Handling Memory Loads/Stores
			elif instr[0] == 'lw' or instr[0] == 'sw' or instr[0] ==  'lbu' or instr[0] == 'sb' or instr[0] == 'lb' or instr[0] == 'lui':
				target = instr[2].replace('(' , ' ').replace(')' , ' ').split()
				if len(bin(int(target[0]))) < 18:
					ans = "0" * (18 - len(bin(int(target[0])))) + bin(int(target[0])).replace("0b" , "")
				ans = self.op[instr[0]] + self.reg[target[1]] + self.reg[instr[1]] + ans

			# Handling branches
			else :
				pass

		return ans

i = Instruction()