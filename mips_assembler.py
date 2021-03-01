from utils import *
import numpy as np

def hex_to_cmd(command, register_names=True):
    #convert to base 2
    value = hex_to_bin(command)
    if value == "":
        return "Value not in base 16."

    #remove 0b from beginning, if there are leading zeros missing, add them
    if len(value) > 34:
        return "Value larger than 32 bit."

    value = sign_extend(value, 32, k2=False)

    #read opcode
    opcode = bin_to_dec(value[:6], error_msg="Error reading opcode.")

    #get r_type
    index = 0
    args = ''
    if opcode == 0:
        index = 1
        opcode = bin_to_dec(value[-6:], error_msg="Error reading funct.")
        rs = bin_to_dec(value[6:11],
                            error_msg="Error reading rs register.")
        rt = bin_to_dec(value[11:16],
                            error_msg="Error reading rt register.")
        rd = bin_to_dec(value[16:21],
                            error_msg="Error reading rd register.")
        shamt = str(
            bin_to_dec(value[21:27], error_msg="Error reading shamt."))

        if register_names == True:
            rs = "$" + registers[rs]
            rt = "$" + registers[rt]
            rd = "$" + registers[rd]
        else:
            rs = "$" + str(rs)
            rt = "$" + str(rt)
            rd = "$" + str(rd)

        #sll, srl
        if opcode == 0 or opcode == 2:
            args = rd + ", " + rt + ", " + shamt
        #jr
        elif opcode == 8:
            args = rs
        else:
            args = rd + ", " + rs + ", " + rt

    #get J type
    elif opcode == 2 or opcode == 3:
        bin_pc = ""
        while(True):
            #PC + 4
            pc = int(input("current PC (base 16) = "), 16) + 4

            bin_pc = sign_extend(bin(pc)[2:], 32, k2=False)
            pc = str(pc)
            if len(pc) > 32:
                print("Input larger than 32 bits. Try again.")
            else:
                break
        #get 4 MSBs
        msb = bin_pc[0:4]

        #get 26 immediate bits, shift left << 2
        imm = value[6:32] + "00"

        # and add MSBs
        imm = msb + imm 
        imm = bin_to_dec(imm, signed=False)
        args = str(hex(imm)) +  "(" + str(imm) + ")"

    #get I type
    else:
        rs = bin_to_dec(value[6:11],
                            error_msg="Error reading rs register.")
        rt = bin_to_dec(value[11:16],
                            error_msg="Error reading rt register.")
        imm = str(
            bin_to_dec(value[16:32],
                           error_msg="Error reading immediate.",
                           signed=True))

        if register_names == True:
            rs = "$" + registers[rs]
            rt = "$" + registers[rt]
        else:
            rs = "$" + str(rs)
            rt = "$" + str(rt)

        #beq, bne
        if opcode == 4 or opcode == 5:
            pc = input("current PC (base 16) = ")
            imm = int(imm) * 4 + int(pc, 16) + 4
            args = rs + ", " + rt + ", " + hex(imm)
        #load commands
        elif opcode == 0x24 or opcode == 0x25 or opcode == 0x30 or opcode == 0x23:
            args = rt + ", " + imm + "(" + rs + ")"
        #store commands
        elif opcode == 0x28 or opcode == 0x38 or opcode == 0x2b:
            args = rt + ", " + imm + "(" + rs + ")"
        else:
            args = rt + ", " + rs + ", " + imm

    cmd_name = commands[opcode][index]
    return cmd_name + " " + args





def cmd_to_hex(cmd: str):
    if cmd == "":
        print("Command not found.") 
        return "0"
    opcode, rtype = find_cmd(cmd)
    if opcode == -1:
        print("Command not found.") 
        return "0"

    args = ""

    #j, jal
    label = ""
    if opcode == 2 or opcode == 3:
        args += sign_extend(bin(opcode)[2:], 6)
        while(True):
            label = sign_extend(bin(int(input("Label address (base 16)= "), 16))[2:],
                            32,
                            k2=False)
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
            rd = input("rd = ")
            #sll,srl
            if opcode != 0 and opcode != 2:
                rs = input("rs = ") 
            rt = input("rt = ")
        else:
            rt = input("rt = ")
            rs = input("rs = ")
        shamt = ""
        imm = ""
        if rtype:
            shamt = input("shamt = ")
            if shamt == " " or shamt == "":
                shamt = "0"
            funct = opcode
            opcode = 0
        else:
            if opcode == 4 or opcode == 5:
                imm = input("Branch address (base16) = ")
                pc = input("Current PC (base16) = ")
                try:
                    imm = (int(imm,16) - (int(pc,16) + 4)) // 4
                except ValueError:
                    print("Failed to convert immediate.")
                    return "0"
            else:
                try:
                    imm = int(input("imm = "))
                except ValueError:
                    print("Failed to convert immediate.")
                    return "0"
                if imm == " " or imm == "":
                    imm = "0"

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
        

        try:

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
                shamt = bin(int(shamt))[2:]
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
            #print(cmd, opcode, rs, rt,  rd,  shamt, funct)

        except ValueError:
            print("Error converting registers.")
            return "0"
    return args


def value2cmd():
    reg = input("Would you like register names? (y/n; m for menu; q to quit): ")
    reg_names = False
    if reg == "q":
        exit(1)
    elif reg == "m":
        return
    if reg == "y" or reg == "Y":
        reg_names = True

    while True:
        inp = input(
            "\n---------\nEnter command value (base 16 without prefix; m for menu; q to quit): ")
        if inp == "q":
            exit(1)
        elif inp == "m":
            return
        t = hex_to_cmd(inp, register_names=reg_names)
        print("\n", t)


def cmd2value():
    while (True):
        inp = input("\n---------\nEnter command (m for menu; q to quit): ")
        if inp == "q":
            exit(1)
        elif inp == "m":
            return
    
        t = cmd_to_hex(inp)
        print("\n", t, " ({})\n".format(bin_to_hex(t)))