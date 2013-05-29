from ScreencastBase import ScreencastBase
import const


class ScreencastRecordMyDesktop(ScreencastBase):
    def __init__(self):
        super(ScreencastRecordMyDesktop, self).__init__()

    def Screencast(self):
        print "Screencast ScreencastRecordMyDesktop"

    def ScreencastArea(self):
        print "ScreencastArea ScreencastRecordMyDesktop"

    def StopScreencast(self):
        print "Stop ScreencastRecordMyDesktop"

    def IsSuitable(self):
        return const.SUITABLE_DEFAULT  # 1 is default
