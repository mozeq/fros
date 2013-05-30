#! /bin/python
# -*- coding: utf-8 -*-


import re
import os
import sys
from froslogging import warn, info, set_verbosity, error
from Controls import Controls
from gi.repository import Gtk

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
    verbose = 0
    set_verbosity(1)
    if len(sys.argv) < 2:
        print ("Usage: {0} -o OUTPUT_FILE").format(sys.argv[0])
        sys.exit(1)

    output_file = None
    plugins = load_plugins("plugins")
    if sys.argv[1] == "is-available":
        exitcode = 0 if plugins else 1
        sys.exit(exitcode)

    if not plugins:
        error("No suitable plugin found!")
        sys.exit(1)

    try:
        output_file = sys.argv[1]
    except IndexError, ex:
        print ("Usage: abrt-screencast -o OUTPUT_FILE")
        sys.exit(1)

    info("Selected plugin: ", plugins[0])
    controls = Controls(plugins[0])
    controls.show_all()
    Gtk.main()
