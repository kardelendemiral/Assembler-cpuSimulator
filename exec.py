def get_value(addmode, operand, registerArray):
    if addmode == "00":
        return operand
    elif addmode == "01": # operand is in the register
        lastChar = operand[-1]
        reg = lastChar - '0'
        return registerArray[reg]
    elif addmode == "11": # operand is a memory adress
        return memory[int(operand, 16)]
    else: # 10 memory address is in the register
        lastChar = operand[-1]
        reg = lastChar - '0'
        memoryLoc = int(registerArray[reg], 16)
        return memory[memoryLoc]


def get_inst_add_type(s):
    bin_version = ""
    for c in s:
        cc = int(c, 16)
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
        return_list.append("JZ")  # JE de olabilir
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
    return_list.append(add_mode)

    return return_list


def get_register_name(s):
	if s == '0001':
		return 'A'
	elif s == '0002':
	    return 'B'
	elif s == '0003':
		return 'C'
	elif s == '0004':
		return 'D'
	elif s == '0005':
		return 'E'
	elif s == '0006':
		return 'S'

inputFile = open("output", "r")
outputFile = open("output2", "w")

instructions = []

for line in inputFile:
	instructions.append(line)

instruction = instructions[0]

while True:  # bu boyle cunku kac intructionlari kac kere execute edicegimizi bilmiyoz halt gelene kadar bakcaz
    first = instruction[0:2]
    ia = get_inst_add_type(first)
    inst_type = ia[0]
    addressing_mode = ia[1]
    last = instruction[2:]
    registers = [0, 0, 0, 0, 0, 0, 0]
    memory = [None] * 65536
    value = get_value(ia, last, registers)
    stack = []
    cf = False
    zf = False
    sf = False

    dumb = 0

    if first == "HALT":
        break
    elif inst_type == 'LOAD':
        a = value
    elif inst_type == 'STORE':
        # store(value) bu funcda a'yi store edicegimiz yeri bulup store ederiz
        dumb = 0
    elif inst_type == 'ADD':
        # cf, sf, zf
        a = a + value
        # flaglari set et
    elif inst_type == 'SUB':
        # cf, sf, zf
        a = a - value
        # flaglar
    elif inst_type == 'INC':
        # cf, sf, zf
        # value'yu arttircaz
        dumb = 0
    elif inst_type == 'DEC':
        # cf, sf, zf
        dumb = 0
    elif inst_type == 'XOR':
        # sf, zf
        a = a ^ value
        # flaglar
    elif inst_type == 'AND':
        # sf, zf
        a = a and value  # ?????cidden boyle mi
    elif inst_type == 'OR':
        # sf, zf
        a = a or value
    elif inst_type == 'NOT':
        # sf, zf
        dumb = 0
        # not'ini alip napicaz yazmamis
    elif inst_type == 'SHL':
        # cf, sf, zf
        dumb = 0
    # value'daki registeri << yapcak
    elif inst_type == 'SHR':
        # sf, zf
        # register'i >> yapcak
        dumb = 0
    elif inst_type == 'NOP':
        continue
    elif inst_type == 'PUSH':
        # Push a word sized operand (two bytes) and update S by subtracting 2.
        dumb = 0
    elif inst_type == 'POP':
         # Pop a word sized data (two bytes) into the operand and update S by adding 2.
         dumb = 0
    elif inst_type == 'CMP':
         # cf, sf, zf
        # Perform comparison (AC-operand) and set flag accordingly.
         dumb = 0
    elif inst_type == 'JMP':
         # Unconditional jump. Set PC to address.
         dumb = 0
    elif inst_type == 'JZ':
        # Conditional jump. Jump to address (given as immediate operand) if zero flag is true.
        dumb = 0
    elif inst_type == 'JNZ':
        # Conditional jump. Jump to address (given as immediate operand) if zero flag is false.
        dumb = 0
    elif inst_type == 'JC':
        # Conditional jump. Jump if carry flag is true.
        dumb = 0
    elif inst_type == 'JNC':
        # Conditional jump. Jump if carry flag is false.
        dumb = 0
    elif inst_type == 'JA':
        # Conditional jump. Jump if carry flag is false.
        dumb = 0
    elif inst_type == 'JAE':
        # Conditional jump. Jump if above or equal.
        dumb = 0
    elif inst_type == 'JB':
        # Conditional jump. Jump if below
        dumb = 0
    elif inst_type == 'JBE':
        # Conditional jump. Jump if below or equal
        dumb = 0
    elif inst_type == 'READ':
        # Reads	a character into the operand.
        dumb = 0
    elif inst_type == 'PRINT':
        # Prints the operand as a character. abi zaten char yazin diyomus biz malmisiz
        dumb = 0
