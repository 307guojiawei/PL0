import threading
import time
class PCodeVM:
    amax = 2048  # 地址的最大长度
    pCode = {'LIT': 0, 'OPR': 1, 'LOD': 2, 'STO': 3, 'CAL': 4, 'INT': 5, 'JMP': 6, 'JPC': 7}
    pCodeRev = {0: 'LIT', 1: 'OPR', 2: 'LOD', 3: 'STO', 4: 'CAL', 5: 'INT', 6: 'JMP', 7: 'JPC'}

    class Instruction:
        def __init__(self, f, l, a):
            self.f = f
            self.l = l
            self.a = a
            return

    def __init__(self):
        pass

    def base(self,stack,b, l):
        b1 = b
        while l > 0:
            b1 = stack[b1]
            l -= 1
        return b1

    def runPCode(self,code):
        p = 0
        b = 1
        t = 0
        s = list()
        for i in range(PCodeVM.amax):
            s.append(0)
        #s.append(0)

        print("Start PL/0...")
        pCode = code
        try:
            firstFlag = True
            while p!=0 or firstFlag:
                firstFlag = False
                instruct = code[p]
                p += 1
                if instruct.f == PCodeVM.pCode['LIT']:
                    t += 1
                    s[t]=instruct.a
                elif instruct.f == PCodeVM.pCode['OPR']:
                    if instruct.a == 0:
                        t = b-1
                        p = s[t+3]
                        b = s[t+2]
                    elif instruct.a == 1:
                        s[t] = -s[t]
                    elif instruct.a == 2:
                        t = t-1
                        s[t] = s[t]+s[t+1]
                    elif instruct.a == 3:
                        t = t -1
                        s[t] = s[t] - s[t+1]
                    elif instruct.a == 4:
                        t = t-1
                        s[t] = s[t]*s[t+1]
                    elif instruct.a == 5:
                        t = t -1
                        s[t] = s[t] // s[t+1]
                    elif instruct.a == 6:
                        if s[t] %2 == 0:
                            s[t] = 0
                        else:
                            s[t] = 1
                    elif instruct.a == 8:
                        t = t -1
                        if s[t]==s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 9:
                        t = t-1
                        if s[t] == s[t+1]:
                            s[t] = 0
                        else:
                            s[t] = 1
                    elif instruct.a == 10:
                        t = t-1
                        if s[t]<s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 11:
                        t = t - 1
                        if s[t] >= s[t+1]:
                            s[t]=1
                        else:
                            s[t] = 0
                    elif instruct.a == 12:
                        t = t - 1
                        if s[t] > s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 13:
                        t = t - 1
                        if s[t] <= s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 14:
                        print(s[t],end="")
                        t = t-1
                    elif instruct.a == 15:
                        print("")
                    elif instruct.a ==16:
                        t = t + 1
                        s[t] = int(input("->"))
                elif instruct.f == PCodeVM.pCode['LOD']:
                    t = t+1
                    s[t] = s[self.base(s,b,instruct.l) + instruct.a]
                elif instruct.f == PCodeVM.pCode['STO']:
                    s[self.base(s, b, instruct.l) + instruct.a] = s[t]
                    t = t -1
                elif instruct.f == PCodeVM.pCode['CAL']:
                    s[t+1] = self.base(s,b,instruct.l)
                    s[t+2] = b
                    s[t+3] = p
                    b = t+1
                    p = instruct.a

                elif instruct.f == PCodeVM.pCode['INT']:
                    t = t + instruct.a
                elif instruct.f == PCodeVM.pCode['JMP']:
                    p = instruct.a
                elif instruct.f == PCodeVM.pCode['JPC']:
                    if s[t]==0:
                        p = instruct.a
                    t = t-1
        except:
            print("Error")

        print("--------DONE-----------")


from tkinter import *
class PCodeVMGUI(threading.Thread):

    amax = 2048  # 地址的最大长度
    pCode = {'LIT': 0, 'OPR': 1, 'LOD': 2, 'STO': 3, 'CAL': 4, 'INT': 5, 'JMP': 6, 'JPC': 7}
    pCodeRev = {0: 'LIT', 1: 'OPR', 2: 'LOD', 3: 'STO', 4: 'CAL', 5: 'INT', 6: 'JMP', 7: 'JPC'}

    class Instruction:
        def __init__(self, f, l, a):
            self.f = f
            self.l = l
            self.a = a
            return

    class InputQueue:
        def __init__(self):
            self.inputQueue = list()

        def enQueue(self, str):
            self.inputQueue.append(str)

        def deQueue(self):
            return self.inputQueue.pop(0)

        def getLen(self):
            return len(self.inputQueue)

    def __init__(self,code,textField,queue):
        threading.Thread.__init__(self)
        self.inputQueue = self.InputQueue()
        self.textField = textField
        self.code = code
        self.queue = queue

    def setArgs(self,code,textField,queue=None):
        self.textField = textField
        self.code = code
        if queue is not None:
            self.queue = queue



    def __input(self):
        self.__output("请输入数字:")
        ans = self.queue.get(block=True)
        print("->"+str(int(ans)))
        self.__output("-> "+str(int(ans)))
        return ans

    def __output(self,strBuf):
        self.textField.insert(END,str(strBuf))

    def base(self,stack,b, l):
        b1 = b
        while l > 0:
            b1 = stack[b1]
            l -= 1
        return b1

    def run(self):
        code = self.code
        p = 0
        b = 1
        t = 0
        s = list()
        for i in range(PCodeVM.amax):
            s.append(0)
        # s.append(0)

        print("Start PL/0...")
        pCode = code
        try:
            firstFlag = True
            while p != 0 or firstFlag:
                firstFlag = False
                instruct = code[p]
                p += 1
                if instruct.f == PCodeVM.pCode['LIT']:
                    t += 1
                    s[t] = instruct.a
                elif instruct.f == PCodeVM.pCode['OPR']:
                    if instruct.a == 0:
                        t = b - 1
                        p = s[t + 3]
                        b = s[t + 2]
                    elif instruct.a == 1:
                        s[t] = -s[t]
                    elif instruct.a == 2:
                        t = t - 1
                        s[t] = s[t] + s[t + 1]
                    elif instruct.a == 3:
                        t = t - 1
                        s[t] = s[t] - s[t + 1]
                    elif instruct.a == 4:
                        t = t - 1
                        s[t] = s[t] * s[t + 1]
                    elif instruct.a == 5:
                        t = t - 1
                        s[t] = s[t] // s[t + 1]
                    elif instruct.a == 6:
                        if s[t] % 2 == 0:
                            s[t] = 0
                        else:
                            s[t] = 1
                    elif instruct.a == 8:
                        t = t - 1
                        if s[t] == s[t + 1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 9:
                        t = t - 1
                        if s[t] == s[t + 1]:
                            s[t] = 0
                        else:
                            s[t] = 1
                    elif instruct.a == 10:
                        t = t - 1
                        if s[t] < s[t + 1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 11:
                        t = t - 1
                        if s[t] >= s[t + 1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 12:
                        t = t - 1
                        if s[t] > s[t + 1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 13:
                        t = t - 1
                        if s[t] <= s[t + 1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 14:
                        print(s[t], end="")
                        self.__output(s[t])
                        t = t - 1
                    elif instruct.a == 15:
                        print("")
                    elif instruct.a == 16:
                        t = t + 1
                        try:
                            s[t] = int(self.__input())
                        except:
                            print("timeout")
                            return
                elif instruct.f == PCodeVM.pCode['LOD']:
                    t = t + 1
                    s[t] = s[self.base(s, b, instruct.l) + instruct.a]
                elif instruct.f == PCodeVM.pCode['STO']:
                    s[self.base(s, b, instruct.l) + instruct.a] = s[t]
                    t = t - 1
                elif instruct.f == PCodeVM.pCode['CAL']:
                    s[t + 1] = self.base(s, b, instruct.l)
                    s[t + 2] = b
                    s[t + 3] = p
                    b = t + 1
                    p = instruct.a

                elif instruct.f == PCodeVM.pCode['INT']:
                    t = t + instruct.a
                elif instruct.f == PCodeVM.pCode['JMP']:
                    p = instruct.a
                elif instruct.f == PCodeVM.pCode['JPC']:
                    if s[t] == 0:
                        p = instruct.a
                    t = t - 1
        except:
            self.__output("Error Occured")

        print("--------DONE-----------")
        self.__output("执行完毕.")

    def runPCode(self,code):
        p = 0
        b = 1
        t = 0
        s = list()
        for i in range(PCodeVM.amax):
            s.append(0)
        #s.append(0)

        print("Start PL/0...")
        pCode = code
        try:
            firstFlag = True
            while p!=0 or firstFlag:
                firstFlag = False
                instruct = code[p]
                p += 1
                if instruct.f == PCodeVM.pCode['LIT']:
                    t += 1
                    s[t]=instruct.a
                elif instruct.f == PCodeVM.pCode['OPR']:
                    if instruct.a == 0:
                        t = b-1
                        p = s[t+3]
                        b = s[t+2]
                    elif instruct.a == 1:
                        s[t] = -s[t]
                    elif instruct.a == 2:
                        t = t-1
                        s[t] = s[t]+s[t+1]
                    elif instruct.a == 3:
                        t = t -1
                        s[t] = s[t] - s[t+1]
                    elif instruct.a == 4:
                        t = t-1
                        s[t] = s[t]*s[t+1]
                    elif instruct.a == 5:
                        t = t -1
                        s[t] = s[t] // s[t+1]
                    elif instruct.a == 6:
                        if s[t] %2 == 0:
                            s[t] = 0
                        else:
                            s[t] = 1
                    elif instruct.a == 8:
                        t = t -1
                        if s[t]==s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 9:
                        t = t-1
                        if s[t] == s[t+1]:
                            s[t] = 0
                        else:
                            s[t] = 1
                    elif instruct.a == 10:
                        t = t-1
                        if s[t]<s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 11:
                        t = t - 1
                        if s[t] >= s[t+1]:
                            s[t]=1
                        else:
                            s[t] = 0
                    elif instruct.a == 12:
                        t = t - 1
                        if s[t] > s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 13:
                        t = t - 1
                        if s[t] <= s[t+1]:
                            s[t] = 1
                        else:
                            s[t] = 0
                    elif instruct.a == 14:
                        print(s[t],end="")
                        t = t-1
                    elif instruct.a == 15:
                        print("")
                    elif instruct.a ==16:
                        t = t + 1
                        s[t] = int(input("->"))
                elif instruct.f == PCodeVM.pCode['LOD']:
                    t = t+1
                    s[t] = s[self.base(s,b,instruct.l) + instruct.a]
                elif instruct.f == PCodeVM.pCode['STO']:
                    s[self.base(s, b, instruct.l) + instruct.a] = s[t]
                    t = t -1
                elif instruct.f == PCodeVM.pCode['CAL']:
                    s[t+1] = self.base(s,b,instruct.l)
                    s[t+2] = b
                    s[t+3] = p
                    b = t+1
                    p = instruct.a

                elif instruct.f == PCodeVM.pCode['INT']:
                    t = t + instruct.a
                elif instruct.f == PCodeVM.pCode['JMP']:
                    p = instruct.a
                elif instruct.f == PCodeVM.pCode['JPC']:
                    if s[t]==0:
                        p = instruct.a
                    t = t-1
        except:
            print("Error")

        print("--------DONE-----------")
