from numpy.lib.function_base import quantile
from utils import *
import numpy as np


def hex_to_cmd(command: str) -> str:
    """Translates 32 bit MIPS instruction to MIPS command

    Args:
        command (str): hex value to be translated

    Returns:
        str: translated command in MIPS format
    """
    #convert to base 2, check if format is correct
    value = hex_to_bin(command)
    if value == "":
        return "Value not in base 16."
    if len(value) > 34:
        return "Value larger than 32 bit."

    #if value is smaller than 32 bits, add leading zeros
    value = sign_extend(value, 32, k2=False)

    #read opcode
    opcode = bin_to_dec(value[:6], error_msg="Error reading opcode.")

    index = 0
    args = ''

    #get r_type
    if opcode == 0:
        index = 1
        funct = bin_to_dec(value[-6:], error_msg="Error reading funct.")
        rs = bin_to_dec(value[6:11], error_msg="Error reading rs register.")
        rt = bin_to_dec(value[11:16], error_msg="Error reading rt register.")
        rd = bin_to_dec(value[16:21], error_msg="Error reading rd register.")
        shamt = str(bin_to_dec(value[21:27], error_msg="Error reading shamt."))

        #format register names
        rs = "${} (${})".format(registers[rs], rs)
        rt = "${} (${})".format(registers[rt], rt)
        rd = "${} (${})".format(registers[rd], rd)

        #sll, srl format
        if funct == 0x0 or funct == 0x2:
            args = "{}, {}, {}".format(rd, rt, shamt)

        #jr format
        elif funct == 0x8:
            args = rs
        else:
            args = "{}, {}, {}".format(rd, rs, rt)

    #get J type
    elif opcode == 0x2 or opcode == 0x3:
        bin_pc = ""
        while (True):
            #get current program counter
            pc = user_input_convert(base=16,
                                    msg="Current PC (base 16) = ")
            if pc == None:
                continue
            elif pc < 0:
                print("Program counter can't be negative.")
                continue
            pc = pc + 4
            bin_pc = sign_extend(bin(pc)[2:], 32, k2=False)
            if len(bin_pc) > 32:
                print("Input larger than 32 bits.")
            else:
                break

        #get 4 MSBs from program counter + 4...
        msb = bin_pc[0:4]

        #...and 26 immediate bits, shift left << 2...
        imm = value[6:32] + "00"

        #...and concatenate MSBs to get a 32 bit address
        imm = msb + imm
        imm = bin_to_dec(imm, signed=False)
        args = "{} ({})".format(hex(imm), imm)

    #get I type
    else:
        rs = bin_to_dec(value[6:11], error_msg="Error reading rs register.")
        rt = bin_to_dec(value[11:16], error_msg="Error reading rt register.")
        imm = bin_to_dec(value[16:32],
                         error_msg="Error reading immediate.",
                         signed=True)

        #format register names
        rs = "${} (${})".format(registers[rs], rs)
        rt = "${} (${})".format(registers[rt], rt)

        #beq, bne format
        if opcode == 0x4 or opcode == 0x5:
            pc = user_input_convert(base=16,
                                    msg="Current PC (base 16) = ")

            #shift right by 2 and add PC + 4
            imm = (imm * 4) + pc + 4

            args = "{}, {}, {} ({})".format(rs, rt, hex(imm), imm)

        #load and store commands format
        elif opcode == 0x24 or opcode == 0x25 or opcode == 0x30 or opcode == 0x23\
            or opcode == 0x28 or opcode == 0x38 or opcode == 0x2b:
            args = "{}, {}({})".format(rt, imm, rs)
        else:
            args = "{}, {}, {}".format(rt, rs, imm)

    return commands[opcode][index] + " " + args


def cmd_to_hex(cmd: str) -> str:
    """Converts command in MIPS format into hex value (assemble)

    Args:
        cmd (str): MIPS instruction

    Returns:
        str: assembled MIPS instruction in hexadecimal format
    """
    if cmd == "":
        print("Command not found.")
        return "0"

    #get opcode
    opcode, rtype = find_cmd(cmd)
    if opcode == -1:
        print("Command not found.")
        return "0"

    args = ""

    #j, jal format
    label = ""
    if opcode == 0x2 or opcode == 0x3:
        args += sign_extend(bin(opcode)[2:], 6)
        while (True):
            address = user_input_convert(base=16,
                                         msg="Label address (base 16) = ")
            if address < 0:
                print("Label addresses cannot be negative.")
            label = sign_extend(bin(address)[2:], 32, k2=False)
            if len(label) > 32:
                print("Input larger than 32 bits. Try again.")
            else:
                #remove 4 MSBs, shift right >> 2
                label = label[4:-2]
                break
        args += label
    else:
        rd = ""
        rs = ""
        rt = ""
        if rtype:
            rd = input("Rd = ")
            #sll,srl
            if opcode != 0 and opcode != 2:
                rs = input("Rs = ")
            rt = input("Rt = ")
        else:
            if opcode == 4 or opcode == 5:
                rs = input("Rs = ")
                rt = input("Rt = ")
            else:
                rt = input("Rt = ")
                rs = input("Rs = ")
        shamt = 0
        imm = 0
        if rtype:
            funct = opcode
            opcode = 0
            #sll, srl format
            if funct == 0x0 or funct == 0x2:
                shamt = user_input_convert(base=10, msg="Shamt = ")
        else:
            #beq, bne format
            if opcode == 0x4 or opcode == 0x5:
                imm = user_input_convert(base=16,
                                         msg="Branch address (base16) = ")
                pc = user_input_convert(base=16, msg="Current PC (base16) = ")
                #calculate relative address
                imm = (imm - pc - 4) // 4
            else:
                imm = user_input_convert(base=10, msg="Imm = ")

        #find/convert registers
        if rs.isnumeric() == False:
            rs = find_reg(rs)
            if rs == -1:
                print("Register rs not found.")
                return "0"
        else:
            rs = int(rs)
        if rt.isnumeric() == False:
            rt = find_reg(rt)
            if rt == -1:
                print("Register rt not found.")
                return "0"
        else:
            rt = int(rt)
        if rtype:
            if rd.isnumeric() == False:
                rd = find_reg(rd)
                if rd == -1:
                    print("Register rd not found.")
                    return "0"
            else:
                rd = int(rd)

        opcode = bin(opcode)[2:]
        opcode = sign_extend(opcode, 6)
        args += opcode

        rs = bin(rs)[2:]
        rs = sign_extend(rs, 5)
        args += rs

        rt = bin(rt)[2:]
        rt = sign_extend(rt, 5)
        args += rt

        if rtype:
            rd = bin(rd)[2:]
            rd = sign_extend(rd, 5)
            args += rd

            shamt = bin(shamt)[2:]
            shamt = sign_extend(shamt, 5)
            args += shamt

            funct = bin(funct)[2:]
            funct = sign_extend(funct, 6)
            args += funct
        else:
            imm = format(imm & 0xffff, '16b')
            i = 0
            while imm[i] == " ":
                i += 1
            imm = i * "0" + imm[i:]
            args += imm

    return args


def value2cmd(switched: bool = False):
    while True:
        inp = input(
            "\n---------\nEnter command value (base 16 without prefix; m to switch mode; q to quit): "
        )
        if inp == "q":
            exit(0)
        elif inp == "m":
            if switched:
                return
            cmd2value(switched=True)
            continue

        t = hex_to_cmd(inp)
        print("\n", t)


def cmd2value(switched: bool = False):
    while (True):
        inp = input(
            "\n---------\nEnter command (m to switch mode; q to quit): ")
        if inp == "q":
            exit(1)
        elif inp == "m":
            if switched:
                return
            value2cmd(switched=True)
            continue

        t = cmd_to_hex(inp)
        print("\n", t, " ({})\n".format(bin_to_hex(t)))