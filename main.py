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
    if ahmet == "A" or ahmet == "a" :
        return "1"
    elif ahmet == "B" or ahmet == "b":
        return "2"
    elif ahmet == "C" or ahmet == "c":
        return "3"
    elif ahmet == "D" or ahmet == "d":
        return "4"
    elif ahmet == "E" or ahmet == "e":
        return "5"
    else:
        return ahmet

def bin_to_hex(s):
    decimal = int(s, 2)
    return hex(decimal)

def hex_to_bin(s):
    decimal = int(s,16)
    return bin(decimal)

def ishexnum(s):  # ffdc
    
    if s.upper() == 'A' or s.upper() == 'B' or s.upper() == 'C' or s.upper() == 'D' or s.upper() == 'E':
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
    if tokens[0][leng-1] == ":":
        myMap.update({tokens[0][0:leng-1].upper():format(memoryLoc, '04x')})
    else:
        memoryLoc += 3

inputFile.close()
inputFile = open(sys.argv[1], "r")

for line in inputFile:

    if line.isspace():
        continue

    line = line.strip()
    tokens = line.split()
    str = ""
    o = ""
    a = ""
    op = ""
    leng = len(tokens[0])


    if tokens[0][leng-1] == ":":
        continue
    elif tokens[0].upper()=="HALT":
        outputFile.write("040000")
        outputFile.write("\n")
        continue
    elif tokens[0].upper()=="LOAD":
        o = "02"
    elif tokens[0].upper() == "STORE":
        o = "03"
    elif tokens[0].upper() == "ADD":
        o = "04"
    elif tokens[0].upper() == "SUB":
        o = "05"
    elif tokens[0].upper() == "INC":
        o = "06"
    elif tokens[0].upper() == "DEC":
        o = "07"
    elif tokens[0].upper() == "XOR":
        o = "08"
    elif tokens[0].upper() == "AND":
        o = "09"
    elif tokens[0].upper() == "OR":
        o = "0A"
    elif tokens[0].upper() == "NOT":
        o = "0B"
    elif tokens[0].upper() == "SHL":
        o = "0C"
    elif tokens[0].upper() == "SHR":
        o = "0D"
    elif tokens[0].upper() == "NOP":
        o = "0E"
    elif tokens[0].upper() == "PUSH":
        o = "0F"
    elif tokens[0].upper() == "POP":
        o = "10"
    elif tokens[0].upper() == "CMP":
        o = "11"
    elif tokens[0].upper() == "JMP":
        o = "12"
    elif tokens[0].upper() == "JZ" or tokens[0].upper() == "JE":
        o = "13"
    elif tokens[0].upper() == "JNZ" or tokens[0].upper() == "JNE":
        o = "14"
    elif tokens[0].upper() == "JC":
        o = "15"
    elif tokens[0].upper() == "JNC":
        o = "16"
    elif tokens[0].upper() == "JA":
        o = "17"
    elif tokens[0].upper() == "JAE":
        o = "18"
    elif tokens[0].upper() == "JB":
        o = "19"
    elif tokens[0].upper() == "JBE":
        o = "1A"
    elif tokens[0].upper() == "READ":
        o = "1B"
    elif tokens[0].upper()== "PRINT":
        o = "1C"
    else:
        print("invalid instruction")
        exit()


    if isnumeric(tokens[1]) or tokens[1][0] == "'" or (tokens[1].upper() in myMap) or ishexnum(tokens[1]):
        a = "00"
    elif tokens[1] == "A" or tokens[1] == "B" or tokens[1] == "C" or tokens[1] == "D" or tokens[1] == "E" or tokens[1] == "a" or tokens[1] == "b" or tokens[1] == "c" or tokens[1] == "d" or tokens[1] == "e":
        a = "01"
    elif tokens[1] == "[A]" or tokens[1] == "[B]" or tokens[1] == "[C]" or tokens[1] == "[D]" or tokens[1] == "[E]" or tokens[1] == "[a]" or tokens[1] == "[b]" or tokens[1] == "[c]" or tokens[1] == "[d]" or tokens[1] == "[e]":
        a = "10"
    else:
        a = "11"



    if a == "00":
        if tokens[1][0] == "'" and tokens[1][2] == "'":
            op = character_to_ascii(tokens[1][1])
        elif (tokens[1].upper() in myMap):
            op = myMap[tokens[1].upper()]
        else:
            op = tokens[1] #ffdc
    elif a == "10":
        ic = tokens[1][1]
        op = register_num(ic)
    elif a == "11":
        if tokens[1][0] == "[" and tokens[1][-1] == "]" and len(tokens[1]) == 6:
            ic = ic(tokens[1])
            op = register_num(ic)
    elif a == "01":
        op = register_num(tokens[1])


    if len(o) == 0 or len(a) == 0 or len(op) == 0:
        print("syntax error")
        exit()
    outputFile.write(convert(o,a,op))
    outputFile.write("\n")
