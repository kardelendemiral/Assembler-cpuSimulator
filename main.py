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
    if ahmet == "A":
        return "1"
    elif ahmet == "B":
        return "2"
    elif ahmet == "C":
        return "3"
    elif ahmet == "D":
        return "4"
    elif ahmet == "E":
        return "5"
    else:
        return ahmet

def bin_to_hex(s):
    decimal = int(s, 2)
    return hex(decimal)

def hex_to_bin(s):
    decimal = int(s,16)
    return bin(decimal)

def ic(s):
    leng = len(s)
    ic = s[1: leng-1]
    return ic

def isnumeric(s):
    for c in s:
        if c>'9' or c<'0':
            return False
    return True


inputFile = open(sys.argv[1], "r")
outputFile = open(sys.argv[1][0:sys.argv[1].index('.')]+".bin", "w")
#outputFile = open("output", "w")
map = {}
memoryLoc = 0


for line in inputFile:
    line = line.strip()
    tokens = line.split(" ")
    #print str(tokens)

    leng = len(str(tokens[0]))
    if tokens[0][leng-1] == ":":
        map.update({tokens[0][0:leng-1]:format(memoryLoc, '04x')})
    else:
        memoryLoc += 3

inputFile.close()
inputFile = open(sys.argv[1], "r")

for line in inputFile:
    line = line.strip()
    tokens = line.split(" ")
    str = ""
    o = ""
    a = ""
    op = ""
    leng = len(tokens[0])


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


    if isnumeric(tokens[1]) or tokens[1][0] == "'" or map.has_key(tokens[1]):
        a = "00"
    elif tokens[1] == "A" or tokens[1] == "B" or tokens[1] == "C" or tokens[1] == "D" or tokens[1] == "E":
        a = "01"
    elif tokens[1] == "[A]" or tokens[1] == "[B]" or tokens[1] == "[C]" or tokens[1] == "[D]" or tokens[1] == "[E]":
        a = "10"
    else:
        a = "11"



    if a == "00":
        if tokens[1][0] == "'":
            op = character_to_ascii(tokens[1][1])
        elif map.has_key(tokens[1]):
            op = map[tokens[1]]
        else:
            op = tokens[1] #buraya MYDATA da gelebilir ama bizce gelmicek
    elif a == "10":
        ic = tokens[1][1]
        op = register_num(ic)
    elif a == "11":
        if tokens[1][0] == "[":
            ic = ic(tokens[1])
            op = register_num(ic)
    elif a == "01":
        op = register_num(tokens[1])

    outputFile.write(convert(o,a,op))
    outputFile.write("\n")

































