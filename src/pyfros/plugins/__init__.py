__package__ = "pyfros.plugins"

import pkgutil

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    print "adding: ", module_name
    __all__.append(module_name)
