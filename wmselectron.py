import os, commands, Tix as Tk
from Selectron import Selectron
import TkGeomSavers as TkGeom

class WindowInfo:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def __str__(self):
        return self.name

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
        wmctrlout = commands.getoutput('wmctrl -Gl')
        windows = wmctrlout.splitlines()
        for win in windows:
            try:
                junk, flags, x, y, width, height, host, name = \
                    win.split(None, 7)
                self.windows.append(WindowInfo(name, x, y, width, height))
            except ValueError:
                # wmctrl is b0rked
                # the height and host got merged somehow :-/
                junk, flags, x, y, width, heighthost, name = \
                    win.split(None, 6)
                self.windows.append(WindowInfo(name, x, y, width, 0))

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
            os.system('wmctrl -a "%s"' % obj.name)
            if self.autohide:
                self.hide()

if __name__ == "__main__":
    import time
    timekey = time.asctime()
    root = TkGeom.TkRootGeomSaver('wmselectron')
    root.title("WMSelectron - " + timekey)
    z = WMSelectron(root, key=timekey)
    z.pack(expand=1, fill='both')
    Tk.mainloop()
