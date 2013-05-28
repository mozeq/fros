class ScreencastBase(object):
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
        return False
