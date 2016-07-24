from ttk import Frame, Label, Notebook, Button, Entry
from Tkinter import Tk, BOTH, CENTER, LEFT, RIGHT, END, RAISED, GROOVE, RIDGE, DISABLED, NORMAL, X, Y, NW, W, N, E, S, Canvas, Text, StringVar
from PIL import Image, ImageTk
import pandas as pd
import string

WIDTH = 680
HEIGHT = 500


class DeckHeroes(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
        self.parent.title("")
        self.pack(fill=BOTH, expand=1)
        
        dh_frame = Frame(self)
        dh_frame.pack(fill=BOTH, expand=1)
        
        ilogo = self.addImage("images/icons/logo_deckheroes_1.jpg", image="logo")
        dh_title = Label(dh_frame, image=ilogo, text="Deck Heroes Dictionary", \
                         compound=LEFT, font = "Helvetica 12 bold")
        dh_title.image = ilogo
        dh_title.pack(fill=BOTH, pady=10, padx=10)
   
        self.createNotebookWidget()
            
        closeButton = Button(self, text="Close", command=self.quit)
        closeButton.pack(side=RIGHT, padx=10, pady=10)
        okButton = Button(self, text="OK", command=self.quit)
        okButton.pack(side=RIGHT, pady=10)
        
        #self.createNotebookWidget()

        
    def createNotebookWidget(self):
        
        notebook = Notebook(self, width=WIDTH-30)
        notebook.pack(expand=1, anchor=NW, padx=10)
        notebook.enable_traversal()
        self.notebook = notebook
        
        self.cr_tab = self.createCreatureTab(self.notebook)
        self.he_tab = self.createHeroTab(self.notebook)
        self.sk_tab = self.createSkillTab(self.notebook)
        self.ru_tab = self.createRuneTab(self.notebook)
     

    def createCreatureTab(self, parent, cr_dict=None):
        
        tab = Frame(parent)
        parent.insert(END, tab, text='Creatures', underline=0) 
        staticLabel_config = {"font":"Helvetica 10 bold"}
        dynamicLabel_config = {"font":"Helvetica 10"}

        self.creature = StringVar()
        self.creature.set("paragon")
            
        if cr_dict is None:
            cr_dict, cr_col = self.fetchCreature(self.creature.get())           
        
        #Create all Frames to be used inside the notebook
        imageFrame = Frame(tab)
        imageFrame.grid(row=1, column=0, sticky=N+W, rowspan=2)
        searchFrame = Frame(tab)
        searchFrame.grid(row=3, column=0, sticky=W, columnspan=2)
        attributeFrame = Frame(tab, relief=GROOVE, padding=10)
        attributeFrame.grid(row=1, column=2, sticky=N+W)
        skillFrame = Frame(tab, relief=GROOVE, padding=15)
        skillFrame.grid(row=2, column=2, sticky=N+W)

        #Define event
        def updateEntry(event):
            
            proc = False
  
            temp,_ = self.fetchCreature(searchEntry.get())
            
            if temp["Code"][0] != "null":
                proc = True
            
            if proc:
                self.creature.set(searchEntry.get())    

                cr_dict = temp      

                cr_name.configure(text=cr_dict["CreatureName"][0])

                try:
                    cr_iphoto = self.addImage("images/creatures/%s"%(cr_dict["Image"][0]))
                except:
                    cr_iphoto = self.addImage("images/creatures/placeholder.jpg")

                cr_photo.configure(image=cr_iphoto)
                cr_photo.image = cr_iphoto
                
                for attr,labent in attrDict.iteritems():
                    
                    if attr == "Faction":                       
                        iphoto = self.addImage("images/icons/Faction_%s.png"%(cr_dict[attr][0]),image="icon")
                        labent.configure(text=cr_dict[attr][0], image=iphoto, compound=LEFT)
                        labent.image = iphoto
                    
                    elif attr == "StarRating":                       
                        iphoto = self.addImage("images/icons/logo_Star%s.png"%(cr_dict[attr][0]),\
                                               image="star", star=int(cr_dict[attr][0]))
                        labent.configure(image=iphoto, compound=LEFT)
                        labent.image = iphoto       
                        
                    else:
                        labent.configure(state=NORMAL)
                        labent.delete(0, END)
                        labent.insert(END,cr_dict[attr][0])
                        labent.configure(state="readonly")
                
        
        #Name of the Creature
        cr_name = Label(tab, text=cr_dict["CreatureName"][0], font="Helvetica 11 bold")
        cr_name.grid(row=0, column=0, sticky=W, padx=10, pady=5, columnspan=2)    
        
        #Contents of the imageFrame
        try:
            cr_iphoto = self.addImage("images/creatures/%s"%(cr_dict["Image"][0]))
        except:
            cr_iphoto = self.addImage("images/creatures/placeholder.jpg")
            
        cr_photo = Label(imageFrame, image=cr_iphoto)
        cr_photo.image = cr_iphoto
        cr_photo.grid(columnspan=2, padx=15, sticky=W+N+E+S)
        sourceLabel = Label(imageFrame, text="Source(s):  " +\
                            str(cr_dict["Source"][0]), **staticLabel_config)
        sourceLabel.grid(row=1, column=0, sticky=W, pady=5, padx=10)
        
        #Contents of the searchFrame
        searchLabel = Label(searchFrame, text="Search:")
        searchLabel.grid(padx=5, pady=5, sticky=E)
        searchEntry = Entry(searchFrame)
        searchEntry.grid(row=0, column=1, pady=10, sticky=W)
        searchEntry.focus_set()
        searchEntry.bind("<Return>", updateEntry)
        
        iSearch = self.addImage("images/icons/search.png", image="icon")
        searchButton = Button(searchFrame, image=iSearch)
        searchButton.image = iSearch
        searchButton.grid(row=0, column=2, pady=10, sticky=W)
        searchButton.bind("<Button-1>", updateEntry)
        
        #Contents of the attributeFrame
        attributeFrame.rowconfigure(0, pad=10)
        attributeFrame.rowconfigure(1, pad=10)
        attributeFrame.rowconfigure(2, pad=10)
        
        attributeLabels = {"Faction":  {"row":0, "column":0},
                        "Star Rating": {"row":0, "column":2},
                        "Delay Timer": {"row":1, "column":0},
                        "Cost":        {"row":1, "column":2},
                        "Base Atk":    {"row":2, "column":0},
                        "Base HP":     {"row":2, "column":2}
                 }
        
        for lbl, rc in attributeLabels.iteritems():
            label = Label(attributeFrame, text=lbl, **staticLabel_config)
            if lbl in ["Cost","Delay Timer", "Base Atk", "Base HP"]:
                iphoto = self.addImage("images/icons/logo_%s.png"%(lbl), image="icon")
                label.configure(image=iphoto, compound=RIGHT)
                label.image = iphoto
            label.grid(padx=5, sticky=E, **rc)       

        attributeEntries = [{"attr":cr_col[1], "text":cr_dict[cr_col[1]][0]    ,"row":0, "column":1},
                            {"attr":cr_col[2], "text":cr_dict[cr_col[2]][0] ,"row":0, "column":3},
                            {"attr":cr_col[3], "text":cr_dict[cr_col[3]][0] ,"row":1, "column":1},
                            {"attr":cr_col[4], "text":cr_dict[cr_col[4]][0]       ,"row":1, "column":3},
                            {"attr":cr_col[5], "text":cr_dict[cr_col[5]][0]    ,"row":2, "column":1},
                            {"attr":cr_col[6], "text":cr_dict[cr_col[6]][0]     ,"row":2, "column":3}
                           ] 
        
        attrDict = {}
        
        for attr in attributeEntries:
            if attr["text"] in ["Human","Faen","Mortii","Neander"]:
                iphoto = self.addImage("images/icons/Faction_%s.png"%(attr["text"]),image="icon")
                label = Label(attributeFrame, width=12, **dynamicLabel_config)
                label.grid(sticky=W, padx=5, row=attr["row"], column=attr["column"])
                label.configure(text=attr["text"], image=iphoto, compound=LEFT)
                label.image = iphoto
                attrDict[attr["attr"]] = label
            
            elif attr["attr"]=="StarRating" and attr["text"] in ["1","2","3","4","5"]:
                iphoto = self.addImage("images/icons/logo_Star%s.png"%(attr["text"]),\
                                       image="star", star=int(attr["text"]))
                label = Label(attributeFrame)
                label.grid(sticky=W, padx=5, row=attr["row"], column=attr["column"])
                label.configure(image=iphoto)
                label.image = iphoto
                attrDict[attr["attr"]] = label
                
            else:
                entry = Entry(attributeFrame, width=12, **dynamicLabel_config)            
                entry.grid(sticky=W, padx=5, row=attr["row"], column=attr["column"])
                entry.insert(0, attr["text"])      
                entry.configure(state="readonly")
                attrDict[attr["attr"]] = entry
        
        #Contents of the skillFrame
        skillFrame.rowconfigure(1, pad=10)
        skillFrame.rowconfigure(2, pad=10)
        skillFrame.rowconfigure(3, pad=10)
        
        skillLabels = {"Skill":       {"row":0, "column":1},
                       "Skill Point": {"row":0, "column":2},
                       "Level 0:":    {"row":1, "column":0},
                       "Level 5:":    {"row":2, "column":0},
                       "Level 10:":   {"row":3, "column":0}
                 }
        
        for lbl, rc in skillLabels.iteritems():
            label = Label(skillFrame, text=lbl, **staticLabel_config)
            label.grid(padx=5, **rc)       
            if lbl not in ["Skill","Skill Point"]:
                label.grid_configure(sticky=E)

        skillEntries = [{"text":cr_dict[cr_col[7]][0] , "row":1, "column":1},
                        {"text":cr_dict[cr_col[8]][0] , "row":1, "column":2},
                        {"text":cr_dict[cr_col[9]][0] , "row":2, "column":1},
                        {"text":cr_dict[cr_col[10]][0], "row":2, "column":2},
                        {"text":cr_dict[cr_col[11]][0], "row":3, "column":1},
                        {"text":cr_dict[cr_col[12]][0], "row":3, "column":2}
                       ] 
        
        for lbl,ent in zip(cr_col[7:13], skillEntries):
            entry = Entry(skillFrame, **dynamicLabel_config)            
            entry.grid(sticky=W, padx=5, row=ent["row"], column=ent["column"])
            entry.insert(0, ent["text"])  
            entry.configure(state="readonly")
            attrDict[lbl] = entry
         
        return tab
    
    
    def createHeroTab(self, parent, he_dict=None):
        
        tab = Frame(parent)
        parent.insert(END, tab, text='Heroes', underline=0)        
        staticLabel_config = {"font":"Helvetica 10 bold"}
        dynamicLabel_config = {"background":"white"}

        self.hero = StringVar()
        self.hero.set("Einherjar")
        
        if he_dict is None:
            he_dict = self.fetchHero(self.hero.get())        

        imageFrame = Frame(tab)
        imageFrame.grid(row=1, column=0, sticky=N+W, rowspan=2)     
        searchFrame = Frame(tab)
        searchFrame.grid(row=3, column=0, sticky=W, columnspan=2)
        
        he_name = Label(tab, text=he_dict["HeroName"][0], font="Helvetica 11 bold")
        he_name.grid(row=0, column=0, sticky=W, padx=10, pady=5, columnspan=2)
        
        #Contents of the imageFrame
        try:
            he_iphoto = self.addImage("images/heroes/%s"%(he_dict["Image"][0]))
        except:
            he_iphoto = self.addImage("images/heroes/placeholder.jpg")
            
        he_photo = Label(imageFrame, image=he_iphoto)
        he_photo.image = he_iphoto
        he_photo.grid(columnspan=2, padx=15, sticky=W+N+E+S)
        sourceLabel = Label(imageFrame, text="Source(s):  " +\
                            he_dict["Source"][0], **staticLabel_config)
        sourceLabel.grid(row=1, column=0, sticky=W, pady=5, padx=10)

        #Contents of the searchFrame
        searchLabel = Label(searchFrame, text="Search:")
        searchLabel.grid(padx=5, pady=5, sticky=E)
        
        
        def fetchEntry(event):
            
            temp = self.fetchHero(searchEntry.get())
            
            if temp["HeroName"][0] == "Null":
                pass
            
            else:
                self.hero.set(searchEntry.get())    

                he_dict = self.fetchHero(self.hero.get())      

                he_name.configure(text=he_dict["HeroName"][0])

                try:
                    he_iphoto = self.addImage("images/heroes/%s"%(he_dict["Image"][0]))
                except:
                    he_iphoto = self.addImage("images/heroes/placeholder.jpg")

                he_photo.configure(image=he_iphoto)
                he_photo.image = he_iphoto
                        
        
        searchEntry = Entry(searchFrame)
        searchEntry.grid(row=0, column=1, pady=10, sticky=W)
        searchEntry.bind("<Return>", fetchEntry)
        
        iSearch = self.addImage("images/icons/search.png", image="icon")
        searchButton = Button(searchFrame, image=iSearch)
        searchButton.image = iSearch
        searchButton.grid(row=0, column=2, pady=10, sticky=W)
        searchButton.bind("<Button-1>", fetchEntry)
        
      
        return tab
            
    def createSkillTab(self, parent, he_dict=None):
        
        tab = Frame(parent)
        parent.insert(END, tab, text='Skills', underline=0)         
        
 
    def createRuneTab(self, parent, he_dict=None):
        
        tab = Frame(parent)
        parent.insert(END, tab, text='Runes', underline=0)  
        
        
    def addImage(self, fname, image=None, **kwargs):
        
        iconsize = 16
        
        if image is None:
            size = (150,250)
        elif image == "logo":
            size = (30,30)
        elif image == "icon":
            size = (iconsize,iconsize)
        elif image == "star":
            size = (iconsize*kwargs["star"],iconsize)
        
        img = Image.open(fname)
        img = img.resize(size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)         
    
    
    def fetchCreature(self, cr_code):
        
        creature = pd.read_csv('creatures.csv', dtype=str, keep_default_na=False)
   
        cr_code = string.lower("".join(cr_code.split()))

        if cr_code in creature.Code.values:
            query = creature[creature.Code==cr_code].reset_index(drop=True)
        else:
            query = creature[creature.Code=="null"].reset_index(drop=True)
            
        return query.to_dict(), query.columns.values

    def fetchHero(self, he_name):
        
        heroes = pd.read_csv('heroes.csv', dtype=str, keep_default_na=False)
        if he_name in heroes.HeroName.values:
            query = heroes[heroes.HeroName==he_name].reset_index(drop=True)
        else:
            query = heroes[heroes.HeroName=="Null"].reset_index(drop=True)
            
        return query.to_dict()    
        
def main():
       
    root = Tk()
    ex = DeckHeroes(root)
    root.geometry("%dx%d+100+100"%(WIDTH,HEIGHT))
    root.resizable(width=False, height=False)
    root.mainloop()  


if __name__ == '__main__':
    main()  