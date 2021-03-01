def get_input(msg : str):
    while True:
        inp = input(msg)
        if inp == "q":
            exit(0)
        if inp == "1":
            return True
        elif inp == "0":
            return False
        else:
            print("\nTry again.")

def main():
    while True:
        ex_rg_write = get_input("EX/MEM.RegWrite = ")
        mem_rg_write = get_input("MEM/WB.RegWrite = ")
        mem_hazard_rs = get_input("MEMHazard Rs = ")
        mem_hazard_rt = get_input("MEMHazard Rt = ")
        wb_hazard_rs = get_input("WBHazard Rs = ")
        wb_hazard_rt = get_input("WBHazard Rt = ")

        fwd_a = "00"
        fwd_b = "00"
        if ex_rg_write:
            if mem_hazard_rs:
                fwd_a = "10"
            if mem_hazard_rt:
                fwd_b = "10"
        if mem_rg_write:
            if not mem_hazard_rs and wb_hazard_rs:
                fwd_a = "01"
            if not mem_hazard_rt and wb_hazard_rt:
                fwd_b = "01"
        print("------------------\nForwardA = {}\nForwardB = {}\n".format(fwd_a, fwd_b))

if __name__ == "__main__":
    main()