#! /usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

"""This module contains the PeonOrderSystem class which 
is the top level object that generates and controls
the PeonOrderSystem GUI.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport

from peonordersystem.interface.UI import UI

class PeonOrderSystem(UI):
    """Generates and controls the PeonOrderSystem GUI and
    establishes its functionality.
    """
    def __init__(self, title='Fish Cake Factory'):
        """Initializes and displays PeonOrderSystem GUI
        
        @keyword title: Keyword argument that sets the title
        of the main GUI window. Default value is 'Fish Cake
        Factory'
        """
        super(PeonOrderSystem, self).__init__(title)
        
if __name__ == '__main__':
    USER = PeonOrderSystem()
    Gtk.main()
