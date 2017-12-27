import Scanner
import Symbol
import lex

from PL0 import *
from PCodeVM import PCodeVM



def main():

    pl0 = PL0("test2.txt")
    pl0.start()
    print("--------------------")
    if pl0.getErr()>0:
        print("Errors Occured")
        exit(2)
    pcode = pl0.getPCode()
    vm = PCodeVM()
    vm.runPCode(pcode)





if __name__ == '__main__':
    main()
