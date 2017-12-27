# PL/0文法翻译以及P-code代码生成
import Symbol
import Define
import Scanner
import copy



#定义单例模式
class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._inst

class Error:
    def __init__(self,line,msg):
        self.line = line
        self.msg = msg

    def getErr(self):
        return str(self.line)+" -> "+self.msg

'''
Attribute类
-定义并保存编译时使用的变量
-采用单例模式
'''
class Attribute(Singleton):
    def __init__(self):
        self.char = ' '  # 最后一次读出来的字符 ch
        self.sym = 0  # 最后一次是别的token类型 sym
        self.id = ''  # 最后一次识别出的标识符 id
        self.number = 0  # 最后一次识别出的数字 num
        self.scanner = None
        self.char_count = 0  # 字母计数 cc
        self.line_number = 0  # 行号
        self.errors = 0
        self.cx = 0  # 代码分配指针 cx
        self.a = ''  # 正在分析的词 a
        self.code = []  # 指令表 code
        self.file_content = []  # 文本内容
        self.dx = 0  # 数据分配指针
        self.lev = 0  # 当前的块深度
        self.tx = 0  # 当前的符号表指针
        self.stack = []  # 数据栈
        self.table = [Define.Table()]  # 符号表
        self.token = None
        self.errList = list()
        for i in range(Define.txmax):
            self.table.append(Define.Table())

'''
PL0
-编译器控制类

'''
class PL0:
    def __init__(self, address):
        self.baseTool = BaseTool()
        self.parser = Parser()
        self.baseTool.initLexParser(address)
        self.pCodeStr = ""

    #开始编译
    def start(self):
        print("Start Compile.....")
        self.baseTool.getSym()
        self.parser.block(set(["peroid"]) | Symbol.declbegsys | Symbol.statbegsys)
        if self.parser.attr.sym != "peroid":
            #print(self.parser.attr.sym)
            self.baseTool.error(9)
        print("Done.")
        print("-----------P-CODE-----------")
        self.pCodeStr=self.parser.tool.listcode(0)

    #返回PCode List对象
    def getPCode(self):
        return self.parser.getPCode()

    #返回转换过的PCode String
    def getPCodeStr(self):
        return self.pCodeStr

    #返回错误数量
    def getErr(self):
        return self.baseTool.attr.errors

    #返回错误列表List
    def getErrList(self):
        return self.baseTool.getErrList()

"""
BaseTool工具类
-定义一些编译器常用的方法
"""
class BaseTool:
    def __init__(self):
        self.attr = Attribute()

    #初始化词法分析
    def initLexParser(self,address):
        self.attr.scanner = Scanner.getScanner(address)

    #获得目前的符号
    def getSym(self):
        self.attr.token = self.attr.scanner.token()
        if self.attr.token is None:
            self.attr.sym = None
            return
        self.attr.sym = self.attr.token.type
        #print(dir(token))
        self.attr.line_number = self.attr.token.lineno
        if self.attr.token.type == "ident":
            self.attr.id = self.attr.token.value
        if self.attr.token.type == "number":
            self.attr.number = self.attr.token.value

    #errror(self,n) -报告错误并记录
    #Note: n代表错误编号，在Define中定义
    def error(self,n):
        self.attr.errors +=1
        if n!=0:
            print("**** {}:{} -> {}".format(self.attr.line_number,n,Define.error_message[n]))
            err = Error(self.attr.line_number,Define.error_message[n])
            self.attr.errList.append(err)

    #返回错误list
    def getErrList(self):
        return self.attr.errList

    #生成代码
    def gen(self,x , y, z):
        if self.attr.cx > Define.cxmax:
            print("程序过长")
            raise "程序过长"
        codeItem = Define.Instruction(x,y,z)
        codeItem.source = self.attr.token
        self.attr.code.append(codeItem)
        self.attr.cx = self.attr.cx+1

    #列出代码,并返回代码的String
    def listcode(self,cx0):
        strBuf = ""
        for i in range(cx0, self.attr.cx):
            print(str(i)+' '+Define.pCodeRev[self.attr.code[i].f] + ' ' + str(self.attr.code[i].l) + ' ' + str(self.attr.code[i].a))
            #print(Define.pCodeRev[self.attr.code[i].f] + ' ' + str(self.attr.code[i].l) + ' ' + str(self.attr.code[i].a))
            strBuf += Define.pCodeRev[self.attr.code[i].f] + ' ' + str(self.attr.code[i].l) + ' ' + str(self.attr.code[i].a)+"\n"
        return strBuf
    #输出符号表
    def printTable(self):
        print("|--------table-----------")
        print("|a\tl\tv\tk\tn")
        print("|------------------------")
        for item in self.attr.table:
            if item.kind != 0 :
                print("|{}\t{}\t{}\t{}\t{}".format(item.address, item.level, item.value, item.kind[0:1], item.name))
    #输出符号表从0到tx部分
    def printTable1(self,tx):
        print("")
        for i in range(1,tx+1):
            item = self.attr.table[i]
            print("|{}\t{}\t{}\t{}\t{}".format(item.address, item.level, item.value, item.kind[0:1], item.name))

#Parser - PL/0语法分析
class Parser:
    def __init__(self):
        self.attr = Attribute()
        self.tool = BaseTool()

    #返回生成的PCode
    def getPCode(self):
        return self.attr.code

    #向后测试跳读
    def test(self,s1,s2,n):
        ss1 = s1
        ss2 = s2
        if  self.attr.sym  not in ss1:
            self.tool.error(n)
            ss1 = ss1 | ss2
            while not self.attr.sym in ss1 and self.attr.sym!=None:
                self.tool.getSym()

    #填入符号表
    def enter(self,k):
        self.attr.tx += 1
        item = Define.Table()
        item.name = self.attr.id
        item.kind = k
        if k == 'constant':
            if self.attr.number > Define.amax:
                self.tool.error(30)
                self.attr.number = 0
            item.value = self.attr.number
        if k == "variable":
            item.level = self.attr.lev
            item.address = self.attr.dx
            self.attr.dx = self.attr.dx+1
        if k == "procedure":
            item.level = self.attr.lev
        self.attr.table[self.attr.tx] = item

    #返回id对应在符号表中的位置，如果符号表不存在则返回0
    def position(self,id):
        self.attr.table[0].name = id
        i = self.attr.tx
        while self.attr.table[i].name != id:
            i = i-1
        return i

    #const定义部分
    def constDeclaration(self):

        if self.attr.sym == "ident":
            self.tool.getSym()
            if self.attr.sym in ("eql","becomes"):
                if self.attr.sym == "becomes":
                    self.tool.error(1)
                self.tool.getSym()
                if self.attr.sym == "number":
                    self.enter("constant")
                    self.tool.getSym()
                else:
                    self.tool.error(2)
            else:
                self.tool.error(3)
        else:
            self.tool.error(4)

    #变量定义
    def varDeclaration(self):

        if self.attr.sym == "ident":
            self.enter("variable")
            self.tool.getSym()
        else:
            self.tool.error(4)


    def factor(self,fsys):

        i = 0
        self.test(set(Symbol.facbegsys) , fsys ,24)
        while self.attr.sym in Symbol.facbegsys:
            if self.attr.sym == "ident":
                i = self.position(self.attr.id)
                if i == 0:
                    self.tool.error(11)

                else:
                    if self.attr.table[i].kind == "constant":
                        self.tool.gen(Define.pCode['LIT'],0,self.attr.table[i].value)
                    if self.attr.table[i].kind == "variable":
                        self.tool.gen(Define.pCode['LOD'], self.attr.lev - self.attr.table[i].level, self.attr.table[i].address)
                    if self.attr.table[i].kind == "procedure":
                        self.tool.error(21)
                self.tool.getSym()
            elif self.attr.sym == "number":
                if self.attr.number > Define.amax:
                    self.tool.error(30)
                    self.attr.number = 0
                self.tool.gen(Define.pCode['LIT'],0,self.attr.number)
                self.tool.getSym()
            elif self.attr.sym == "lparen":
                self.tool.getSym()
                self.expression(set(["rparen"])|fsys)
                if self.attr.sym == "rparen":
                    self.tool.getSym()
                else:
                    self.tool.error(22)
                self.test(fsys,set(["lparen"]),23)

    def term(self, fsys):
        mulop = ''
        self.factor(fsys | set(['mul','div']))
        while self.attr.sym in {'mul','div'}:
            mulop = self.attr.sym
            self.tool.getSym()
            self.factor(fsys | {'mul','div'})
            if mulop == "mul":
                self.tool.gen(Define.pCode['OPR'],0,4)
            else:
                self.tool.gen(Define.pCode['OPR'],0,5)

    def expression(self, fsys):
        addop = ''
        if self.attr.sym in {'plus','minus'}:
            addop = copy(self.attr.sym)
            self.tool.getSym()
            self.term(fsys | {'plus','minus'})
            if addop == "minus":
                self.tool.gen(Define.pCode['OPR'],0,1)
        else:
            self.term(fsys | {'plus','minus'})
        while self.attr.sym in ['plus','minus']:
            addop = self.attr.sym
            self.tool.getSym()
            self.term(fsys | {'plus','minus'})
            if addop == "plus":
                self.tool.gen(Define.pCode['OPR'],0,2)
            else:
                self.tool.gen(Define.pCode['OPR'],0,3)

    def condition(self,fsys):
        relop = ''
        if self.attr.sym == "odd":
            self.tool.getSym()
            self.expression(fsys)
            self.tool.gen(Define.pCode['OPR'],0,6)
        else:
            self.expression({'eql','neq','lss','gtr','leq','geq'} | fsys)
            if self.attr.sym not in {'eql','neq','lss','gtr','leq','geq'}:
                self.tool.error(20)
            else:
                relop = self.attr.sym
                self.tool.getSym()
                self.expression(fsys)
                if relop == "eql":
                    self.tool.gen(Define.pCode['OPR'],0,8)
                if relop == "neq":
                    self.tool.gen(Define.pCode['OPR'],0,9)
                if relop == "lss":
                    self.tool.gen(Define.pCode['OPR'],0,10)
                if relop == "geq":
                    self.tool.gen(Define.pCode['OPR'],0,11)
                if relop == "gtr":
                    self.tool.gen(Define.pCode['OPR'],0,12)
                if relop == "leq":
                    self.tool.gen(Define.pCode['OPR'],0,13)

    def statement(self,fsys):
        if self.attr.sym == "ident":
            i = self.position(self.attr.id)
            if i == 0:
                self.tool.error(11)

            elif  self.attr.table[i].kind != "variable":
                self.tool.error(12)
                i = 0
            self.tool.getSym()
            if self.attr.sym == "becomes":
                self.tool.getSym()
            else:
                self.tool.error(13)
            self.expression(fsys)
            if i != 0:
                item = self.attr.table[i]
                self.tool.gen(Define.pCode['STO'],self.attr.lev-item.level,item.address)
        elif self.attr.sym == "call":
            self.tool.getSym()
            if self.attr.sym != "ident":
                error(14)
            else:
                i = self.position(self.attr.id)
                if i == 0:
                    self.tool.error(11)

                else:
                    item = self.attr.table[i]
                    if item.kind == "procedure":
                        self.tool.gen(Define.pCode['CAL'],self.attr.lev - item.level,item.address)
                    else:
                        self.tool.error(15)
                    self.tool.getSym()
        elif self.attr.sym == "if":
            self.tool.getSym()
            self.condition({'then','do'} | fsys)
            if self.attr.sym == "then":
                self.tool.getSym()
            else:
                self.tool.error(16)
            cx1 = self.attr.cx
            self.tool.gen(Define.pCode['JPC'],0,0)
            self.statement(fsys)
            if self.attr.sym == "else":
                self.attr.getsym()
                cx2 = self.attr.cx
                self.tool.gen(define.p_code['JMP'], 0, 0)
                self.attr.code[cx1].a = self.attr.cx
                self.tool.statement(fsys)
                self.attr.code[cx2].a = self.attr.cx
            else:
                self.attr.code[cx1].a = self.attr.cx
        elif self.attr.sym == "begin":
            self.tool.getSym()
            self.statement(set(['semicolon','endsym']) | fsys)
            while self.attr.sym in {'semicolon'} | Symbol.statbegsys:
                if self.attr.sym == "semicolon":
                    self.tool.getSym()
                else:
                    self.tool.error(10)
                self.statement({'semicolon','endsym'} | fsys)
            if self.attr.sym == "end":
                self.tool.getSym()
            else:
                self.tool.error(17)
        elif self.attr.sym == "while":
            cx1 = self.attr.cx
            self.tool.getSym()
            self.condition({'do'} | fsys)
            cx2 = self.attr.cx
            self.tool.gen(Define.pCode['JPC'],0,0)
            if self.attr.sym == "do":
                self.tool.getSym()
            else:
                self.tool.error(18)
            self.statement(fsys)
            self.tool.gen(Define.pCode['JMP'],0,cx1)
            self.attr.code[cx2].a = self.attr.cx
        elif self.attr.sym == "read":
            self.tool.getSym()
            if self.attr.sym == "lparen":
                firstFlag = True
                while firstFlag or self.attr.sym == "comma":
                    firstFlag = False
                    self.tool.getSym()
                    if self.attr.sym == "ident":
                        i = self.position(self.attr.id)
                        if i == 0:
                            self.tool.error(11)
                        elif self.attr.table[i].kind != "variable":
                            self.tool.error(12)
                            i = 0
                        else:
                            item = self.attr.table[i]
                            self.tool.gen(Define.pCode['OPR'], 0, 16)
                            self.tool.gen(Define.pCode['STO'], self.attr.lev - self.attr.table[i].level, self.attr.table[i].address)

                            #self.tool.gen(Define.pCode['RED'],self.attr.lev - item.level,item.address)
                    else:
                        self.tool.error(4)
                    self.tool.getSym()
            else:
                self.tool.error(40)
            if self.attr.sym != "rparen":
                self.tool.error(22)
            self.tool.getSym()
        elif self.attr.sym == "write":
            self.tool.getSym()
            if self.attr.sym == "lparen":
                firstFlag = True
                while firstFlag or self.attr.sym == "comma":
                    firstFlag = False
                    self.tool.getSym()
                    self.expression({'rparen','comma'} | fsys)
                    self.tool.gen(Define.pCode['OPR'], 0, 14)
                    self.tool.gen(Define.pCode['OPR'], 0, 15)
                    #self.tool.gen(Define.pCode['WRT'],0,0)
                if self.attr.sym != "rparen":
                    self.tool.error(22)
                self.tool.getSym()
            else:
                self.tool.error(40)
        elif self.attr.sym == "repeat":
            self.tool.getSym()
            cx1 = self.attr.cx
            self.statement(fsys | {"semicolon" ,"until"})
            while self.attr.sym in {"semicolon"} | Symbol.statbegsys:
                if self.attr.sym == "semicolon":
                    self.tool.getSym()
                else:
                    self.tool.error(10)
                self.statement(fsys | {"semicolon",'until'})
            if self.attr.sym == "until":
                self.tool.getSym()
            else:
                self.tool.error(19)
            self.condition(fsys)
            self.tool.gen(Define.pCode['JPC'], 0, cx1)
        self.test(fsys,set(),19)

    def block(self,fsys):
        self.attr.dx = 3
        tx0 = self.attr.tx
        cx0 = 0
        self.attr.table[self.attr.tx].address = self.attr.cx
        self.tool.gen(Define.pCode['JMP'],0,0)
        if self.attr.lev > Define.levmax:
            self.tool.error(32)

        while True:
            if self.attr.sym == "const":
                self.tool.getSym()
                self.constDeclaration()
                while self.attr.sym == "comma":
                    self.tool.getSym()
                    self.constDeclaration()
                if self.attr.sym == "semicolon":
                    self.tool.getSym()
                else:
                    self.tool.error(5)
            if self.attr.sym == "var":
                self.tool.getSym()
                self.varDeclaration()
                while self.attr.sym == "comma":
                    self.tool.getSym()
                    self.varDeclaration()
                if self.attr.sym == "semicolon":
                    self.tool.getSym()
                else:
                    self.tool.error(5)
            while self.attr.sym == "procedure":
                self.tool.getSym()
                if self.attr.sym == "ident":
                    self.enter("procedure")
                    self.tool.getSym()
                else:
                    self.tool.error(4)
                if self.attr.sym == "semicolon":
                    self.tool.getSym()
                else:
                    self.tool.error(5)

                #print("start block")
                self.attr.lev += 1
                tx1 = self.attr.tx
                dx1 = self.attr.dx
                self.block({"semicolon"} | fsys)
                self.attr.dx = dx1
                self.attr.tx = tx1
                self.attr.lev -= 1
                #print("end block:"+str(self.attr.lev))

                if self.attr.sym == "semicolon":
                    self.tool.getSym()
                    self.test(Symbol.statbegsys | {"ident" , "procedure"},fsys,6)
                else:
                    self.tool.error(5)
            self.test(Symbol.statbegsys | set(["ident"]),Symbol.declbegsys,7)
            if self.attr.sym not in Symbol.declbegsys:
                break
        self.attr.code[self.attr.table[tx0].address].a = self.attr.cx
        self.attr.table[tx0].address = self.attr.cx
        cx0 = self.attr.cx
        self.tool.gen(Define.pCode['INT'],0,self.attr.dx)
        self.statement(set(["semicolon","end"]) | fsys)
        self.tool.gen(Define.pCode['OPR'],0,0)
        self.test(fsys,set(),0)
        #self.tool.printTable1(self.attr.tx)

        #self.tool.listcode(cx0)
        #print("")







