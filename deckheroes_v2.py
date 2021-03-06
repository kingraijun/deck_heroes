from tkinter import Tk, BOTH, CENTER, LEFT, RIGHT, END, HORIZONTAL, RAISED, GROOVE, RIDGE, DISABLED, SOLID, NORMAL, INSERT, X, Y, NW, W, N, E, S, Canvas, Text, StringVar, Radiobutton, Toplevel, WORD
from tkinter.ttk import Label, Frame, Notebook, Entry, Progressbar, Combobox, Button
from PIL import Image, ImageTk
import pandas as pd
import string
import math


#Global Variables
WIDTH = 770
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
                         compound=LEFT, font = "Times 15 bold")
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
        notebook.enable_traversal()
        self.notebook = notebook
               
        self.cr_tab = self.createCreatureTab(self.notebook)
        self.he_tab = self.createHeroTab(self.notebook)
        self.sk_tab = self.createSkillTab(self.notebook)
        self.ru_tab = self.createRuneTab(self.notebook)
        
        self._creatureTabEvents()
    
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

        creature = "aquarius"  
        creature_ = self.fetchCreature(creature)     
        self.creature = creature_
        
        ### Create all Frames to be used inside the notebook
        #crFrame   = Frame(tab)
        imgFrame  = Frame(tab)
        attrFrame = Frame(tab, relief=GROOVE)
        sklFrame  = Frame(tab, relief=GROOVE, padding=5)
        srcFrame  = Frame(tab, relief=GROOVE, padding=5)
        srchFrame = Frame(tab)
        fltrFrame = Frame(tab)
        
        #Position the Frames in the notebook grid
        # (0,0) reserved for the crName below
        #crFrame.grid   (sticky=N+W, columnspan=4)
        imgFrame.grid  (row=2, column=0, sticky=S+N+W+E, rowspan=2)
        attrFrame.grid (row=2, column=1, sticky=S+N+W+E, rowspan=2, ipadx=8, ipady=5)
        sklFrame.grid  (row=2, column=2, sticky=N+W, padx=5, ipadx=10, ipady=8)
        srcFrame.grid  (row=3, column=2, sticky=S+W+E+N, padx=5)
        fltrFrame.grid (row=4, column=0, sticky=S+W+E, pady=5, columnspan=3)
        srchFrame.grid (row=5, column=0, sticky=S+W, columnspan=3)
        
        #Name and description of the Creature
        crName = Label (tab, text=creature_.CreatureName.item(), font="Times 14 bold")
        crName.grid (row=0, column=0, sticky=N, ipady=5, columnspan=3)
        attrDict["CreatureName"] = crName
        
        crDesc = Label(tab, text=creature_.Script.item(), font="Helvetica 9 italic")
        crDesc.grid(row=1, column=0, sticky=N, ipady=5, columnspan=3)
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
        
        ### Contents of the srcFrame
        srcLabel = Label(srcFrame, text="Source(s)", **config["static"])
        srcLabel.grid(ipadx=5, ipady=5, sticky=N+W)
        srcLabel2 = Text(srcFrame, height=3, width=35, wrap=WORD, padx=10,\
                         borderwidth=0, relief=SOLID, **config["dynamic"])
        srcLabel2.grid(row=1, column=0, padx=5, pady=5)
        srcLabel2.insert(END, creature_.Source.item())
        srcLabel2.config(state=DISABLED)
        attrDict["Source"] = srcLabel2
                      
        ### Contents of the attrFrame
        attrFrame.rowconfigure(0, pad=10)
        attrFrame.rowconfigure(1, pad=10)
        attrFrame.rowconfigure(2, pad=10)
        
        ## Place static labels       
        attrLabels = {"Faction":     {"row":0, "column":0},
                      "Star Rating": {"row":1, "column":0},
                      "Delay Timer": {"row":2, "column":0},
                      "Cost":        {"row":3, "column":0},
                      "Base Atk":    {"row":4, "column":0},
                      "Base HP":     {"row":5, "column":0},
                      "Choose Level":{"row":6, "column":0}
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
            
            if lbl in ["Faction", "Star Rating"]:
                pady = 1
            else:
                pady = 5
            
            attrLabel.grid(padx=5, pady=pady, sticky=E, **rc)       
        
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
        starLabel.grid(sticky=W, padx=5, row=1, column=1)
        attrDict["StarRating"] = starLabel
        
        ## Place other dynamic entries
        attrOther = ["DelayTimer","Cost","BaseAtk0","BaseHP0"]
        
        attrEntries = [{"attr":attrOther[0], "text":attrOther[0], "row":2, "column":1},
                       {"attr":attrOther[1], "text":attrOther[1], "row":3, "column":1},
                       {"attr":attrOther[2], "text":attrOther[2], "row":4, "column":1},
                       {"attr":attrOther[3], "text":attrOther[3], "row":5, "column":1}
                      ] 
               
        for attr in attrEntries:
            entry = Entry(attrFrame, width=12, **config["dynamic"])            
            entry.grid(sticky=W, padx=5, pady=5, row=attr["row"], column=attr["column"])
            entry.insert(0, creature_[attr["text"]].item())  
            entry.configure(state="readonly", cursor="")
            attrDict[attr["attr"]] = entry
            
        
        clFrame = Frame(attrFrame)
        clFrame.grid(row=6, column=1, pady=5)
        
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
                     "Pt":          {"row":0, "column":2},
                     "Level 0:":    {"row":1, "column":0},
                     "Level 5:":    {"row":2, "column":0},
                     "Level 10:":   {"row":3, "column":0}
                    }
        
        for lbl, rc in sklLabels.items():
            sklLabel = Label(sklFrame, text=lbl, **config["static"])
            sklLabel.grid(padx=5, **rc)       
            if lbl not in ["Skill","Pt"]:
                sklLabel.grid_configure(sticky=E)

        sklOther = ["Level0Skill","Level0SkillPoint","Level5Skill",\
                    "Level5SkillPoint","Level10Skill","Level10SkillPoint"]  
        
        sklEntries = [{"text":creature_[sklOther[0]].item(), "row":1, "column":1},
                      {"text":creature_[sklOther[1]].item(), "row":1, "column":2},
                      {"text":creature_[sklOther[2]].item(), "row":2, "column":1},
                      {"text":creature_[sklOther[3]].item(), "row":2, "column":2},
                      {"text":creature_[sklOther[4]].item(), "row":3, "column":1},   
                      {"text":creature_[sklOther[5]].item(), "row":3, "column":2}
                     ] 
        
        for lbl,ent in zip(sklOther, sklEntries):
            if lbl in ["Level0Skill","Level5Skill","Level10Skill"]:
                width = 16
            else:
                width = 3
            sklentry = Entry(sklFrame, style='TEntry', width=width,  **config["dynamic"])            
            sklentry.grid(sticky=W, padx=5, row=ent["row"], column=ent["column"])
            sklentry.insert(0, ent["text"])  
            sklentry.configure(state="readonly", cursor="")
            attrDict[lbl] = sklentry
        
        iSearch = self.addImage("images/icons/search.png", image="icon")
        
        sklSrchButton = {}
        
        for row in range(3):    
            sklSrchButton[row] = Button(sklFrame, image=iSearch)
            sklSrchButton[row].image = iSearch
            sklSrchButton[row].grid(row=row+1, column=3, sticky=W)

        #Contents of the srchFrame
        srchLabel = Label(srchFrame, text="Search:")
        srchLabel.grid(padx=5, pady=5, sticky=E)
        srchCombo = AutocompleteCombobox(srchFrame)
        srchCombo.grid(row=0, column=1, pady=10, sticky=W)
        srchCombo.set_completion_list(self.allCreatures)
       
        srchButton = Button(srchFrame, image=iSearch)
                  
        
        #Contents of the fltrFrame
        fltrLabel = Label(fltrFrame, text="Filter(s):")
        fltrLabel.grid(padx=5, pady=5, sticky=E)
        
        fltrFactionFrame = Frame(fltrFrame, relief=GROOVE)
        fltrFactionFrame.grid(row=0, column=1, pady=5, ipadx=3)
        
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
            fltrFaction[fctn].grid(row=0, column=col+1)
           
        fltrStarFrame = Frame(fltrFrame, relief=GROOVE)
        fltrStarFrame.grid(row=0, column=2, ipadx=5, padx=2, pady=5)
        
        fltrStarLabel = Label(fltrStarFrame, text="Stars:")
        fltrStarLabel.grid(padx=5, pady=10, sticky=E)
        
        self.chooseStar = 0
        starLabel = {}
        iStar = self.addImage("images/icons/logo_blankStar.png", image="icon")
        for star in range(5):
            starLabel[star] = Label(fltrStarFrame, image=iStar)
            starLabel[star].image = iStar
            starLabel[star].name = str(star+1)
            starLabel[star].grid(row=0, column=star+1, sticky=E)        
      
        fltrSkillFrame = Frame(fltrFrame, relief=GROOVE)
        fltrSkillFrame.grid(row=0, column=3, pady=5)
        
        fltrSkillLabel = Label(fltrSkillFrame, text="Skill:")
        fltrSkillLabel.grid(padx=5, pady=10, sticky=E)        
      
        fltrSkill = AutocompleteCombobox(fltrSkillFrame)
        fltrSkill.grid(row=0, column=1, padx=5, pady=10, sticky=W)      
        fltrSkill.set_completion_list([""] + self.getSkillList()) 
        
        resetButton = Button(srchFrame, text="Reset")
        resetButton.grid(row=0, column=2, padx=10, pady=10, sticky=E)
        resetButton.bind("<Button-1>", self._resetTab)
                    
        self.attrDict = attrDict
        self.srchCombo = srchCombo
        self.fltrFaction = fltrFaction
        self.fltrSkill = fltrSkill
        self.sklSrchButton = sklSrchButton
        self.srchButton = srchButton
        self.starLabel = starLabel
        
        return tab
    
    
    def _resetTab(self, event):
        
        self.srchCombo.focus_set()
        
        try:
            self.fltrFaction[self.fctnChoice.get()].deselect()
            self.fctnChoice.set("")
        except KeyError:
            pass
        
        self.fltrSkill.set("")
        stars = self.chooseStar = 0
        
        iStarOn = self.addImage("images/icons/logo_Star1.png", image="icon")
        iStarOff = self.addImage("images/icons/logo_blankStar.png", image="icon")
        
        for star in range(stars):
            self.starLabel[star].config(image=iStarOn)
            self.starLabel[star].image = iStarOn

        for star in range(stars,5):
            self.starLabel[star].config(image=iStarOff)
            self.starLabel[star].image = iStarOff   
                
        self.srchCombo['values'] = self.allCreatures    
    
    
    
    def _creatureTabEvents(self):
         
        #skill toolTip event
        ToolTip(self.attrDict["Level0Skill"], mode="skill")         
        ToolTip(self.attrDict["Level5Skill"], mode="skill")   
        ToolTip(self.attrDict["Level10Skill"], mode="skill")     

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
            
            cost = self.creature.Cost.item()
            
            if source == "15":
                cost = self.creature.CostAtMeld.item()
            if cost == "":
                cost = self.creature.Cost.item()
                    
            self.attrDict["Cost"].configure(state=NORMAL)
            self.attrDict["Cost"].delete(0, END)
            self.attrDict["Cost"].insert(END, cost)
            self.attrDict["Cost"].configure(state="readonly")                                      
        
        for rb in levelRB.values():
            rb.bind("<Enter>", _levelRBevent)
            rb.bind("<Leave>", _levelRBevent)
        
        
        #skill Events
        for i in range(3):
            self.sklSrchButton[i].bind("<ButtonRelease>", self.srchSkillTab)
        
        #search Events        
        self.srchCombo.bind("<Return>", self.updateCreature)
        self.srchCombo.bind("<<ComboboxSelected>>", self.updateCreature) 
        
        #filter Events          
        self.fltrSkill.bind("<<ComboboxSelected>>", self.updateSearchCombolist)    
        self.fltrSkill.bind("<Return>", self.updateSearchCombolist)    
              
        def _deselect(event):
            if event.widget.cget("value") == self.fctnChoice.get():
                event.widget.deselect()
                self.fctnChoice.set("")
                self.updateSearchCombolist()
        
        for fctn in self.fltrFaction.values():
            fctn.bind("<ButtonRelease>", _deselect)
            ToolTip(fctn, mode="faction", delay=700)   
  
        
        def _starEvent(event):
            iStarOn = self.addImage("images/icons/logo_Star1.png", image="icon")
            iStarOff = self.addImage("images/icons/logo_blankStar.png", image="icon")

            if event.type == "4": #<Button-1> event - left-click mouse
                self.chooseStar = int(event.widget.name)
          
            stars = self.chooseStar
            
            if event.type == "7": #<Enter> event
                stars = int(event.widget.name)

            elif event.type == "8": #<Leave> event
                stars = int(self.chooseStar)            
                
            for star in range(stars):
                self.starLabel[star].config(image=iStarOn)
                self.starLabel[star].image = iStarOn

            for star in range(stars,5):
                self.starLabel[star].config(image=iStarOff)
                self.starLabel[star].image = iStarOff   
                                         
        
        for strLabel in self.starLabel.values():
            strLabel.bind("<Enter>", _starEvent)
            strLabel.bind("<Leave>", _starEvent)
            strLabel.bind("<Button-1>", _starEvent)
            strLabel.bind("<ButtonRelease>", self.updateSearchCombolist)                       
    
    
    
    def updateSearchCombolist(self, event=None, **kwargs):
        
        fltrTable = self.allCreatures
        
        if self.chooseStar == 0:
            fltrStar = None
        else:
            fltrStar = str(self.chooseStar)
    
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
       
                if attr in ["CreatureName", "Script"]:
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
                
                
                elif isinstance(child, Text):
                    child.configure(state=NORMAL)
                    child.delete(1.0, END)
                    child.insert(END, creature_[attr].item())
                    child.configure(state=DISABLED) 
                      
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
        
        return tab
        
 
    def srchSkillTab(self, event=None):
        self.notebook.select(self.sk_tab)


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
        
        creature = pd.read_csv('data/creatures.csv', dtype=str, keep_default_na=False)
        
        skills = creature["Level0Skill"]
        skills = skills.append(creature["Level5Skill"])
        skills = skills.append(creature["Level10Skill"])
        skills = [skl for skl in skills.unique()]
        
        return sorted(skills)
        
        
    
    def getCreatureList(self, fltrFaction=None, fltrStar=None, fltrSkill=None):
        
        creature = pd.read_csv('data/creatures.csv', dtype=str, keep_default_na=False)   
        
        if fltrFaction and fltrFaction not in ["Faction",""]:
            creature = creature[creature.Faction==fltrFaction]
        if fltrStar and fltrStar not in ["Stars",""]:
            creature = creature[creature.StarRating==fltrStar]
        if fltrSkill and fltrSkill not in ["Skill",""]:
            creature = creature[(creature.Level0Skill==fltrSkill) | (creature.Level5Skill==fltrSkill)\
                                | (creature.Level10Skill==fltrSkill)]
            
        return sorted(creature.CreatureName.values.tolist())        
  

    def fetchCreature(self, cr_code):
        
        creature = pd.read_csv('data/creatures.csv', dtype=str, keep_default_na=False)   
        creature_desc = pd.read_csv('data/creature_desc.csv', keep_default_na=False, encoding = "ISO-8859-1")
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
        
        heroes = pd.read_csv('data/heroes.csv', dtype=str, keep_default_na=False)
        
        if he_name in heroes.HeroName.values:
            query = heroes[heroes.HeroName==he_name].reset_index(drop=True)
        else:
            query = heroes[heroes.HeroName=="Null"].reset_index(drop=True)
            
        return query.to_dict()    

   

def fetchSkillDesc(skill):
        
    skills = pd.read_csv('data/creature_skill_desc.csv', dtype=str, keep_default_na=False)
        
    if skill in skills.SkillName.values:
        text = skills.Description[skills.SkillName==skill].item()
    else:
        text = "No entry"
            
    return text    


class AutocompleteCombobox(Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(INSERT),END)
                        self.position = self.index(END)
                if event.keysym == "Left":
                        if self.position < self.index(END): # delete the selection
                                self.delete(self.position, END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, END)
                if event.keysym == "Right":
                        self.position = self.index(END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion
    
    
class ToolTip:

    def __init__(self, master, **opts):
        self.master = master
        self.delay = 0
        if "delay" in opts.keys():
            self.delay = opts["delay"]
        
        self._tipwindow = None
        self._opts = opts
        self._id = None
        self._id1 = self.master.bind("<Enter>", self.enter, '+')
        self._id2 = self.master.bind("<Leave>", self.leave, '+')
        self._id3 = self.master.bind("<ButtonPress>", self.leave, '+')
        self._id4 = self.master.bind("<Motion>", self.motion, '+')

    def enter(self, event=None):
        self._schedule()

    def leave(self, event=None):
        self._unschedule()
        self._hide()

    def motion(self, event=None):
        if self._tipwindow:
            x, y = self.coords()
            self._tipwindow.wm_geometry("+%d+%d" % (x,y))

    def _schedule(self):
        self._unschedule()
        self._id = self.master.after(self.delay, self._show)

    def _unschedule(self):
        id = self._id
        self._id = None
        if id:
            self.master.after_cancel(id)

    def _show(self):
        if not self._tipwindow:
            self._tipwindow = tw = Toplevel(self.master)
            tw.withdraw()
            tw.wm_overrideredirect(1)

            #if tw.tk.call("tk", "windowingsystem") == 'aqua':
            #    tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w, "help", "none")

            self.create_contents()
            tw.update_idletasks()
            x, y = self.coords()
            tw.wm_geometry("+%d+%d" % (x, y))
            tw.deiconify()               

    def _hide(self):
        tw = self._tipwindow
        self._tipwindow = None
        if tw:
            tw.destroy()

    def coords(self):
        tw = self._tipwindow
        twx, twy = tw.winfo_reqwidth(), tw.winfo_reqheight()
        w, h = tw.winfo_screenwidth(), tw.winfo_screenheight()
        y = tw.winfo_pointery() + 20
        if y + twy > h:
            y = y - twy - 30
        x = tw.winfo_pointerx() #- twx / 2
        if x < 0:
            x = 0
        elif x + twx > w:
            x = w - twx
        return x, y    

    def create_contents(self):
        opts = self._opts.copy()

        textopts = {"background":"white", "font":"Helvetica 8", "padx":5, "pady":5,\
                    "height":1, "width":10, "wrap":WORD, "relief":SOLID, "borderwidth":1}#"#ffffe0"
        
        if opts["mode"] == "skill":
            skill = self.master.get()
            text = fetchSkillDesc(skill)
        elif opts["mode"] == "faction":
            text = self.master.cget("value")
        
        if len(text) <= 40:
            textopts["width"] = len(text)+1
            textopts["height"] = 1
        else:
            textopts["width"] = 40
            textopts["height"] = max(math.ceil(len(text)/40), 1)


            
        hover = Text(self._tipwindow, **textopts)
        hover.tag_configure(CENTER, justify='center')
        hover.tag_add(CENTER, 1.0, "end")
        hover.insert(END, text)
        hover.pack(expand=1)

def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    
def main():
       
    root = Tk()
    ex = DeckHeroes(root)
    #root.geometry("%dx%d+100+100"%(WIDTH,HEIGHT))
    center(root)
    root.resizable(width=False, height=False)
    root.mainloop()  


if __name__ == '__main__':
    main()  