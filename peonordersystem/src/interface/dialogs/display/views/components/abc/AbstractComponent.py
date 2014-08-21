"""Provides the AbstractComponent
class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""

from abc import ABCMeta, abstractproperty


class AbstractComponent(object):
    """Describes the required basic
    functionality for a class to be
    a component
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def main_component(self):
        """Gets the main component of
        the component to be displayed

        @return: Gtk.Container
        """
        pass