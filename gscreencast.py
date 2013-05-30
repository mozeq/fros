#! /bin/python
# -*- coding: utf-8 -*-


import re
import os
from ScreencastBase import ScreencastBase
from froslogging import warn, info, set_verbosity, error

#sys.path.append(sys.path[0]+ "/plugins")
PLUGIN_DIR = "."
#ignore_pattern = "(__init__.py)|(\w*\.pyc)"
#ignore_regexp = re.compile(ignore_pattern)
plugin_pattern = r"\w*\.py$"
plugin_regexp = re.compile(plugin_pattern)


def load_plugins(plugin_dir="plugins"):
    plugins = []
    for plugin in os.listdir(plugin_dir):
        if plugin_regexp.match(plugin):
            info("loading: %s" % plugin)
            try:
                module = __import__("%s.%s" % (plugin_dir, plugin[:-3]), fromlist=["getScreencastPluginInstance"])
                try:
                    instance = module.getScreencastPluginInstance()
                    if instance.IsSuitable() > 0:  # append only suitable plugins
                        plugins.append(instance)
                    info("Added plugin:", instance)
                except Exception, ex:
                    warn("'{0}' is not a plugin: '{1}'".format(plugin, ex))
            except ImportError, ex:
                warn("Module '{0}' doesn't provide getPluginInstance() function, so it's not a plugin: {1}".format(plugin, ex))
        else:
            #print "ignoring: ", plugin
            pass

    # return plugins sorted by their IsSuitable weight, the best match first
    return sorted(plugins, key=lambda plugin: plugin.IsSuitable(), reverse=True)

if __name__ == "__main__":
    plugins = load_plugins("plugins")
    print plugins
    for plugin in plugins:
        result = plugin.Screencast()
        raw_input("Recording...")
        plugin.StopScreencast()
        if result.success:
            print "Screencast was saved to: '{0!s}'".format(result.filename)
            break  # screencasting is done, no need to run another plugin
