from plugins import const
from froslogging import info
from gi.repository import Gdk
import os


class ScreencastResult(object):
    def __init__(self, result, filename):
        self.success = result
        self.filename = filename


class ScreencastBase(object):
    selected_area = None
    wroot = None
    wwidth = None
    wheight = None
    save_to = None
    width = None
    height = None
    x = None

    def __init__(self):
        pass

    def Screencast(self):
        raise NotImplementedError

    def ScreencastArea(self):
        raise NotImplementedError

    def StopScreencast(self):
        raise NotImplementedError

    # whether the plugin is suitable for actual desktop
    def IsSuitable(self):
        return const.SUITABLE_NOT_SUITABLE

    def SelectArea(self, *args):
        """
        Calls xwinfo to get area which user would like to record
        """

        self.wroot = Gdk.get_default_root_window()
        self.wwidth = self.wroot.get_width()
        self.wheight = self.wroot.get_height()

        xwininfo_com = ['xwininfo', '-frame']
        (stdin, stdout, stderr) = os.popen3(xwininfo_com, 't')
        wid = stdout.readlines()
        stdin.close()
        stdout.close()
        stderr.close()
        x = y = width = height = None
        for i in wid:
            if i.lstrip().startswith('Absolute upper-left X:'):
                x = int(i.split(' ')[len(i.split(' '))-1])
            elif i.lstrip().startswith('Absolute upper-left Y'):
                y = int(i.split(' ')[len(i.split(' '))-1])
            elif i.lstrip().startswith('Width:'):
                width = int(i.split(' ')[len(i.split(' '))-1])
            elif i.lstrip().startswith('Height:'):
                height = int(i.split(' ')[len(i.split(' '))-1])

        if x <= 0:
            width += x
            x = 1  # recordmydesktop accepts only values > 0
        if y <= 0:
            height += y
            y = 1
        if width + x > self.wwidth:
            width = self.wwidth - x
        if height + y > self.wheight:
            height = self.wheight - y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        info(self.x, self.y, self.width, self.height)
        self.selected_area = (self.x, self.y, self.width, self.height)
