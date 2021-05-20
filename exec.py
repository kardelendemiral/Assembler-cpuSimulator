# set_cf set_zf set_sf
def store(operand, add_mode):   # operand and add_mode can be (B)0002-01 ,([B])0002-10, xxxx-11
    decimal_address = int(operand, 16)
    value_to_be_stored = registers[0]
    if add_mode == '01':
        reg_name = get_register_name(operand)        # A, B falan oldu
        registers[reg_name-'A'+1] = value_to_be_stored
    elif add_mode == '10':
        reg_name = get_register_name(operand)        # A, B falan oldu
        store_address = registers[reg_name-'A'+1]    # reg deki adresi aldim
        store_dec_add = int(store_address, 16)
        memory[store_dec_add] = value_to_be_stored   # regdeki adrese koydum
    elif add_mode == '11':
        memory[decimal_address] = value_to_be_stored # direkt o adrese koydum    



def get_value(addmode, operand):
    if addmode == "00":
        return operand
    elif addmode == "01": # operand is in the register
        lastChar = operand[-1]
        reg = lastChar - '0'
        return registers[reg]
    elif addmode == "11": # operand is a memory adress
        return memory[int(operand, 16)]
    else: # 10 memory address is in the register
        lastChar = operand[-1]
        reg = lastChar - '0'
        memoryLoc = int(registers[reg], 16)
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
reg_max_value = 31

for line in inputFile:
    instructions.append(line)


isJump = False
inst_count = 0
instruction = instructions[inst_count]
registers = [0, 0, 0, 0, 0, 0, 0]  # PC A B C D E S bunlar decimal depoluyo
memory = [None] * 65536
stack = []
cf = False
zf = False
sf = False

while True:  # bu boyle cunku kac intructionlari kac kere execute edicegimizi bilmiyoz halt gelene kadar bakcaz
    isJump = False
    first = instruction[0:2]
    ia = get_inst_add_type(first)
    inst_type = ia[0]
    addressing_mode = ia[1]
    last = instruction[2:]
    value = int(get_value(addressing_mode, last), 16) # decimal dondu
    
    dumb = 0

    if first == "HALT":
        break
    elif inst_type == 'LOAD': # 0041
        registers[1] = value
    elif inst_type == 'STORE':
        store(last, addressing_mode) #bu funcda a'yi store edicegimiz yeri bulup store ederiz
        dumb = 0
    elif inst_type == 'ADD':
        # cf, sf, zf
        registers[1] += value
        if cf:
            registers[1] += reg_max_value + 1
        if registers[1] < 0:
            sf = True
        else:
            sf = False
        if registers[1] == 0:
            zf = True
        else:
            zf = False    
        if registers[1] > reg_max_value:
            cf = True
        else:
            cf = False    
    elif inst_type == 'SUB':
        # cf, sf, zf
        registers[1] -= value
        if cf:
            registers[1] += reg_max_value + 1
        if registers[1] < 0:
            sf = True
        else:
            sf = False
        if registers[1] == 0:
            zf = True
        else:
            zf = False    
        if registers[1] > reg_max_value:
            cf = True
        else:
            cf = False
    elif inst_type == 'INC':        # INC 0041'A' INC 0002(B) registers[2] +=1   INC[B] memory[45]+=1  B=45 INC[xxxx] memory[xdec] +=1
        # cf, sf, zf
        # flag varsa bakmamıza gerek var mı bilmiyoruz
        result = 0
        if addressing_mode == '01':
            reg_name = get_register_name(last)  
            registers[reg_name-'A'+1] += 1
            result = registers[reg_name-'A'+1]
        elif addressing_mode == '00':
            dec_value = int(last, 16)
            result = dec_value + 1
        elif addressing_mode == '10':
            lastChar = last[-1]
            reg = lastChar - '0'
            memoryLoc = registers[reg]
            memory[memoryLoc] += 1
            result = memory[memoryLoc]
        elif addressing_mode == '11':
            dec_value = int(last, 16)
            memory[dec_value] += 1
            result = memory[dec_value]

        
        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False    
        if result > reg_max_value:
            cf = True
        else:
            cf = False

    elif inst_type == 'DEC':
        # cf, sf, zf
        result = 0
        if addressing_mode == '01':
            reg_name = get_register_name(last)  
            registers[reg_name-'A'+1] -= 1
            result = registers[reg_name-'A'+1]
        elif addressing_mode == '00':
            dec_value = int(last, 16)
            result = dec_value - 1
        elif addressing_mode == '10':
            lastChar = last[-1]
            reg = lastChar - '0'
            memoryLoc = registers[reg]
            memory[memoryLoc] -= 1
            result = memory[memoryLoc]
        elif addressing_mode == '11':
            dec_value = int(last, 16)
            memory[dec_value] -= 1
            result = memory[dec_value]

        
        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False    
        if result > reg_max_value:
            cf = True
        else:
            cf = False
    elif inst_type == 'XOR':
        # sf, zf
        a_dec_value = registers[1]
        result = value ^ a_dec_value
        registers[1] = result

        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False 
    elif inst_type == 'AND':
        # sf, zf
        a_dec_value = registers[1]
        result = value & a_dec_value
        registers[1] = result

        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False
    elif inst_type == 'OR':
        # sf, zf
        a_dec_value = registers[1]
        result = value | a_dec_value
        registers[1] = result

        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False
    elif inst_type == 'NOT':
        result = ~value
        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False
    elif inst_type == 'SHL':
        # cf, sf, zf
        result = value << 1

        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False
        if result > reg_max_value:
            cf = True
        else:
            cf = False    
    
    elif inst_type == 'SHR':
        # sf, zf
        result = value >> 1
        
        if result < 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False

    elif inst_type == 'NOP':
        continue
    elif inst_type == 'PUSH':
        # Push a word sized operand (two bytes) and update S by subtracting 2.
        stack.append(value)
        registers[6] -= 2 # bununla napıcaz
    elif inst_type == 'POP':
        # Pop a word sized data (two bytes) into the operand and update S by adding 2.
        lastChar = last[-1]
        reg = lastChar - '0'
        registers[reg] = stack.pop()
        registers[6] += 2 # bununla napıcaz
    elif inst_type == 'CMP':
        # cf, sf, zf
        # Perform comparison (AC-operand) and set flag accordingly.
        a_value = registers[1]
        result = a_value - value
        if result< 0:
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False    
        if result > reg_max_value:
            cf = True
        else:
            cf = False     

    elif inst_type == 'JMP': # last'ı decimala çevir ve 3'e bol sonra inst_count = orası
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
        # Reads a character into the operand.
        read_char = input()
        result = ord(read_char)
        if addressing_mode == '01':
            reg_name = get_register_name(last)  
            registers[reg_name-'A'+1] = result
        elif addressing_mode == '10':
            lastChar = last[-1]
            reg = lastChar - '0'
            memoryLoc = registers[reg]
            memory[memoryLoc] = result
        elif addressing_mode == '11':
            dec_value = int(last, 16)
            memory[dec_value] = result

    elif inst_type == 'PRINT':
        # Prints the operand as a character. abi zaten char yazin diyomus biz malmisiz
        print(chr(value))

    
    if not isJump:
        inst_count += 1
