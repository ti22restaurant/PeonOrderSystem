"""This module provides the
abstract base class for the
SelectionObserverable.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractSelectionObservable(object):
    """Describes the necessary functionality
    for an object to be SelectionObservable.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def register_selection_observation(self, observer_ref):
        """Registers the given observer as
        a selection observer.

        @param observer_ref: AbstractObserver
        to be registered to the observerable.

        @return: None
        """
        pass

    @abstractmethod
    def unregister_selection_observation(self, observer_ref):
        """Removes the given observer as
        a selection observer.

        @param observer_ref: AbstractObserver
        to be unregistered from observerable.

        @return: None
        """
        pass

    @abstractmethod
    def notify_selection(self, *args):
        """Notifies the observers that
        a selection has been made.

        @param args: Arguments that are
        to be passed to the observers.

        @return: None
        """
        pass
