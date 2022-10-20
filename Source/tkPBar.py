from tkinter import *
from tkinter.ttk import *

class tkProgressbar():
    global self
    def __init__(self, total, Title="Downloading", Orientation=HORIZONTAL, Determinate=False):
        def cancel():
            self.cancel = True
            self.root.destroy()
        self.cancel = False
        self.total = total
        self.tdone = float(0)
        self.nctdn = 0
        self.value = 0
        self.Title = Title
        self.isDet = Determinate
        self.Orint = Orientation
        self.p2jmp = self.total/100
        self.root = Tk()
        self.root.title(self.Title)
        self.root.geometry('400x250+1000+300')
        if not self.isDet:
            self.pb1 = Progressbar(self.root, orient=self.Orint, length=100, mode='indeterminate')
        if self.isDet:
            self.pb1 = Progressbar(self.root, orient=self.Orint, length=100, mode='determinate')
        self.pb1.pack(expand=True)
        self.DesLV = ''
        self.DescL = Label(self.root)
        self.DescL.pack()
        self.cance = Button(self.root,command=cancel,text="Cancel")
        self.cance.pack()
        def pUpdate():
            #global self
            try:
                self.root.update_idletasks()
                self.pb1['value'] = self.value
                self.DescL['text'] = self.DesLV
                self.root.update()
                #print(self.nctdn, self.total)
                if self.nctdn >= self.total:
                    self.root.destroy()
                try:
                    self.root.after(10, pUpdate)
                except:
                    pass
            except Exception as e:
                #print(str(e)+"\n\nHappened in pUpdated()")
                pass
        pUpdate()


    def update(self, amount):
        if self.cancel:
            raise KeyboardInterrupt
        self.tdone += amount
        self.nctdn += amount
        while self.tdone >= self.p2jmp:
            if self.tdone >= self.p2jmp*2:
                self.tdone -= self.p2jmp*2
                self.value += 2
                continue
            self.tdone -= self.p2jmp
            self.value += 1
        try:
            self.root.update()
        except:
           pass

    def description(self, Desc):
        self.DesLV = Desc
        try:
            self.root.update()
        except:
            pass
