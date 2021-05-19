import sys

def convert(o,a,op):
    opcode = int(o, 16)
    addrmode = int(a, 16)
    operand = int(op, 16)

    bopcode = format(opcode, '06b')
    baddrmode = format(addrmode, '02b')
    boperand = format(operand, '016b')
    bin = '0b' + bopcode + baddrmode + boperand
    ibin = int(bin[2:], 2);
    instr = format(ibin, '06x')
    return instr


def bin_to_hex(s):
    decimal = int(s, 2)
    return hex(decimal)

def hex_to_bin(s):
    decimal = int(s,16)
    return bin(decimal)


inputFile = open(sys.argv[1], "r")
#outputFile = open(sys.argv[1][0:sys.argv[1].index('.')]+".bin")
outputFile = open("output", "w")
variables = [None] * 65536
memoryLoc = 0

for line in inputFile:
    line = line.strip()
    tokens = line.split(" ")
    #print str(tokens)

    leng = len(str(tokens[0]))
    if tokens[0][leng-1] == ":":
        variables[memoryLoc] = tokens[0][0:leng-1]
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
        o = "1"
    elif tokens[0]=="LOAD":
        o = "2"
    elif tokens[0] == "STORE":
        o = "3"
    elif tokens[0] == "ADD":
        o = "4"
    elif tokens[0] == "SUB":
        o = "5"
    elif tokens[0] == "INC":
        o = "6"
    elif tokens[0] == "DEC":
        o = "7"
    elif tokens[0] == "XOR":
        o = "8"
    elif tokens[0] == "AND":
        o = "9"
    elif tokens[0] == "OR":
        o = "A"
    elif tokens[0] == "NOT":
        o = "B"
    elif tokens[0] == "SHL":
        o = "C"
    elif tokens[0] == "SHR":
        o = "D"
    elif tokens[0] == "NOP":
        o = "E"
    elif tokens[0] == "PUSH":
        o = "F"
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


    if len(tokens) == 2:
        if isinstance(tokens[1], int) or tokens[1][0] == "'":
            a = "00"
        elif tokens[1] == "A" or tokens[1] == "B" or tokens[1] == "C" or tokens[1] == "D":
            a = "01"
        elif tokens[1] == "[A]" or tokens[1] == "[B]" or tokens[1] == "[C]" or tokens[1] == "[D]":
            a = "10"
        else:
            a = "11"
















