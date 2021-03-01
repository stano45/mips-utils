from mips_assembler import *

def main():
    while True:
        inp = input("\nValue to command? (y/n; q to quit): ")
        if inp == "q":
            exit(0)
        
        if inp == "y":
            value2cmd()
        else:
            cmd2value()


if __name__ == "__main__":
    main()