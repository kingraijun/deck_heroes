from ttk import Frame, Label, Notebook, Button, Entry
from Tkinter import Tk, BOTH, CENTER, LEFT, RIGHT, END, RAISED, GROOVE, RIDGE, DISABLED, NORMAL, X, Y, NW, W, N, E, S, Canvas, Text, StringVar
from PIL import Image, ImageTk
import pandas as pd
import string

WIDTH = 680
HEIGHT = 520


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
        
        
    def createNotebookWidget(self):
        
        notebook = Notebook(self, width=WIDTH-30)
        notebook.pack(expand=1, anchor=NW, padx=10)
        notebook.enable_traversal()
        self.notebook = notebook
        
        self.cr_tab = self.createCreatureTab(self.notebook)
        self.he_tab = self.createHeroTab(self.notebook)
        self.sk_tab = self.createSkillTab(self.notebook)
        self.ru_tab = self.createRuneTab(self.notebook)
     

    def createCreatureTab(self, parent):

        attrDict = {}
        
        config = {
            "static":  {"font":"Helvetica 10 bold"},
            "dynamic": {"font":"Helvetica 10"}
            }
        
        path = {
            "img":  "images/creatures/%s",
            "icon": "images/icons/logo_%s.png",
            "fctn": "images/icons/Faction_%s.png",
            "star": "images/icons/logo_Star%d.png",        
            }
            
        tab = Frame(parent)
        parent.insert(END, tab, text='Creatures', underline=0) 

        self.creature = "apprentice"  
        creatDict, creatCol = self.fetchCreature(self.creature)            
        
        ### Create all Frames to be used inside the notebook
        imgFrame  = Frame(tab)
        attrFrame = Frame(tab, relief=GROOVE, padding=10)
        sklFrame  = Frame(tab, relief=GROOVE, padding=15)
        srchFrame = Frame(tab)
        
        #Position the Frames in the notebook grid
        # (0,0) reserved for the creatureName below
        imgFrame.grid  (row=1, column=0, sticky=N+W, rowspan=2)
        attrFrame.grid (row=1, column=2, sticky=N+W)
        sklFrame.grid  (row=2, column=2, sticky=N+W)
        srchFrame.grid (row=3, column=0, sticky=W, columnspan=3)
                       
        #Name of the Creature
        crName = Label (tab, text=creatDict["CreatureName"][0], font="Helvetica 11 bold")
        crName.grid (row=0, column=0, sticky=W, padx=10, pady=5, columnspan=2)
        attrDict["CreatureName"] = crName
               
        
        ### Contents of the imgFrame
        try:
            icrImage = self.addImage(path["img"]%(creatDict["Image"][0]))
        except:
            icrImage = self.addImage(path["img"]%("placeholder.jpg"))
        finally:
            crImage = Label(imgFrame, image=icrImage)
            crImage.image = icrImage
        
        crImage.grid(columnspan=2, padx=15, sticky=W+N+E+S)
        attrDict["Image"] = crImage
        
        srcLabel = Label(imgFrame, text="Source(s): ", **config["static"])
        srcLabel.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        srcLabel2 = Label(imgFrame, text=creatDict["Source"][0], **config["dynamic"])
        srcLabel2.grid(row=1, column=1, pady=10, sticky=W)
        attrDict["Source"] = srcLabel2
                      
        ### Contents of the attrFrame
        attrFrame.rowconfigure(0, pad=10)
        attrFrame.rowconfigure(1, pad=10)
        attrFrame.rowconfigure(2, pad=10)
        
        ## Place static labels       
        attrLabels = {"Faction":     {"row":0, "column":0},
                      "Star Rating": {"row":0, "column":2},
                      "Delay Timer": {"row":1, "column":0},
                      "Cost":        {"row":1, "column":2},
                      "Base Atk":    {"row":2, "column":0},
                      "Base HP":     {"row":2, "column":2}
                     }
        
        for lbl, rc in attrLabels.iteritems():
            
            if lbl in ["Faction", "Star Rating"]:
                attrLabel = Label(attrFrame, text=lbl, **config["static"])
            
            #Add icon beside the labels
            else:
                iphoto = self.addImage(path["icon"]%(lbl), image="icon")             
                attrLabel = Label(attrFrame, text=lbl, image=iphoto,\
                                  compound=RIGHT, **config["static"])
                attrLabel.image = iphoto
                
            attrLabel.grid(padx=5, sticky=E, **rc)       
        
        ## Place dynamic label: Faction
        fctn = creatDict["Faction"][0]
        ifctnImage = self.addImage(path["fctn"]%(fctn),image="icon")
        fctnLabel = Label(attrFrame, width=12, text=fctn, \
                         image=ifctnImage, compound=LEFT, **config["dynamic"])
        fctnLabel.image = ifctnImage
        fctnLabel.grid(sticky=W, padx=5, row=0, column=1)
        attrDict["Faction"] = fctnLabel
        
        ## Place dynamic label: StarRating
        star = int(creatDict["StarRating"][0])
        istarImage = self.addImage(path["star"]%(star), image="star", star=star)
        starLabel = Label(attrFrame, text=star, image=istarImage, compound=RIGHT)
        starLabel.image = istarImage
        starLabel.grid(sticky=W, padx=5, row=0, column=3)
        attrDict["StarRating"] = starLabel
        
        ## Place other dynamic entries
        attrOther = ["DelayTimer","Cost","BaseAtk","BaseHP"]
        
        attrEntries = [{"attr":attrOther[0], "text":attrOther[0], "row":1, "column":1},
                       {"attr":attrOther[1], "text":attrOther[1], "row":1, "column":3},
                       {"attr":attrOther[2], "text":attrOther[2], "row":2, "column":1},
                       {"attr":attrOther[3], "text":attrOther[3], "row":2, "column":3}
                      ] 
        
        for attr in attrEntries:
            entry = Entry(attrFrame, width=12, **config["dynamic"])            
            entry.grid(sticky=W, padx=5, row=attr["row"], column=attr["column"])
            entry.insert(0, attr["text"])      
            entry.configure(state="readonly")
            attrDict[attr["attr"]] = entry
        
        
        
        ### Contents of the sklFrame
        sklFrame.rowconfigure(1, pad=10)
        sklFrame.rowconfigure(2, pad=10)
        sklFrame.rowconfigure(3, pad=10)
        
        sklLabels = {"Skill":       {"row":0, "column":1},
                     "Skill Point": {"row":0, "column":2},
                     "Level 0:":    {"row":1, "column":0},
                     "Level 5:":    {"row":2, "column":0},
                     "Level 10:":   {"row":3, "column":0}
                    }
        
        for lbl, rc in sklLabels.iteritems():
            sklLabel = Label(sklFrame, text=lbl, **config["static"])
            sklLabel.grid(padx=5, **rc)       
            if lbl not in ["Skill","Skill Point"]:
                sklLabel.grid_configure(sticky=E)

        sklOther = ["Level0Skill","Level0SkillPoint","Level5Skill",\
                    "Level5SkillPoint","Level10Skill","Level10SkillPoint"]  
        
        sklEntries = [{"text":creatDict[sklOther[0]][0], "row":1, "column":1},
                      {"text":creatDict[sklOther[1]][0], "row":1, "column":2},
                      {"text":creatDict[sklOther[2]][0], "row":2, "column":1},
                      {"text":creatDict[sklOther[3]][0], "row":2, "column":2},
                      {"text":creatDict[sklOther[4]][0], "row":3, "column":1},
                      {"text":creatDict[sklOther[5]][0], "row":3, "column":2}
                     ] 
        
        for lbl,ent in zip(sklOther, sklEntries):
            sklentry = Entry(sklFrame, **config["dynamic"])            
            sklentry.grid(sticky=W, padx=5, row=ent["row"], column=ent["column"])
            sklentry.insert(0, ent["text"])  
            sklentry.configure(state="readonly")
            attrDict[lbl] = sklentry

        #Define event
        def updateEntry(event):

            proc = False 
            temp,_ = self.fetchCreature(srchEntry.get())

            if temp["Code"][0] != "null":
                proc = True
            
            if proc:
        
                creatDict = temp.copy()   
                self.creature = creatDict["CreatureName"][0]
            
                #Update attrDict
                
                for attr,child in attrDict.iteritems():
       
                    if attr in ["CreatureName", "Source"]:
                        child.configure(text=creatDict[attr][0])

                    elif attr=="Image":
                        try:
                            icrImage = self.addImage(path["img"]%(creatDict["Image"][0]))
                        except:
                            icrImage = self.addImage(path["img"]%("placeholder.jpg"))
                        finally:
                            child.configure(image=icrImage)
                            child.image = icrImage 
                
                    elif attr=="Faction":
                        ifctnImage = self.addImage(path["fctn"]%(creatDict["Faction"][0])\
                                                   ,image="icon")
                        child.configure(text=creatDict[attr][0],\
                                         image=ifctnImage, compound=LEFT)
                        child.image = ifctnImage
                                            
                    elif attr == "StarRating":    
                        star = int(creatDict["StarRating"][0])
                        istarImage = self.addImage(path["star"]%(star),\
                                               image="star", star=star)
                        child.configure(text=star, image=istarImage, compound=RIGHT)
                        child.image = istarImage           
                        
                    elif isinstance(child, Entry):
                        child.configure(state=NORMAL)
                        child.delete(0, END)
                        child.insert(END, creatDict[attr][0])
                        child.configure(state="readonly")
       
        
        #Contents of the searchFrame
        srchLabel = Label(srchFrame, text="Search:")
        srchLabel.grid(padx=5, pady=5, sticky=E)
        srchEntry = Entry(srchFrame)
        srchEntry.grid(row=0, column=1, pady=10, sticky=W)
        srchEntry.focus_set()
        srchEntry.bind("<Return>", updateEntry)
        
        iSearch = self.addImage("images/icons/search.png", image="icon")
        srchButton = Button(srchFrame, image=iSearch)
        srchButton.image = iSearch
        srchButton.grid(row=0, column=2, pady=10, sticky=W)
        srchButton.bind("<Button-1>", updateEntry)
        
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