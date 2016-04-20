from tkinter import *
from tkinter.font import Font, nametofont
import time
import redis
import config as cf
import cardlookup as lookup
import hashlib
import audioplayer

class View(Frame):
    db = None
    double_allow = None
    def __init__(self, *args, **kwargs):
        Frame.__init__(self)
        self.db = redis.Redis(kwargs['redis_host'])
        self.double_allow = kwargs['double_allow']
        scrollbar = Scrollbar(self)
        scrollbar.pack( side = RIGHT, fill=Y )
        self.mylist = Listbox(self, yscrollcommand = scrollbar.set )
        with open(kwargs['infile'], newline='') as dfile:
            for line in dfile.readlines():
                self.mylist.insert(END, line.strip())

        self.mylist.pack( side = BOTTOM, fill = BOTH, expand = 1 )
        scrollbar.config( command = self.mylist.yview )
        self.b = Button(self, text="Vote", command=self.button_click)
        self.b.pack(side=TOP, fill=X, pady=50)

    def button_click(self):
        window = Toplevel(self, bg='red')
        label = Label(window, text="Please scan ID", bg='red')
        label.pack(side="top", fill="both", padx=30, pady=70)
        self.b.configure(state=DISABLED)
        self.update()
        #scan card here
        cs = lookup.getCardNonBlocking()
        self.b.configure(state=NORMAL)
        val = self.mylist.curselection()
        self.mylist.selection_clear(0,END)
        window.destroy()
        if(len(val) == 0):
            print("No option selected")
            audioplayer.playWav(cf.fail_sound)
            return
        val = self.mylist.get(val)
        
        if not cs:
            print("No card detected")
            audioplayer.playWav(cf.fail_sound)
            return
        
        if not(cs[1] in cf.valid_facilities):
            #not an IIT card
            print("Not an IIT Card!")
            audioplayer.playWav(cf.fail_sound)
            return
        rawstr = str(cs[0])+str(cs[1])+cf.hash_salt
        cardh = hashlib.sha256(rawstr.encode('utf-8')).hexdigest()
        
        if not(cardh in self.double_allow):
            if self.db.sismember('voters', cardh):
                print("%s is not allowed to double vote" % cardh)
                audioplayer.playWav(cf.fail_sound)
                return
        
        self.db.lpush(val,cardh)
        self.db.sadd('voters',cardh)
        print("Successful vote for ",val)
        audioplayer.playWav(cf.pass_sound)
if __name__ == "__main__":
    root = Tk()
    default_font = nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    view = View(root, redis_host='localhost', infile=cf.infile, double_allow=cf.double_allow)
    view.pack(side="top", fill="both", expand=True)
    root.title("IPRO Day People's Choice")
    root.mainloop()

