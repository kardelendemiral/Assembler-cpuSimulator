
def get_inst_add_type(s):
	bin_version = ""
	for c in s:
		cc = int(c, base=16)
		bin_version += format(cc, '04b')
	
	inst_type = bin_version[0:6]
	add_mode = bin_version[6:8]

	return_list = []		
	# INSTRUCTION TYPE
	if inst_type == '000001':
		return_list.append("HALT")
	elif inst_type == '000010':
		return_list.append("LOAD")
	elif inst_type == '000011':
		return_list.append("STORE")
	elif inst_type == '000100':
		return_list.append("ADD")
	elif inst_type == '000101':
		return_list.append("SUB")
	elif inst_type == '000110':
		return_list.append("INC")
	elif inst_type == '000111':
		return_list.append("DEC")
	elif inst_type == '001000':
		return_list.append("XOR")
	elif inst_type == '001001':
		return_list.append("AND")
	elif inst_type == '001010':
		return_list.append("OR")	
	elif inst_type == '001011':
		return_list.append("NOT")
	elif inst_type == '001100':
		return_list.append("SHL")
	elif inst_type == '001101':
		return_list.append("SHR")
	elif inst_type == '001110':
		return_list.append("NOP")	
	elif inst_type == '001111':
		return_list.append("PUSH")	
	elif inst_type == '010000':
		return_list.append("POP")	
	elif inst_type == '010001':
		return_list.append("CMP")	
	elif inst_type == '010010':
		return_list.append("JMP")	
	elif inst_type == '010011':
		return_list.append("JZ")   # JE de olabilir	
	elif inst_type == '010100':
		return_list.append("JNZ")  # JNE de olabilir 	
	elif inst_type == '010101':
		return_list.append("JC")	
	elif inst_type == '010110':
		return_list.append("JNC")	
	elif inst_type == '010111':
		return_list.append("JA")	
	elif inst_type == '011000':
		return_list.append("JAE")	
	elif inst_type == '011001':
		return_list.append("JB")	
	elif inst_type == '011010':
		return_list.append("JBE")	
	elif inst_type == '011011':
		return_list.append("READ")	
	elif inst_type == '011100':
		return_list.append("PRINT")		
	# ADDRESSING MODE
	if add_mode == '00':
		return_list.append("IMMEDIATE DATA")
	elif add_mode == '01':
		return_list.append("REGISTER")
	elif add_mode == '10':
		return_list.append("MEM ADD IN REGISTER")
	elif add_mode == '11':
		return_list.append("MEMORY ADD")

	return return_list			
																										

inputFile = open("output", "r")
outputFile = open("output2", "w")

instructions = []

for line in inputFile:
	instructions.append(line)

for instruction in instructions:
	first = instruction[0:2]
	ia = get_inst_add_type(first)
	inst_type = ia[0]
	addressing_mode = ia[1] 
	last = instruction[2:]
	#value = find_value(last)
	
