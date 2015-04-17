class InstructionMem(object):
	"""PC is the instruction address
	   instruction is the instruction being executed before it is decoded into binary	
	"""
	def __init__(self, PC):
		self.PC = PC
		self.instruction = arr[PC]
		