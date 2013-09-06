#! /usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

"""Contains PeonOrderSystem class, and main method if this
is called as main. Main method generates an instance of the
PeonOrderSystem class
"""

from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport

from peonordersystem.interface.UI import UI

class PeonOrderSystem(UI):
    """Generates and controls the PeonOrderSystem GUI and
    establishes its functionality.
    """
    def __init__(self, title):
        """Creates PeonOrderSystem"""
        super(PeonOrderSystem, self).__init__(title)
        
if __name__ == '__main__':
    USER = PeonOrderSystem("Fish Cake Factory")
    Gtk.main()