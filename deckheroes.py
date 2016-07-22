from Tkinter import *
from PIL import Image, ImageTk
import pandas as pd

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack(fill=X)    
                                
        m = PanedWindow(frame)
        m.pack(fill=BOTH, expand=1)
        
        images = ["cr_apprentice_1.jpg", "cr_aquarius_1.jpg", "cr_pikeman_1.jpg",
                 "cr_marksman_1.jpg", "cr_scout_1.jpg", "cr_zealot_1.jpg"]
        
        for image in images:
        
            img = Image.open("images/creatures/%s"%(image))
            img = img.resize((250,400), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)

            _img = Label(master,image=photo)
            _img.image = photo
            m.add(_img)

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()

app = App(root)

root.mainloop()
root.destroy()