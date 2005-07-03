# wmctrl calling and parsing

import os, commands

class WindowInfo:
    def __init__(self, name, x, y, width, height, wid, desk):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.wid = wid # as hex literal
        self.desk = int(desk)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "WindowInfo(%r, %r, %r, ...)" % (self.name, self.x, self.y)

    def area(self):
        return self.width * self.height

class DesktopInfo:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        

def windowList():
    winlist = []
    wmctrlout = commands.getoutput('wmctrl -Gl')
    windows = wmctrlout.splitlines()
    for win in windows:
        # wmctrl sometimes mashes h and host together, but the left
        # part seems to be fixed-width
        wid, desk, x, y, w, h = win[:33].split(None, 5)
        host, name = win[33:].split(None, 1)
        winlist.append(WindowInfo(name, x, y, w, h, wid, desk))
    return winlist

def activeDesktopWorkareaSize():
    for line in commands.getoutput("wmctrl -d").splitlines():
        words = line.split(None,9)
        if words[1] == "*":
            WA = words.index("WA:")
            if words[WA+1] == "N/A":
                raise ValueError(
                 "wmctrl returned no work area size for desktop %s" % words[0])
            
            try:
                w,h = words[WA+2].split('x')
                return int(w),int(h)
            except ValueError:
                raise ValueError("couldn't get size from work area %r" %
                                 words[8])
    raise ValueError("output of 'wmctrl -d' had no starred lines")

class gravity:
    """from http://standards.freedesktop.org/wm-spec/wm-spec-1.3.html#id2506756

    for the formulas, see also
    http://standards.freedesktop.org/wm-spec/wm-spec-1.3.html#id2508199
    """
    default = 0
    NorthWest = 1
    North = 2
    NorthEast = 3
    West = 4
    Center = 5
    East = 6
    SouthWest = 7
    South = 8
    SouthEast = 9
    Static = 10
    
UNCHANGED = -1
def resizeAndMove(win, x=UNCHANGED, y=UNCHANGED, w=UNCHANGED, h=UNCHANGED,
                  grav=gravity.default):
    use_id = ""
    if hasattr(win,'wid'):
        win = win.wid
        use_id = "-i"

    args = (use_id, win, grav, x, y, w, h)

    cmd = "wmctrl %s -r %r -e %d,%d,%d,%d,%d" % args
    os.system(cmd)
