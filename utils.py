import numpy as np

commands = np.array([['', 'sll'], ['', ''], ['j', 'srl'], ['jal', 'sra'],
                ['beq', 'sllv'], ['bne', ''], ['blez', 'srlv'], ['bgtz', 'srav'],
                ['addi', 'jr'], ['addiu', 'jalr'], ['slti', 'movz'],
                ['sltiu', 'movn'], ['andi', 'syscall'], ['ori', 'break'],
                ['xori', ''], ['lui', 'sync'], ['', 'mfhi'], ['', 'mthi'],
                ['', 'mflo'], ['', 'mtlo'], ['', ''], ['', ''], ['', ''],
                ['', ''], ['', 'mult'], ['', 'multu'], ['', 'div'], ['', 'divu'],
                ['', ''], ['', ''], ['', ''], ['', ''], ['lb', 'add'],
                ['lh', 'addu'], ['lwl', 'sub'], ['lw', 'subu'], ['lbu', 'and'],
                ['lhu', 'or'], ['lwr', 'xor'], ['', 'nor'], ['sb', ''],
                ['sh', ''], ['swl', 'slt'], ['sw', 'sltu'], ['', ''], ['', ''],
                ['swr', ''], ['cache', ''], ['ll', 'tge'], ['lwc1', 'tgeu'],
                ['lwc2', 'tlt'], ['pref', 'tltu'], ['', 'teq'], ['ldc1', ''],
                ['ldc2', 'tne'], ['', ''], ['sc', ''], ['swc1', ''],
                ['swc2', ''], ['', ''], ['', ''], ['sdc1', ''], ['sdc2', ''],
                ['', '']])

registers = np.array([
    'zero', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3', 't0', 't1', 't2', 't3',
    't4', 't5', 't6', 't7', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7',
    't8', 't9', 'k0', 'k1', 'gp', 'sp', 'fp', 'ra'
])

def find_reg(name: str):
    if name == "" or name == " " or name == "0":
        return 0
    for i in range(len(registers)):
        if registers[i] == name:
            return i
    return -1


def find_cmd(cmd: str):
    for i in range(len(commands)):
        if commands[i][0] == cmd:
            return i, False
        elif commands[i][1] == cmd:
            return i, True
    return -1, False


def bin_to_hex(num: str):
    res = ""
    for i in range(0, len(num), 4):
        try:
            res = res + hex(int(num[i:i + 4], 2))[2:]
        except ValueError:
            print("ValueError in bin_to_hex, string = {}.\n".format(num))
            return
    return "0x" + res

def bin_to_dec(n: str, error_msg="Could not convert number.", signed=False):
    res = 0
    neg = 1
    if signed:
        neg = -1
    for i in range(len(n)):
        if n[i] == "1":
            res += (2**(len(n) - i - 1))
            if i == 0:
                res *= neg
        elif n[i] == "0":
            continue
        else:
            print(error_msg)
            raise ValueError

    return res


def sign_extend(num: str, n, k2=False):
    if k2:
        sign = num[0]
    else:
        sign = "0"
    num = ((n - len(num)) * sign) + num
    return num


def hex_to_bin(num: str):
    res = ""
    for i in range(0, len(num)):
        try:
            res = res + sign_extend(bin(int(num[i], 16))[2:], 4)
        except ValueError:
            print("Value error in hex_to_bin. String = {}\n".format(num))
            return ""
    return res
