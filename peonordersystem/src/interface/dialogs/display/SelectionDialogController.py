"""This module provides the
SelectionDialogController class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from .abc.AbstractController import AbstractController
from .models.StandardModel import StandardModel
from .views.OrderView import OrderView
from .mappers.SignalMapper import SignalMapper

from peonordersystem.src.interface.dialogs.DialogBuilder import PRIMARY_SELECTION_SIGNAL


class SelectionDialogController(AbstractController):
    """Controls the view and model for
    a selection dialog where a selection
    is made on a single string
    """
    PROP_NAME_ORDERS = 'orders'
    PROP_NAME_SELECTION = 'selection'

    TOGO_NAME_FORMAT = "{name} ({num})"
    DEFAULT_MODEL_TYPES = (str,)

    def __init__(self):
        """Initializes the SelectionDialogController"""
        self._current_selection = None
        self._orders = {}

        self._model = StandardModel(self.DEFAULT_MODEL_TYPES)
        self._view = OrderView(None)
        self._mapper = self._configure_mapper()
        self._configure_view()
        self.set_properties()

    def set_properties(self, **kwargs):
        """Sets the properties associated
        with the controller

        @param kwargs: keyword catchall
        that allows for 'orders' key to
        be defined
        """
        self._set_properties(kwargs)
        self._update_model()

    def _set_properties(self, kwargs):
        """Sets the properties to those
        specified in the given argument

        @param kwargs: dict representing
        property values
        """
        self._orders = self._generate_orders(kwargs)

    def _generate_orders(self, kwargs):
        """Generates the data from
        the orders field of the
        properties

        @param kwargs: dict of keywords
        that contains 'orders'

        @return: dict of orders mapped
        from their display names to their
        data names
        """
        if self.PROP_NAME_ORDERS in kwargs:
            return self._build_orders_from_data(kwargs[self.PROP_NAME_ORDERS])
        return {}

    def _build_orders_from_data(self, orders_data):
        """Builds the orders from
        the data.

        @param orders_data: list
        of names or tuples of names.

        @return: dict of display names
        mapped to actual order data names
        """
        return {self._parse_name(x): x for x in orders_data}

    def _parse_name(self, name):
        """Parses an orders name
        into a display name

        @param name: str

        @return: str
        """
        if isinstance(name, tuple):
            return self._parse_tuple_name(name)
        return name

    def _parse_tuple_name(self, data):
        """Parses an order name as
        a tuple into a display name

        @param data: tuple of str

        @return: str
        """
        name, number = data[:2]
        return self.TOGO_NAME_FORMAT.format(name=name, num=number)

    def _update_model(self):
        """Updates the model with the
        currently stored order display
        names
        """
        self._model.clear()
        for order in self._orders:
            self._model.append((order,))

    def get_properties(self):
        """Gets the properties associated
        with the controller

        @return: dict of values representing
        the properties.
        """
        return {self.PROP_NAME_ORDERS: self._orders,
                self.PROP_NAME_SELECTION: self._orders[self._current_selection]}

    def _configure_mapper(self):
        """Configures the mapper
        for the controllers bindings

        @return: SignalMapper
        """
        mapper = SignalMapper()
        mapper.register_function(self._selection_made, PRIMARY_SELECTION_SIGNAL)
        return mapper

    def _selection_made(self, itr, *args):
        """Function called when a selection on
        the view has been made and the mapped
        signal is called.

        @param itr: Gtk.TreeIter

        @param args: catchall catches
        random arguments

        @return: bool value representing
        if the selection should be made
        """
        self._current_selection, = self._model[itr]
        return True

    def _configure_view(self):
        """Configures the view to the
        current state
        """
        self._view.set_models(self._model)
        self._view.set_mapper(self._mapper)

    def run(self):
        """Runs the dialog to retrieve
        user order selection

        @return: Gtk.ResponseType
        """
        return self._view.run()