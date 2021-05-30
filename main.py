import sys

def convert(o,a,op):
    opcode = int(o, 16)
   # addrmode = int(a, 16)
    operand = int(op, 16)

    bopcode = format(opcode, '06b')
  #  baddrmode = format(addrmode, '02b')
    boperand = format(operand, '016b')
    bin = '0b' + bopcode + a + boperand
    ibin = int(bin[2:], 2)
    instr = format(ibin, '06x')
    return instr

def character_to_ascii(c):
    return format(ord(c), "x")

def register_num(ahmet):
    if ahmet == "A" or ahmet == "a":
        return "1"
    elif ahmet == "B" or ahmet == "b":
        return "2"
    elif ahmet == "C" or ahmet == "c":
        return "3"
    elif ahmet == "D" or ahmet == "d":
        return "4"
    elif ahmet == "E" or ahmet == "e":
        return "5"
    elif ahmet == "PC" or ahmet == "pc":
        return "0"
    elif ahmet == "S" or ahmet == "s":
        return "6"        
    else:
        return ahmet

def bin_to_hex(s):
    decimal = int(s, 2)
    return hex(decimal)

def hex_to_bin(s):
    decimal = int(s,16)
    return bin(decimal)

def ishexnum(s):  # ffdc
    if not isnumeric(s[0]):
        return False
    for x in s:
        if (x>'9' or x<'0') and (x>'F' or x<'A') and (x>'f' or x<'a'):
            return False
    return True
            
def ic(s):
    leng = len(s)
    ic = s[1: leng-1]
    return ic

def isnumeric(s):
    for c in s:
        if c>'9' or c<'0':
            return False
    return True

def removeSpaces(s):
    while s[0].isspace():
        s = s[1:]

    while s[-1].isspace():
        leng = len(s)
        s = s[0:leng-1]

    return s

def checkLine(line):
    i = len(line) - 1
    if line[-1] == ':':
        while line[i].isspace():
            i = i-1

        label = line[0:i+1]

        if (' ' in label):
            print("syntax error: invalid label name")
            exit()
    else:
        line = line.strip()
        line = removeSpaces(line)
        tokens = line.split()

        if not(tokens[0] == "HALT") and not(len(tokens) == 2):
            print("invalid instruction")
            exit()


inputFile = open(sys.argv[1], "r")
outputFile = open(sys.argv[1][0:sys.argv[1].index('.')]+".bin", "w")
#outputFile = open("output", "w")
myMap = {}
memoryLoc = 0


for line in inputFile:
    if line.isspace():
        continue
    line = line.strip()
    line = removeSpaces(line)
    tokens = line.split()
    #print str(tokens)

    leng = len(str(tokens[0]))
    if tokens[0][leng-1] == ":" and not isnumeric(tokens[0][0]):
        myMap.update({tokens[0][0:leng-1]:format(memoryLoc, '04x')})
    else:
        memoryLoc += 3

inputFile.close()
inputFile = open(sys.argv[1], "r")

for line in inputFile:
    if line.isspace():
        continue

    line = line.strip()
    tokens = line.split()
    
    if len(tokens) == 3:
        if (tokens[1] == "'" and tokens[2] == "'") or (tokens[1] == '"' and tokens[2] == '"'):
            tokens = [tokens[0], "' '"]

    str = ""
    o = ""
    a = ""
    op = ""
    leng = len(tokens[0])
    tokens[0] = tokens[0].upper()

    if tokens[0][leng-1] == ":":
        continue
    elif tokens[0]=="HALT":
        outputFile.write("040000")
        outputFile.write("\n")
        continue
    elif tokens[0]=="LOAD":
        o = "02"
    elif tokens[0] == "STORE":
        o = "03"
    elif tokens[0] == "ADD":
        o = "04"
    elif tokens[0] == "SUB":
        o = "05"
    elif tokens[0] == "INC":
        o = "06"
    elif tokens[0] == "DEC":
        o = "07"
    elif tokens[0] == "XOR":
        o = "08"
    elif tokens[0] == "AND":
        o = "09"
    elif tokens[0] == "OR":
        o = "0A"
    elif tokens[0] == "NOT":
        o = "0B"
    elif tokens[0] == "SHL":
        o = "0C"
    elif tokens[0] == "SHR":
        o = "0D"
    elif tokens[0] == "NOP":
        o = "0E"
        res = convert(o, "00", "0000")
        outputFile.write(res)
        outputFile.write("\n")
        continue
    elif tokens[0] == "PUSH":
        o = "0F"
    elif tokens[0] == "POP":
        o = "10"
    elif tokens[0] == "CMP":
        o = "11"
    elif tokens[0] == "JMP":
        o = "12"
    elif tokens[0] == "JZ" or tokens[0] == "JE":
        o = "13"
    elif tokens[0] == "JNZ" or tokens[0] == "JNE":
        o = "14"
    elif tokens[0] == "JC":
        o = "15"
    elif tokens[0] == "JNC":
        o = "16"
    elif tokens[0] == "JA":
        o = "17"
    elif tokens[0] == "JAE":
        o = "18"
    elif tokens[0] == "JB":
        o = "19"
    elif tokens[0] == "JBE":
        o = "1A"
    elif tokens[0] == "READ":
        o = "1B"
    elif tokens[0] == "PRINT":
        o = "1C"
    else:
        print("invalid instruction")
        exit()    

    #tokens[1] = tokens[1].upper()

    if isnumeric(tokens[1]) or tokens[1][0] == "'" or (tokens[1].upper() in myMap) or ishexnum(tokens[1]) or tokens[1][0] == '"':
        a = "00"
    elif tokens[1].upper() == "A" or tokens[1].upper() == "B" or tokens[1].upper() == "C" or tokens[1].upper() == "D" or tokens[1].upper() == "E" or tokens[1].upper() == "PC" or tokens[1].upper() == "S":
        a = "01"
    elif tokens[1].upper() == "[A]" or tokens[1].upper() == "[B]" or tokens[1].upper() == "[C]" or tokens[1].upper() == "[D]" or tokens[1].upper() == "[E]" or tokens[1].upper() == "[PC]" or tokens[1].upper() == "[S]":
        a = "10"
    else:
        a = "11"



    if a == "00":
        if (tokens[1][0] == "'" and tokens[1][2] == "'") or (tokens[1][0] == '"' and tokens[1][2] == '"') :
            op = character_to_ascii(tokens[1][1])
        elif (tokens[1].upper() in myMap and not isnumeric(tokens[1][0])):
            op = myMap[tokens[1]]
        else:
            while len(tokens[1]) < 4:
                tokens[1] = '0' + tokens[1]
            if len(tokens[1]) > 4:
                while len(tokens[1]) > 4:
                    if tokens[1][0] == '0':
                        tokens[1] = tokens[1][1:]
                    else:
                        print("wrong immediate data")
                        exit()    
            op = tokens[1]
    
    elif a == "10":
        ic = tokens[1][1:-1]
        op = register_num(ic)

    elif a == "11":
        if tokens[1][0] == "[" and tokens[1][-1] == "]":
            ic = ic(tokens[1])
            while len(ic) < 4:
                ic = '0' + ic
            if len(ic) > 4:
                while len(ic) > 4:
                    if ic[0] == '0':
                        ic = ic[1:]
                    else:
                        print("wrong address")
                        exit()
            op = register_num(ic)
    
    elif a == "01":
        op = register_num(tokens[1])

    if len(o) == 0 or len(a) == 0 or len(op) == 0:
        print("syntax error")
        exit()    
    outputFile.write(convert(o,a,op))
    outputFile.write("\n")
