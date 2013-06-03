from pyfros.plugins import const
from pyfros.froslogging import info
#pylint: disable=E0611
from gi.repository import Gdk
import os
import sys


class ScreencastResult(object):
    def __init__(self, result, filename):
        self.success = result
        self.filename = filename


class ScreencastBase(object):
    wroot = None
    wwidth = None
    wheight = None
    save_to = None
    width = None
    height = None
    x = None
    y = None

    def _dummy_progress(self, percent):
        sys.stdout.write("Processing: %.3i%%\r" % percent)
        sys.stdout.flush()

    #pylint: disable=W0613
    def __init__(self, *args, **kwargs):
        self.progress_update = kwargs.get("progress_update", self._dummy_progress)
        self.output = kwargs.get("output", os.path.join(os.getcwd(), "screencast"))

    def SetProgressUpdate(self, progress_cb):
        self.progress_update = progress_cb

    def Screencast(self):
        raise NotImplementedError

    def ScreencastArea(self):
        raise NotImplementedError

    def StopScreencast(self, end_handler):
        raise NotImplementedError

    # whether the plugin is suitable for actual desktop
    def IsSuitable(self):
        return const.SUITABLE_NOT_SUITABLE

    def SelectArea(self, widget, result_handler):
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
        result_handler(True)  # true means - area was selected
