class Symbol:
    def __init__(self):
        self.reserved = (
            'begin', 'end', 'if', 'then', 'while',
            'write', 'read', 'do', 'call', 'var',
            'procedure', 'else', 'repeat', 'until','const','odd'
        )
        self.tokens = self.reserved+(
            'nul', 'plus', 'minus', 'mul',
            'div',   'eql', 'neq',
            'lss', 'geq', 'gtr', 'leq', 'lparen',
            'rparen', 'comma', 'semicolon', 'peroid', 'becomes',
             'ident','number'
        )

declbegsys = set( ['const','var','procedure'])
statbegsys = set( ['begin' , 'call' , 'if' , 'while'])
facbegsys = set(['ident','number','lparen'])

