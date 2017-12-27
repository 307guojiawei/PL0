import Scanner
import Symbol
import lex

from PL0 import *
from PCodeVM import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import queue

class PCodeVMApp():
    def __init__(self,master,pcode):
        self.master = master
        self.pcode = pcode
        self.create_widgets()
        self.queue = queue.Queue()
        self.vm = PCodeVMGUI(None,None,None)


    def create_widgets(self):
        vmFrame = Toplevel(self.master)
        vmFrame.resizable(width=False, height=False)
        consoleFrame = Frame(vmFrame)

        scrolly = Scrollbar(consoleFrame)
        scrolly.grid(row=0, column=1, sticky=(N, S, E))
        self.consoleField = Listbox(consoleFrame, width=84, height=20,yscrollcommand=scrolly.set)
        self.consoleField.grid(row=0,column=0,sticky=(W,N))
        scrolly.config(command=self.consoleField.yview)

        consoleFrame.grid(row=0, column=0, sticky=(W, N,E))

        commandFrame=Frame(vmFrame)
        commandLabel = Label(commandFrame)
        commandLabel['text'] = "命令:"
        commandLabel.grid(row=0,column=0,sticky=(W))
        self.commandField = Entry(commandFrame,width=79)
        self.commandField.grid(row=0,column=1)
        self.commandField.focus()
        button = Button(commandFrame,command=self.getInputCommand)
        button['text'] = "执行"
        self.commandField.bind("<Key>",self.getInputCommand)
        #button.grid(row=0,column=2)
        commandFrame.grid(row=1,sticky=(W,E,S))

    def getInputCommand(self,event):
        #print(event.keysym)
        if event.keysym == "Return" or event.keysym == "KP_Enter":
            buf=self.commandField.get()
            try:
                buf2 = int(buf)
                self.queue.put(buf)
                self.commandField.delete(0,len(buf))
            except:
                messagebox.askokcancel("错误","输入非法字符")



    def start(self):
        self.vm.setArgs(self.pcode, self.consoleField,self.queue)
        self.vm.setDaemon(True)
        self.vm.start()






class Application():

    def __init__(self, master=None):
        self.master = master
        self.create_widgets()
        self.sourceCode = StringVar()
        self.pl0 = None


    def pCodeVM(self):
        if self.pl0 is not None:
            vm = PCodeVMApp(self.master,self.pl0.getPCode())
            vm.start()

    def authorInfo(self):
        messagebox.askokcancel("关于本程序","作者：郭嘉伟 15051092")

    def errSelectHandler(self,event):
        count = 0
        strBuf=""
        for count in range(0,self.errText.size()):
            if self.errText.selection_includes(count):
                strBuf=self.errText.get(count)
                break
            count+=1
        if strBuf != "":
            buf=strBuf.split(" ->")
            line=buf[0]
            buffer = self.sourceCodeFiled.get("1.0","end")
            self.sourceCodeFiled.delete("1.0", "end")
            self.sourceCodeFiled.insert("1.0", buffer)
            self.sourceCodeFiled.tag_add("err",line+".0",line+".end")


    def displayErr(self,errList):
        errFrame = Toplevel(self.master)
        errFrame.resizable(width=False, height=False)
        errFrame.title = "错误列表"
        errTitle = Label(errFrame)
        errTitle["text"]="错误列表"
        errTitle.grid(row=0,column=0,sticky=(N))
        self.errText = Listbox(errFrame,width=80)


        for err in errList:
            self.errText.insert(END,err.getErr())
        self.errText.bind("<Button-1>",self.errSelectHandler)
        self.errText.grid(row=1,column = 0,sticky=(S))


    #打开源码文件
    def openFile(self):
        fileName=filedialog.askopenfilename()
        print(fileName)
        if fileName != () and fileName is not None:
            fd = open(fileName,"r")
            self.sourceCode.set(fd.read())
            fd.close()
            self.sourceCodeFiled.delete("1.0","end")
            self.sourceCodeFiled.insert("1.0",self.sourceCode.get())
            self.showMsg("打开文件:"+fileName)

    #保存编译的P-Code文件
    def saveFile(self):
        fd = filedialog.asksaveasfile("w")
        if fd is not None and self.pl0 is not None and len(self.pl0.getPCode()) >0:
            fd.write(self.pl0.getPCodeStr())
            fd.close()
            self.showMsg("保存成功")
        else:
            self.showMsg("错误:未编译")


    def compile(self):
        fd = open("temp","w")
        fd.write(self.sourceCodeFiled.get("1.0","end"))
        fd.close()
        buf=self.sourceCodeFiled.get("1.0","end")
        self.sourceCodeFiled.delete("1.0","end")
        self.sourceCodeFiled.insert("1.0",buf)
        self.pl0 = PL0("temp")
        self.showMsg("编译中...")
        self.pl0.start()
        self.pCodeFiled.delete("1.0", "end")
        if self.pl0.getErr() > 0:
            self.showMsg("编译错误")
            self.displayErr(self.pl0.getErrList())
            for err in self.pl0.getErrList():
                self.sourceCodeFiled.tag_add("err",str(err.line)+".0",str(err.line)+".end")
        else:
            self.showMsg("编译完成")
            self.pCodeFiled.insert("1.0", self.pl0.getPCodeStr())



    def showMsg(self,msg):
        self.label_status["text"]=str(msg)

    def create_widgets(self):
        #Menu Part
        menu = Menu(self.master)
        submenu_file = Menu(menu, tearoff=0)
        submenu_file.add_command(label='打开源码',command=self.openFile)
        submenu_file.add_command(label='保存P-Code',command = self.saveFile)
        menu.add_cascade(label='文件', menu=submenu_file)
        submenu_operation = Menu(menu,tearoff=0)
        submenu_operation.add_command(label="编译",command=self.compile)
        submenu_operation.add_command(label="运行",command=self.pCodeVM)
        menu.add_cascade(label='操作', menu=submenu_operation)
        menu_help = Menu(menu,tearoff=0)
        menu_help.add_command(label="关于",command=self.authorInfo)
        menu.add_cascade(menu=menu_help, label='帮助')

        self.master.config(menu=menu)
        #end of Menu
        #Main filed
        mainFiledFrame = Frame(self.master)



        tabControl = ttk.Notebook(mainFiledFrame)  # Create Tab Control
        tab1 = ttk.Frame(tabControl)  # Create a tab(sourceCode)
        tabControl.add(tab1, text='源码')  # Add the tab

        scrolly1 = Scrollbar(tab1)

        scrolly1.grid(row=0,column=1,sticky=(N,S,E))
        self.sourceCodeFiled = Text(tab1,width=82,height=24,yscrollcommand = scrolly1.set)
        self.sourceCodeFiled.tag_config("err",background="red")
        self.sourceCodeFiled.grid(row=0,column=0,sticky=(W,N))
        scrolly1.config(command=self.sourceCodeFiled.yview)

        tab2 = ttk.Frame(tabControl)  # Add a second tab(p-code)
        tabControl.add(tab2, text='P-Code')  # Make second tab visible
        scrolly2 = Scrollbar(tab2)
        scrolly2.grid(row=0, column=1, sticky=(N, S, E))
        self.pCodeFiled = Text(tab2, width=82, height=24,yscrollcommand = scrolly2.set)
        self.pCodeFiled.grid(row=0, column=0, sticky=(E, N))
        scrolly2.config(command=self.pCodeFiled.yview)

        tabControl.grid(row=0,column=0,sticky=(W,E))  # Pack to make visible
        mainFiledFrame.grid(row=0,column=0,sticky=(W,E))

        #end Main Filed
        #footbar

        footBar = Frame(self.master)
        self.label_status = Label(footBar)
        self.label_status["text"] = "等待...."
        self.label_status.grid(row=0,column=1,sticky=(W))
        footBar["borderwidth"]=2
        footBar['relief']='groove'
        footBar.grid(row=1,column=0,sticky=(W,E))





def main():
    root = Tk()
    root.geometry("595x396")
    root.title("PL/0 Compiler")
    root.resizable(width=False, height=False)
    app = Application(master=root)
    root.mainloop()






if __name__ == '__main__':
    main()
