import sys
# set_cf set_zf set_sf
def store(operand, add_mode):   # operand and add_mode can be (B)0002-01 ,([B])0002-10, xxxx-11
    global memory
    global registers
    decimal_address = int(operand, 16)
    value_to_be_stored = registers[1]   # dec
    if add_mode == '01':
        reg_name = get_register_name(operand)        # 1, 2 falan oldu
        registers[reg_name] = value_to_be_stored
    elif add_mode == '10':
        reg_name = get_register_name(operand)      # 1, 2 falan oldu
        store_dec_add = registers[reg_name]    # reg deki adresi aldim
        o = format(value_to_be_stored, '016b')
        first_part = o[0:8]
        second_part = o[8:]
        memoryCheck(store_dec_add)
        memory[store_dec_add] = first_part   # regdeki adrese koydum
        memoryCheck(store_dec_add+1) 
        memory[store_dec_add+1] = second_part
    elif add_mode == '11':
        o = format(value_to_be_stored, '016b')
        first_part = o[0:8]
        second_part = o[8:]
        memoryCheck(decimal_address) 
        memory[decimal_address] = first_part # direkt o adrese koydum    
        memoryCheck(decimal_address+1)  
        memory[decimal_address+1] = second_part

def twos_comp(a):          # dec sayiyi 2s complement binary ye cevirip pozitif dec donuyo
    binary = format(a & 0xffff, '016b')
    return int(binary, 2)

def get_value(addmode, operand):   # hex geliyo dec donuyo
    global memory
    global registers
    if addmode == "00":
        return int(operand,16)
    elif addmode == "01": # operand is in the register 
        lastChar = operand[3]
        reg = ord(lastChar) - 48
        return registers[reg]
    elif addmode == "11": # operand is a memory adress
        memoryCheck(int(operand, 16))
        memoryCheck(int(operand, 16)+1)
        f = memory[int(operand, 16)] 
        s = memory[int(operand, 16) + 1] 
        combine = f + s
        return int(combine, 2)
    else: # 10 memory address is in the register
        lastChar = operand[3]
        reg = ord(lastChar) - 48
        memoryLoc = registers[reg]
        memoryCheck(memoryLoc)
        memoryCheck(memoryLoc+1)
        f = memory[memoryLoc]
        s = memory[memoryLoc + 1]
        combine = f + s
        return int(combine, 2)

def getTheInstructionNumber(address):
    #print(address)
    decimal = int(address, 16)
    #print(decimal/3)
    return decimal

def removeSpaces(s):
    while s[0].isspace():
        s = s[1:]
    while s[-1].isspace():
        leng = len(s)
        s = s[0:leng-1]
    return s

def get_inst_add_type(s):

    inst_type = s[0:6]
    add_mode = s[6:8]

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
    else:
        print("illegal instruction")
        exit()    
    # ADDRESSING MODE
    return_list.append(add_mode)

    return return_list


def memoryCheck(s):
    if s > 65535 or s < 0:
        print("memory limit exceeded")
        exit()

def get_register_name(s):
    if s == '0001':
        return 1
    elif s == '0002':
        return 2
    elif s == '0003':
        return 3
    elif s == '0004':
        return 4
    elif s == '0005':
        return 5
    elif s == '0006':
        return 6
    elif s == '0000':
        return 0    


inputFile = open(sys.argv[1], "r")
#outputFile = open(sys.argv[1][0:sys.argv[1].index('.')]+".exec", "w")
memory = ['00000000'] * 65536   # MEMORYDE BINARY STRING VAR 
i = 0
reg_max_value = 65535


for line in inputFile:
    first_part = line[0:2]    #08
    second_part = line[2:]    #0041
    second_part = removeSpaces(second_part)
    dec_first = int(first_part, 16)
    bin_first = format(dec_first, '08b')
    bin_second = format(int(second_part, 16), '016b')
    memoryCheck(i)
    memory[i] = bin_first
    memoryCheck(i+1)
    memory[i+1] = bin_second[0:8]
    memoryCheck(i+2)
    memory[i+2] = bin_second[8:]
    i+=3


isJump = False
registers = [0, 0, 0, 0, 0, 0, 65534]  # PC A B C D E S bunlar decimal depoluyo
instruction = memory[registers[0]]
cf = False
zf = False
sf = False
x = 1
while True:  # bu boyle cunku kac intructionlari kac kere execute edicegimizi bilmiyoz halt gelene kadar bakcaz
    x+=1
    isJump = False
    memoryCheck(registers[0])
    ia = memory[registers[0]]    #00001000
    memoryCheck(registers[0]+1)
    operand_f = memory[registers[0]+1] # 00
    memoryCheck(registers[0]+2)
    operand_s = memory[registers[0]+2] # 10
    iaa = get_inst_add_type(ia)
    inst_type = iaa[0]
    addressing_mode = iaa[1]
    combine = int((operand_f + operand_s), 2)
    last = format(combine, '04x')
    value = get_value(addressing_mode, last) # decimal dondu
    
    if inst_type == "HALT":
        break
    elif inst_type == 'LOAD': # 0041
        registers[1] = value
    elif inst_type == 'STORE':
        store(last, addressing_mode) #bu funcda a'yi store edicegimiz yeri bulup store ederiz
    elif inst_type == 'ADD':
        # cf, sf, zf
        registers[1] += value 
        if registers[1] < 0:
            registers[1] = twos_comp(registers[1])  
        if registers[1] > reg_max_value:
            cf = True
            registers[1] -= (reg_max_value + 1)
        else: 
            cf = False     
        
        b = format(registers[1], '016b')    
        
        if b[0] == '1':
            sf = True
        else:
            sf = False
        if registers[1] == 0:
            zf = True
        else:
            zf = False    
    elif inst_type == 'SUB':
        # cf, sf, zf
        registers[1] = registers[1] + ((~value) & 65535) + 1 
        if registers[1] < 0:
            registers[1] = twos_comp(registers[1]) 
        
        if registers[1] > reg_max_value:
            cf = True
            registers[1] -= (reg_max_value + 1)
        else: 
            cf = False     
        
        b = format(registers[1], '016b')   

        if b[0] == '1':
            sf = True
        else:
            sf = False
        if registers[1] == 0:
            zf = True
        else:
            zf = False    
    elif inst_type == 'INC':        # INC 0041'A' INC 0002(B) registers[2] +=1   INC[B] memory[45]+=1  B=45 INC[xxxx] memory[xdec] +=1
        # cf, sf, zf
        # flag varsa bakmamiza gerek var mi bilmiyoruz
        result = 0
        if addressing_mode == '01':
            reg_name = get_register_name(last)  
            registers[reg_name] += 1
            if registers[reg_name] < 0:
                registers[reg_name] = twos_comp(registers[reg_name]) 
            # cf icin
            if registers[reg_name] > reg_max_value:
                cf = True
                registers[reg_name] -= (reg_max_value + 1)
            else:
                cf =  False    
            result = registers[reg_name]
            # sf icin
            b = format(result, '016b')
            if b[0] == '1':
                sf = True
            else:
                sf = False        
        elif addressing_mode == '00':
            dec_value = int(last, 16)
            result = dec_value + 1
            cf = False   # emin degiliz
            b = format(result, '016b')
            if b[0] == '1':
                sf = True
            else:
                sf = False  
        elif addressing_mode == '10':
            reg = get_register_name(last)
            memoryLoc = registers[reg]
            memoryCheck(memoryLoc)
            f = int(memory[memoryLoc], 2)
            memoryCheck(memoryLoc + 1)
            s = int(memory[memoryLoc + 1], 2)
            v = int(f+s, 2) + 1
            if v > 65535:
                cf = True
                v = v - 65536
            else:
                cf = False    
            bv = format(v, '016b')   
            memory[memoryLoc] = bv[0:8]
            memory[memoryLoc+1] = bv[8:]
            result = v
            if bv[0] == '1':
                sf = True
            else:
                sf = False    
        elif addressing_mode == '11':
            dec_value = int(last, 16)
            memoryCheck(dec_value)
            f = memory[dec_value]
            memoryCheck(dec_value + 1)
            s = memory[dec_value + 1]
            v = int(f+s, 2) + 1
            if v > 65535:
                cf = True
                v = v - 65536
            else:
                cf = False    
            bv = format(v, '016b') 
            if bv[0] == '1':
                sf = True
            else:
                sf = False     
            memory[dec_value] = bv[0:8]
            memory[dec_value+1] = bv[8:]
            result = v
    
        if result == 0:
            zf = True
        else:
            zf = False    

    elif inst_type == 'DEC':
        # cf, sf, zf
        result = 0
        if addressing_mode == '01':
            reg_name = get_register_name(last)  
            registers[reg_name] = registers[reg_name] + ((~1)&65535) + 1
            if registers[reg_name] < 0:
                registers[reg_name] = twos_comp(registers[reg_name]) 
            # cf icin
            if registers[reg_name] > reg_max_value:
                cf = True
                registers[reg_name] -= (reg_max_value + 1)
            else:
                cf =  False    
            result = registers[reg_name]
            # sf icin
            b = format(result, '016b')
            if b[0] == '1':
                sf = True
            else:
                sf = False        
        elif addressing_mode == '00': 
            dec_value = int(last, 16)
            result = dec_value + ((~1)&65535) + 1
            if result > reg_max_value:
                cf = True
                result -= (reg_max_value + 1)
            else :
                cf = False
            b = format(result, '016b')
            if b[0] == '1':
                sf = True
            else:
                sf = False  
        elif addressing_mode == '10':
            reg = get_register_name(last)
            memoryLoc = registers[reg]
            memoryCheck(memoryLoc)
            f = memory[memoryLoc]
            memoryCheck(memoryLoc+1)
            s = memory[memoryLoc + 1]
            v = int(f+s, 2) + ((~1)&65535) + 1 
            if v > 65535:
                cf = True
                v = v - 65536
            else:
                cf = False    
            bv = format(v, '016b')    
            memory[memoryLoc] = bv[0:8]
            memory[memoryLoc + 1] = bv[8:]  
            result = v
            if bv[0] == '1':
                sf = True
            else:
                sf = False    
        elif addressing_mode == '11':
            dec_value = int(last, 16)
            memoryCheck(dec_value)
            f = memory[dec_value]
            memoryCheck(dec_value+1)
            s = memory[dec_value + 1]
            v = int(f+s, 2) + ((~1)&65535) + 1 
            if v > 65535:
                cf = True
                v = v - 65536
            else:
                cf = False    
            bv = format(v, '016b') 
            if bv[0] == '1':
                sf = True
            else:
                sf = False      
            memory[dec_value] = bv[0:8]
            memory[dec_value + 1] = bv[8:]
            result = v
    
        if result == 0:
            zf = True
        else:
            zf = False  
    elif inst_type == 'XOR':
        # sf, zf
        a_dec_value = registers[1]
        result = value ^ a_dec_value
        registers[1] = result
        if registers[1] < 0:
            registers[1] = twos_comp(registers[1]) 
        b = format(registers[1], '016b')
        if b[0] == '1':
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
        if registers[1] < 0:
            registers[1] = twos_comp(registers[1])
        b = format(registers[1], '016b')
        if b[0] == '1':
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
        if registers[1] < 0:
            registers[1] = twos_comp(registers[1])
        b = format(registers[1], '016b')
        if b[0] == '1':
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False
    elif inst_type == 'NOT':
        result = ~value & 65535
        registers[1] = result
        if registers[1] < 0:
            registers[1] = twos_comp(registers[1])
        b = format(registers[1], '016b')
        if b[0] == '1':
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
        regName = get_register_name(last)
        registers[regName] = result
        if registers[regName] < 0:
            registers[regName] = twos_comp(registers[regName])

        if registers[regName] > reg_max_value:
            cf = True
            registers[regName] -= (reg_max_value + 1)
        else:
            cf =  False  

        b = format(registers[regName], '016b')

        if b[0] == '1':
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False
    
    elif inst_type == 'SHR':
        # sf, zf
        result = value >> 1
        regName = get_register_name(last)
        registers[regName] = result
        
        if registers[regName] < 0:
            registers[regName] = twos_comp(registers[regName])

        b = format(registers[regName], '016b')

        if b[0] == '1':
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False

    elif inst_type == 'NOP':
        registers[0] += 3
        continue
    elif inst_type == 'PUSH': # ikiye bol ve 
        # Push a word sized operand (two bytes) and update S by subtracting 2.
        b = format(value, '016b')
        f = b[0:8]
        s = b[8:]
        memoryCheck(registers[6]) 
        memory[registers[6]] = f 
        memoryCheck(registers[6]+1) 
        memory[registers[6]+1] = s
        registers[6] -= 2
    elif inst_type == 'POP':
        # Pop a word sized data (two bytes) into the operand and update S by adding 2.
       
        registers[6] += 2
        if registers[6] >= 65536:
            print("stack is empty")
            exit()
        reg = get_register_name(last)
        f = memory[registers[6]]
        s = memory[registers[6] + 1]
        b = f + s
        registers[reg] = int(b, 2)
       
    elif inst_type == 'CMP':
        # cf, sf, zf
        # Perform comparison (AC-operand) and set flag accordingly
      
        result = registers[1] + 65536 - value
        
        if result > reg_max_value:
            result = result - 65536
            cf = True
        else:
            cf = False
        
        b = format(result, '016b')      
        if b[0] == '1':
            sf = True
        else:
            sf = False
        if result == 0:
            zf = True
        else:
            zf = False   
    elif inst_type == 'JMP': # last'ı decimala çevir ve 3'e bol sonra inst_count = orası
        # Unconditional jump. Set PC to address.
        nextInst = getTheInstructionNumber(last)
        registers[0] = nextInst
        isJump = True
        
    elif inst_type == 'JZ':
        # Conditional jump. Jump to address (given as immediate operand) if zero flag is true.
        if(zf):
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'JNZ':
        # Conditional jump. Jump to address (given as immediate operand) if zero flag is false.
        if not zf:
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'JC':
        # Conditional jump. Jump if carry flag is true.
        if cf:
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'JNC':
        # Conditional jump. Jump if carry flag is false.
        if not cf:
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'JA':
        # Conditional jump. Jump if carry flag is false.
        if (not zf) and (not sf):
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'JAE':
        # Conditional jump. Jump if above or equal.
        if not sf:
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'JB':
        # Conditional jump. Jump if below
        if sf:
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'JBE':
        # Conditional jump. Jump if below or equal
        if sf or zf:
            nextInst = getTheInstructionNumber(last)
            registers[0] = nextInst
            isJump = True
    elif inst_type == 'READ':   # 8 BIT ALDIK
        # Reads a character into the operand.
        read_char = input()
        result = ord(read_char)
        if addressing_mode == '01':
            reg_name = get_register_name(last)  
            registers[reg_name] = result
        elif addressing_mode == '10':
            reg = get_register_name(last)
            b = format(result, '016b')
            memoryLoc = registers[reg]
            f = b[0:8]
            s = b[8:]
            memoryCheck(memoryLoc)
            memory[memoryLoc] = f
            memoryCheck(memoryLoc+1)
            memory[memoryLoc+1] = s
        elif addressing_mode == '11':
            dec_value = int(last, 16)
            b = format(result, '016b')
            f = b[0:8]
            s = b[8:]
            memoryCheck(dec_value)
            memory[dec_value] = f
            memoryCheck(dec_value+1)
            memory[dec_value+1] = s
    elif inst_type == 'PRINT':
        # Prints the operand as a character. abi zaten char yazin diyomus biz malmisiz
        print(chr(value))

   
    if not isJump:
        registers[0] += 3
