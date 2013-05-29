from plugins import const


class ScreencastResult(object):
    def __init__(self, result, filename):
        self.success = result
        self.filename = filename


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
        return const.SUITABLE_NOT_SUITABLE
