from tkinter import Tk, BOTH, CENTER, LEFT, RIGHT, END, HORIZONTAL, RAISED, GROOVE, RIDGE, DISABLED, NORMAL, X, Y, NW, W, N, E, S, Canvas, Text, StringVar, Radiobutton
from tkinter.ttk import Label, Frame, Notebook, Entry, Progressbar, Combobox, Button
from PIL import Image, ImageTk
import pandas as pd
import string


#Global Variables
WIDTH = 680
HEIGHT = 550


class DeckHeroes(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.allCreatures = self.getCreatureList()
        
        self.initUI()
        
        
    def initUI(self):
        
        self.parent.title("Deck Heroes Dictionary")
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
        okButton = Button(self, text="OK")
        okButton.pack(side=RIGHT, pady=10)
 

    def createNotebookWidget(self):
        
        notebook = Notebook(self, width=WIDTH-30)
        notebook.pack(expand=1, anchor=NW, padx=10)
        notebook.bind("<<NotebookTabChanged>>", self._resetTab)
        #notebook.bind("<<NotebookTabChanged>>", self.updateSearchCombolist, add='+')
        notebook.enable_traversal()
        self.notebook = notebook
               
        self.cr_tab = self.createCreatureTab(self.notebook)
        self.he_tab = self.createHeroTab(self.notebook)
        self.sk_tab = self.createSkillTab(self.notebook)
        self.ru_tab = self.createRuneTab(self.notebook)
        
        self._creatureTabEvents()
  

    def _resetTab(self, event):
        
        self.srchCombo.focus_set()
        
        try:
            self.fltrFaction[self.fctnChoice.get()].deselect()
            self.fctnChoice.set("")
        except KeyError:
            pass
        
        self.fltrSkill.set("Skill")
        self.fltrStar.set("Stars")
        
        self.srchCombo['values'] = self.allCreatures
    
    
    def createCreatureTab(self, parent):

        attrDict = {}
        
        config = {
            "static":  {"font":"Helvetica 10 bold"},
            "dynamic": {"font":"Helvetica 10"}
            }
        
        path = {
            "img":  "images/creatures/%s",
            "icon": "images/icons/logo_%s.png",
            "star": "images/icons/logo_Star%d.png",
            "fctn": "images/icons/Faction_%s.png",
            "fctn2": "images/icons/Faction_%s_2.png"
 
            }
            
        tab = Frame(parent)
        parent.insert(END, tab, text='Creatures', underline=0) 

        creature = "abaddon"  
        creature_ = self.fetchCreature(creature)     
        self.creature = creature_
        
        ### Create all Frames to be used inside the notebook
        imgFrame  = Frame(tab)
        attrFrame = Frame(tab, relief=GROOVE, padding=10)
        sklFrame  = Frame(tab, relief=GROOVE, padding=15)
        srchFrame = Frame(tab)
        fltrFrame = Frame(tab)
        
        #Position the Frames in the notebook grid
        # (0,0) reserved for the crName below
        imgFrame.grid  (row=1, column=0, sticky=N+W, rowspan=2)
        attrFrame.grid (row=1, column=2, sticky=N+W)
        sklFrame.grid  (row=2, column=2, sticky=N+W)
        fltrFrame.grid (row=3, column=0, sticky=S+W+E, columnspan=3)
        srchFrame.grid (row=4, column=0, sticky=S+W, columnspan=3)
        
        #Name and description of the Creature
        crName = Label (tab, text=creature_.CreatureName.item(), font="Helvetica 11 bold")
        crName.grid (row=0, column=0, padx=10, pady=5)
        attrDict["CreatureName"] = crName
        
        crDesc = Label(tab, text=creature_.Script.item(), font="Helvetica 10 italic")
        crDesc.grid(row=0, column=1, sticky=W, pady=5, columnspan=3)
        attrDict["Script"] = crDesc
                       
        ### Contents of the imgFrame
        try:
            icrImage = self.addImage(path["img"]%(creature_.Image.item()))
        except:
            icrImage = self.addImage(path["img"]%("placeholder.jpg"))
        finally:
            crImage = Label(imgFrame, image=icrImage)
            crImage.image = icrImage
        
        crImage.grid(columnspan=2, padx=15, sticky=W+N+E+S)
        attrDict["Image"] = crImage
        
        srcLabel = Label(imgFrame, text="Source(s): ", **config["static"])
        srcLabel.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        srcLabel2 = Label(imgFrame, text=creature_.Source.item(), **config["dynamic"])
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
                      "Base HP":     {"row":2, "column":2},
                      "Choose Level":{"row":3, "column":0}
                     }
        
        for lbl, rc in attrLabels.items():
            
            if lbl in ["Faction", "Star Rating", "Choose Level"]:
                attrLabel = Label(attrFrame, text=lbl, **config["static"])
            
            #Add icon beside the labels
            else:
                iphoto = self.addImage(path["icon"]%(lbl), image="icon")             
                attrLabel = Label(attrFrame, text=lbl, image=iphoto,\
                                  compound=RIGHT, **config["static"])
                attrLabel.image = iphoto
                
            attrLabel.grid(padx=5, sticky=E, **rc)       
        
        ## Place dynamic label: Faction
        fctn = creature_.Faction.item()
        ifctnImage = self.addImage(path["fctn2"]%(fctn),image="icon")
        fctnLabel = Label(attrFrame, width=12, text=fctn, \
                         image=ifctnImage, compound=LEFT, **config["dynamic"])
        fctnLabel.image = ifctnImage
        fctnLabel.grid(sticky=W, padx=5, row=0, column=1)
        attrDict["Faction"] = fctnLabel
        
        ## Place dynamic label: StarRating
        star = int(creature_.StarRating.item())
        istarImage = self.addImage(path["star"]%(star), image="star", star=star)
        starLabel = Label(attrFrame, image=istarImage, compound=RIGHT)
        starLabel.image = istarImage
        starLabel.grid(sticky=W, padx=5, row=0, column=3)
        attrDict["StarRating"] = starLabel
        
        ## Place other dynamic entries
        attrOther = ["DelayTimer","Cost","BaseAtk0","BaseHP0"]
        
        attrEntries = [{"attr":attrOther[0], "text":attrOther[0], "row":1, "column":1},
                       {"attr":attrOther[1], "text":attrOther[1], "row":1, "column":3},
                       {"attr":attrOther[2], "text":attrOther[2], "row":2, "column":1},
                       {"attr":attrOther[3], "text":attrOther[3], "row":2, "column":3}
                      ] 
               
        for attr in attrEntries:
            entry = Entry(attrFrame, width=12, **config["dynamic"])            
            entry.grid(sticky=W, padx=5, row=attr["row"], column=attr["column"])
            entry.insert(0, creature_[attr["text"]].item())  
            entry.configure(state="readonly")
            attrDict[attr["attr"]] = entry
            
        
        clFrame = Frame(attrFrame)
        clFrame.grid(row=3, column=1)
        
        chooseLevelRB = {}
        self.chooseLevel = StringVar()
        
        for col,lvl in enumerate(["0","5","10","15"]):
            chooseLevelRB[lvl] = Radiobutton(clFrame, indicatoron=0, variable=self.chooseLevel, value=lvl, text=lvl, width=2)
            chooseLevelRB[lvl].grid(row=3, column=col+2)
        
        chooseLevelRB["0"].select()
        
        attrDict["chooseLevel"] = chooseLevelRB
        
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
        
        for lbl, rc in sklLabels.items():
            sklLabel = Label(sklFrame, text=lbl, **config["static"])
            sklLabel.grid(padx=5, **rc)       
            if lbl not in ["Skill","Skill Point"]:
                sklLabel.grid_configure(sticky=E)

        sklOther = ["Level0Skill","Level0SkillPoint","Level5Skill",\
                    "Level5SkillPoint","Level10Skill","Level10SkillPoint"]  
        
        sklEntries = [{"text":creature_[sklOther[0]].item(), "row":1, "column":1},
                      {"text":creature_[sklOther[2]].item(), "row":2, "column":1},
                      {"text":creature_[sklOther[4]].item(), "row":3, "column":1},
                     ] 
        
        for lbl,ent in zip(sklOther[0::2], sklEntries):
            sklentry = Entry(sklFrame, **config["dynamic"])            
            sklentry.grid(sticky=W, padx=5, row=ent["row"], column=ent["column"])
            sklentry.insert(0, ent["text"])  
            sklentry.configure(state="readonly")
            attrDict[lbl] = sklentry
        
        sklProgress = [{"text":creature_[sklOther[1]].item(), "row":1, "column":2},
                       {"text":creature_[sklOther[3]].item(), "row":2, "column":2},
                       {"text":creature_[sklOther[5]].item(), "row":3, "column":2}
                      ]  
        
        for i,j in zip(sklOther[1::2], sklProgress):
            sklprogress = Progressbar(sklFrame, mode="determinate", orient=HORIZONTAL, maximum=10)
            sklprogress.grid(sticky=W, padx=5, row=j["row"], column=j["column"])
            
            if j["text"] == '':
                value = 10
            else:
                value = int(j["text"])
            
            sklprogress.configure(value=value)
            attrDict[i] = sklprogress


        #Contents of the srchFrame
        srchLabel = Label(srchFrame, text="Search:")
        srchLabel.grid(padx=5, pady=5, sticky=E)
        srchCombo = Combobox(srchFrame)
        srchCombo.grid(row=0, column=1, pady=10, sticky=W)
        srchCombo['values'] = self.allCreatures

        
        iSearch = self.addImage("images/icons/search.png", image="icon")
        srchButton = Button(srchFrame, image=iSearch)
        srchButton.image = iSearch
        srchButton.grid(row=0, column=2, pady=10, sticky=W)

        
        #Contents of the fltrFrame
        fltrLabel = Label(fltrFrame, text="Filter(s):")
        fltrLabel.grid(padx=5, pady=5, sticky=E)
        
        fltrFactionFrame = Frame(fltrFrame, relief=GROOVE)
        fltrFactionFrame.grid(row=0, column=1, pady=5)
        
        fltrFactionLabel = Label(fltrFactionFrame, text="Faction:")
        fltrFactionLabel.grid(padx=5, pady=10, sticky=E)

        fltrFaction = {}
        factions = ["Human", "Faen", "Neander", "Mortii"]
        self.fctnChoice = StringVar()
                        
        for col,fctn in enumerate(factions):
            ifctnImage = self.addImage(path["fctn2"]%(fctn),image="icon")
            fltrFaction[fctn] = Radiobutton(fltrFactionFrame,\
                                            image=ifctnImage,\
                                            indicatoron=0,\
                                            variable=self.fctnChoice,\
                                            value=fctn,\
                                            command=self.updateSearchCombolist)
            fltrFaction[fctn].image = ifctnImage
            fltrFaction[fctn].grid(row=0, column=col+1, padx=5)
            
                       
        fltrStar = Combobox(fltrFrame, state="readonly", justify=CENTER, width=5)
        fltrStar.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        fltrStar["values"] = ["","1","2","3","4","5"]

        fltrStar.set("Stars")
                        
        fltrSkill = Combobox(fltrFrame, state="readonly", justify=CENTER)
        fltrSkill.grid(row=0, column=3, padx=5, pady=10, sticky=W)
        
        fltrSkill["values"] = [""] + self.getSkillList() 
        
        fltrSkill.set("Skill")

        
        resetButton = Button(fltrFrame, text="Reset")
        resetButton.grid(row=0, column=4, padx=10, pady=10, sticky=E)

                    
        self.attrDict = attrDict
        self.srchCombo = srchCombo
        self.fltrFaction = fltrFaction
        self.fltrStar = fltrStar
        self.fltrSkill = fltrSkill
        self.resetButton = resetButton
        self.srchButton = srchButton
        
        return tab
    
    
    def _creatureTabEvents(self):
         
        #changeLevel Event
        
        levelRB = self.attrDict["chooseLevel"]      
        
        def _levelRBevent(event):
            if event.type == "7":
                source = event.widget.cget("text")
            else:
                source = self.chooseLevel.get()
                
            basehp = self.creature["BaseHP%s"%(source)].item()
            self.attrDict["BaseHP0"].configure(state=NORMAL)
            self.attrDict["BaseHP0"].delete(0, END)
            self.attrDict["BaseHP0"].insert(END, basehp)
            self.attrDict["BaseHP0"].configure(state="readonly") 
            
            baseatk = self.creature["BaseAtk%s"%(source)].item()
            self.attrDict["BaseAtk0"].configure(state=NORMAL)
            self.attrDict["BaseAtk0"].delete(0, END)
            self.attrDict["BaseAtk0"].insert(END, baseatk)
            self.attrDict["BaseAtk0"].configure(state="readonly")  
            
            cost = self.creature["Cost"].item()
            
            if source == "15":
                cost = self.creature["CostAtMeld"].item()
            if cost == "":
                cost = self.creature["Cost"].item()
                    
            self.attrDict["Cost"].configure(state=NORMAL)
            self.attrDict["Cost"].delete(0, END)
            self.attrDict["Cost"].insert(END, cost)
            self.attrDict["Cost"].configure(state="readonly")                                      
        
        for rb in levelRB.values():
            rb.bind("<Enter>", _levelRBevent)
            rb.bind("<Leave>", _levelRBevent)
        
        #search Events        
        self.srchCombo.bind("<Return>", self.updateCreature)
        self.srchCombo.bind("<<ComboboxSelected>>", self.updateCreature)
        self.srchButton.bind("<Button-1>", self.updateCreature)    
        
        #filter Events
        self.fltrStar.bind("<<ComboboxSelected>>", self.updateSearchCombolist)        
        self.fltrSkill.bind("<<ComboboxSelected>>", self.updateSearchCombolist)    
        self.resetButton.bind("<Button-1>", self._resetTab)
    
    
    
    def updateSearchCombolist(self, *event):
        
        fltrTable = self.allCreatures
            
        if self.fltrStar.get() == "":
            fltrStar = None
        else:
            fltrStar = self.fltrStar.get()
            
        if self.fltrSkill.get() == "":
            fltrSkill = None           
        else:
            fltrSkill = self.fltrSkill.get()
        
        self.srchCombo['values'] = self.getCreatureList(fltrFaction=self.fctnChoice.get(), fltrStar=fltrStar,\
                                                       fltrSkill=fltrSkill)
    
    
    def updateCreature(self, event):
        
        path = {
            "img":  "images/creatures/%s",
            "icon": "images/icons/logo_%s.png",
            "star": "images/icons/logo_Star%d.png",
            "fctn": "images/icons/Faction_%s.png",
            "fctn2": "images/icons/Faction_%s_2.png"
            }

        temp = self.fetchCreature(self.srchCombo.get())

        if temp.Code.item() != "null":
        
            creature_ = temp.copy()   
            self.creature = creature_
            
            #Update attrDict               
            for attr,child in self.attrDict.items():
       
                if attr in ["CreatureName", "Source", "Script"]:
                    child.configure(text=creature_[attr].item())

                elif attr=="Image":
                    try:
                        icrImage = self.addImage(path["img"]%(creature_.Image_2.item()))
                    except:
                        try:
                            icrImage = self.addImage(path["img"]%(creature_.Image.item()))
                        except:
                            icrImage = self.addImage(path["img"]%("placeholder.jpg"))
                    finally:
                        child.configure(image=icrImage)
                        child.image = icrImage 
                
                elif attr=="Faction":
                    ifctnImage = self.addImage(path["fctn2"]%(creature_.Faction.item())\
                                               ,image="icon")
                    child.configure(text=creature_[attr].item(),\
                                     image=ifctnImage, compound=LEFT)
                    child.image = ifctnImage
                                            
                elif attr == "StarRating":    
                    star = int(creature_.StarRating.item())
                    istarImage = self.addImage(path["star"]%(star),\
                                           image="star", star=star)
                    child.configure(image=istarImage)
                    child.image = istarImage           
                
                elif attr == "BaseHP0":
                    basehp = self.creature["BaseHP%s"%(self.chooseLevel.get())].item()   
                    
                    child.configure(state=NORMAL)
                    child.delete(0, END)
                    child.insert(END, basehp)
                    child.configure(state="readonly")                      


                elif attr == "BaseAtk0":
                    baseatk = self.creature["BaseAtk%s"%(self.chooseLevel.get())].item()   
                    
                    child.configure(state=NORMAL)
                    child.delete(0, END)
                    child.insert(END, baseatk)
                    child.configure(state="readonly")                    
            
                elif attr == "Cost":
                    cost = self.creature["Cost"].item()
            
                    if self.chooseLevel.get() == "15":
                        cost = self.creature["CostAtMeld"].item()
                    if cost == "":
                        cost = self.creature["Cost"].item()

                    self.attrDict["Cost"].configure(state=NORMAL)
                    self.attrDict["Cost"].delete(0, END)
                    self.attrDict["Cost"].insert(END, cost)
                    self.attrDict["Cost"].configure(state="readonly")        
                
                elif attr == "chooseLevel":
                    pass             
                
                elif isinstance(child, Entry):
                    child.configure(state=NORMAL)
                    child.delete(0, END)
                    child.insert(END, creature_[attr].item())
                    child.configure(state="readonly")  
                    
                elif isinstance(child, Progressbar):
                    if creature_[attr].item()=='':
                        value = 10
                    else:
                        value = int(creature_[attr].item())
                        
                    child.configure(value=value)
    
    
    
    
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
    
    
    def getSkillList(self):
        
        creature = pd.read_csv('creatures.csv', dtype=str, keep_default_na=False)
        
        skills = creature["Level0Skill"]
        skills = skills.append(creature["Level5Skill"])
        skills = skills.append(creature["Level10Skill"])
        skills = [skl for skl in skills.unique()]
        
        return sorted(skills)
        
        
    
    def getCreatureList(self, fltrFaction=None, fltrStar=None, fltrSkill=None):
        
        creature = pd.read_csv('creatures.csv', dtype=str, keep_default_na=False)   
        
        if fltrFaction and fltrFaction not in ["Faction",""]:
            creature = creature[creature.Faction==fltrFaction]
        if fltrStar and fltrStar not in ["Stars",""]:
            creature = creature[creature.StarRating==fltrStar]
        if fltrSkill and fltrSkill not in ["Skill",""]:
            creature = creature[(creature.Level0Skill==fltrSkill) | (creature.Level5Skill==fltrSkill)\
                                | (creature.Level10Skill==fltrSkill)]
            
        return sorted(creature.CreatureName.values.tolist())        
  

    def fetchCreature(self, cr_code):
        
        creature = pd.read_csv('creatures.csv', dtype=str, keep_default_na=False)   
        creature_desc = pd.read_csv('creature_desc.csv', keep_default_na=False)
        creature = pd.merge(creature, creature_desc, how='left')
        creature.fillna("", inplace=True)
        cr_code = "".join(cr_code.split())
        cr_code = cr_code.lower()
        
        if cr_code in creature.Code.values:
            query = creature[creature.Code==cr_code].reset_index(drop=True)
        else:
            query = creature[creature.Code=="null"].reset_index(drop=True)
            
        return query
   

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