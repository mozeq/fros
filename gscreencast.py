import re
import os
from ScreencastBase import ScreencastBase

#sys.path.append(sys.path[0]+ "/plugins")
PLUGIN_DIR = "."
#ignore_pattern = "(__init__.py)|(\w*\.pyc)"
#ignore_regexp = re.compile(ignore_pattern)
plugin_pattern = r"\w*\.py$"
plugin_regexp = re.compile(plugin_pattern)


def find_plugins():
    plugins = []
    for plugin in ScreencastBase.__subclasses__():
        try:
            instance = plugin()
            plugins.append(instance)
        except Exception, ex:
            print plugin, ex
            pass  # ignore failed plugins, they are not usable for current env

    return plugins


def load_plugins(dir="plugins"):
    for plugin in os.listdir(dir):
        if plugin_regexp.match(plugin):
            print "loading: ", plugin
            __import__("%s.%s" % (dir, plugin[:-3]), None, None, [''])
        else:
            print "ignoring: ", plugin

    return find_plugins()

if __name__ == "__main__":
    plugins = load_plugins("plugins")
    print plugins
    for plugin in plugins:
        print plugin.Screencast()
        raw_input("Recording...")
        plugin.StopScreencast()
