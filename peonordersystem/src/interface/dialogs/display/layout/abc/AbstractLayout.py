"""This module defines the basic fucntionality
of the abstract layout class

@author: Carl McGraw
@email: cjmcgraw@u.washington.edu
@version: 1.1
"""

from abc import ABCMeta, abstractproperty, abstractmethod


class AbstractLayout(object):
    """Provides the external facing functionality
    for the Layout class
    """
    
    __metaclass__ = ABCMeta
    
    @abstractproperty
    def main_component(self):
        """Gets the main component
        
        @return: Gtk.Widget
        """
        pass
    
    @abstractmethod
    def confirm(self):
        """Confirms the data and
        returns the result of the
        data.
        
        @return: result
        """
        pass
    
    @abstractmethod
    def cancel(self):
        """Cancels the data
        and returns any potential
        cancelled result
        
        @return: result
        """
        pass
