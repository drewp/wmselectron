import os, commands, Tix as Tk
from Selectron import Selectron
import TkGeomSavers as TkGeom
import wmctrl

class WMSelectron(Tk.Frame):
    def __init__(self, master, key, autohide=1):
        Tk.Frame.__init__(self, master, width=700)
        self.key = key
        self.autohide = autohide

        self.selectron = None
        self.windows = None
        self.refresh()
        self.bind("<Expose>", self.refresh)
    def hide(self, *args):
        os.system('wmctrl -r "WMSelectron - %s" -b add,hidden' % self.key)
    def refresh(self, *args):
        self.windows = []
        self.windows = wmctrl.windowList()

        if self.selectron:
            self.selectron.pack_forget()
        self.selectron = Selectron(self, sort=1, objects=self.windows,
            command=self.selectron_callback, case_sensitive=0)
        self.selectron.pack(expand=1, fill='both')
        self.selectron.listbox.configure(bg='black', fg='white')
        self.selectron.entry.configure(bg='black', fg='white')
        self.selectron.entry.bind('<Escape>', self.hide)
        os.system('wmctrl -r "WMSelectron - %s" -b add,sticky' % self.key)
    def selectron_callback(self, objs):
        if len(objs) == 1:
            obj = objs[0]
            if self.autohide:
                self.hide()
            os.system('wmctrl -a "%s"' % obj.name)

if __name__ == "__main__":
    import time
    timekey = time.asctime()
    root = TkGeom.TkRootGeomSaver('wmselectron')
    root.title("WMSelectron - " + timekey)
    z = WMSelectron(root, key=timekey)
    z.pack(expand=1, fill='both')
    Tk.mainloop()
