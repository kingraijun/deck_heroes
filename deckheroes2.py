from ttk import Frame, Label, Notebook, Button, Entry
from Tkinter import Tk, BOTH, LEFT, RIGHT, END, RAISED, X, Y, NW, Canvas, W, N
from PIL import Image, ImageTk

WIDTH = 500
HEIGHT = 700

class DeckHeroes(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
        self.parent.title("")
        self.pack(fill=BOTH, expand=1)
        
        title = Label(self, text="Deck Heroes Dictionary")
        title.pack(fill=X, pady=6)
        
        self.createNotebookWidget()
        
        closeButton = Button(self, text="Close", command=self.quit)
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(self, text="OK")
        okButton.pack(side=RIGHT, pady=5)
        searchLabel = Label(self, text="Search")
        searchLabel.pack(side=LEFT, padx=5, pady=5)
        searchEntry = Entry(self)
        searchEntry.pack(side=LEFT, pady=5)
        
    def createNotebookWidget(self):
        
        nb_config = {"sticky":W+N, "padding":5, "underline":0}
        
        notebook = Notebook(self, width=WIDTH-60, height=HEIGHT-130)
        notebook.pack(anchor=NW, expand=1)
        notebook.enable_traversal()
                    
        #Tab for Creatures
        tab1 = Frame(notebook)
        notebook.insert(END, tab1, text='Creatures', underline=0)
        photo1 = self.addImage("images/creatures/cr_aquarius_1.jpg")
        
        img = Label(tab1, image=photo1)
        img.image = photo1
        img.pack(anchor=NW, padx=5, pady=5)
        
        cr_name = Label(tab1, text="Aquarius")
        #cr_name.pack(anchor=NW, padx=5)
        cr_name.grid(row=0, column=0, padx=5)
        
        
        #Tab for Heroes
        tab2 = Frame(notebook)
        notebook.insert(END, tab2, text='Heroes', underline=0)
        photo2 = self.addImage("images/heroes/he_alchemist_1.jpg")

        img = Label(tab2,image=photo2)
        img.image = photo2
        img.pack(anchor=NW, padx=5, pady=5)
        
        #Tab for Skills
        tab3 = Frame(notebook)
        notebook.insert(END, tab3, text='Skills', underline=0)
        
        #Tab for Runes
        tab4 = Frame(notebook)
        notebook.insert(END, tab4, text='Runes', underline=0)
        
    def addImage(self, fname, size=(150,250)):
        img = Image.open(fname)
        img = img.resize(size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)           
        
def main():
  
    root = Tk()
    ex = DeckHeroes(root)
    root.geometry("%dx%d+10+10"%(WIDTH,HEIGHT))
    root.mainloop()  


if __name__ == '__main__':
    main()  