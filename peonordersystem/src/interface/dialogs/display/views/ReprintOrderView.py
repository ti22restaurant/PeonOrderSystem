"""This module defines the ReprintOrderView
class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from .abc.View import View
from .BaseDialog import BaseDialog
from .layout.BaseLayout import BaseLayout
from .components.OrderDisplayComponent import OrderDisplayComponent

from peonordersystem.src.interface.dialogs.DialogBuilder import PRIMARY_SELECTION_SIGNAL
from peonordersystem.src.interface.dialogs.display.mappers.SignalMapper import SignalMapper


class ReprintOrderView(View):
    """Provides the basic functionality
    for display a tree view in a simple
    dialog window expected titles of the
    columns are order and time.
    """

    def __init__(self, parent, title="Reprint Order Dialog"):
        """Initializes the view"""
        self._mapper = SignalMapper()
        self._dialog = BaseDialog(parent, title)
        self._layout = BaseLayout()
        self._component = OrderDisplayComponent()
        self._build_view()

    def _build_view(self):
        """Builds the view"""
        self._layout.add_component(self._component)
        self._dialog.set_layout(self._layout)
        self._set_up_mappings()

    def set_models(self, *args):
        """Sets the models associated
        with the views.

        @param args: list of Gtk.TreeModels
        where the first model is to be used
        """
        model = args[0].model
        self._component.set_model(model)

    def set_mapper(self, mapper):
        """ Sets the current mapper
        used by the view.

        @param mapper: SignalMapper
        """
        self._mapper = mapper

    def _set_up_mappings(self):
        """Sets up the mappings
        to be used by this view
        """
        self._component.set_selection_func(self._function_signal)

    def _function_signal(self, selection, model, path, path_currently_selected, *args):
        """Maps the set selection function call
        and filters the parameters to be passed
        to the SignalMapper.

        @param selection: Gtk.Selection

        @param model: Gtk.TreeModel

        @param path: Gtk.TreePath

        @param path_currently_selected: bool

        @param args: catchall to be passed
        to the mapped function

        @return: bool representing if the
        selection should be made
        """
        itr = model.get_iter(path)
        return self._mapper.signal(PRIMARY_SELECTION_SIGNAL, itr, *args)

    def run(self):
        """Runs the main loop
        of the dialog window for
        this view.

        @return: Gtk.ResponseType
        representing the response
        to the dialog window
        """
        return self._dialog.run_dialog()