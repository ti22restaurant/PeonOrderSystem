"""This module defines the container that
is used to store and display key data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from .abc.Container import Container
from .components.DateCreator import DateCreator
from .components.TimeCreator import TimeCreator


class KeyContainer(Container):
    """Container used to store keys
    data.
    """

    KEY_COMPONENTS = {
        'TIMES': TimeCreator,
        'DATES': DateCreator
    }

    def __init__(self, component_name, *args):
        """Initializes the KeyContainer with the
        given _components.

        @param component_name: str representing the
        values to create for this KeyContainer.

        @param args: arguments to be passed to the
        component.
        """
        self._component = self._get_component_from_str(component_name, *args)

    def _get_component_from_str(self, name, *args):
        """Gets the _components data from the given
        string and passes the arguments to the
        generated _components.

        @param name: str representing the creator
        component to generate.

        @param args: arguments to be passed to the
        component.

        @return: component that has been generated.
        """
        return self.KEY_COMPONENTS[name](*args)

    @property
    def data(self):
        """Gets the keys data
        associated with this
        container.

        @return: tuple of keys
        representing the generated
        keys.
        """
        return self._component._data

    def add(self, data):
        """Adds the given data
        to the keys.

        @param data: object to
        be added to the keys.

        @return: None
        """
        pass

    def get_data_format(self, format_data):
        """Gets the format data used to display
        the keys data.

        @param format_data: FormatData object
        that is used to store the format data.

        @return: format that is used to display
        any given index of the stored data.
        """
        return self._component.get_data_format(format_data)
