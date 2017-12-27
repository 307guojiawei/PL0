
# 一些常量定义
norw = 13 # 保留字的数量
txmax = 100 #符号表的长度
nmax = 14 #数字的最大位数
al = 10 #id的最大长度
amax = 2047 #地址的最大长度
levmax = 3 # 程序块的最大深度
cxmax = 2048 # 代码数组的最大大小

# 一些类型的定义
class Instruction:
    def __init__(self, f, l , a):
        self.f = f
        self.l = l
        self.a = a
        self.source = ''
        return

error_message = (
    "",
    "Found ':=' when expecting '='.",
    "There must be a number to follow '='.",
    "There must be an '=' to follow the identifier.",
    "There must be an identifier to follow 'const', 'var', or 'procedure'.",
    "Missing ',' or ';'.",
    "Incorrect procedure name.",
    "Statement expected.",
    "Follow the statement is an incorrect symbol.",
    "'.' expected.",
    "';' expected.",
    "Undeclared identifier.",
    "Illegal assignment.",
    "':=' expected.",
    "There must be an identifier to follow the 'call'.",
    "A constant or variable can not be called.",
    "'then' expected.",
    "';' or 'end' expected.",
    "'do' expected.",
    "Incorrect symbol.",
    "Relative operators expected.",
    "Procedure identifier can not be in an expression.",
    "Missing ')'.",
    "The symbol can not be followed by a factor.",
    "The symbol can not be as the beginning of an expression.",
    "",
    "",
    "",
    "",
    "",
    "",
    "The number is too great.",
    "There are too many levels.",
    "There should be a right paren.",
    "There should be a left paren."
)

#符号表对象
class Table:
    def __init__(self):
        self.name = ''  #名称
        self.kind = 0   #类型
        self.value = 0  #值
        self.level = 0  #层
        self.address = 0#地址，var 和procedure使用
        return

objectType = {'constant': 0, 'variable': 1, 'procedure': 2}
pCode = {'LIT': 0, 'OPR': 1, 'LOD': 2, 'STO': 3, 'CAL': 4, 'INT': 5, 'JMP': 6, 'JPC': 7}
pCodeRev = {0: 'LIT', 1: 'OPR', 2: 'LOD', 3: 'STO', 4: 'CAL', 5: 'INT', 6: 'JMP', 7: 'JPC'}



#一些控制参数
show_control_detail = True   #

