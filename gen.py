with open("gen.txt" , "a") as t:
	for i in range(0 , 32):
		t.write("\"" + bin(i).replace("0b" , "") + '\"\n')