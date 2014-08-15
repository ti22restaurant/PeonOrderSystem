"""This module defines the basic functionality for a dialog
window.

@author: Carl McGraw
@email: cjmcgraw@u.washington.edu
@version: 1.1
"""

from.abc.AbstractDialog import AbstractDialog
from peonordersystem.src.interface.dialogs.DialogBuilder import (PACK_ARGS,
                                                                 generate_default_dialog,
                                                                 generate_default_button)


class BaseDialog(AbstractDialog):
    """Represents the general base dialog
    container that holds layout components
    """
    DEFAULT_CANCEL_BUTTON_NAME = "cancel"
    DEFAULT_CONFIRM_BUTTON_NAME = "confirm"

    ERROR_MSG = "Invalid State: Layout of dialog hasn't been set!"

    def __init__(self, parent, title, dialog=None, default_size=(400, 400)):
        """initializes the dialog window"""
        self._parent = parent
        self._title = title
        self._default_size = default_size
        self._dialog = self._create_dialog_window()
        self._response = self.CANCEL_RESPONSE
        self._layout = None

    def set_layout(self, layout):
        """Sets the layout to the given
        parameter

        @param layout: Gtk.Widget
        """
        self._set_state(layout)
        self._connect_layout()

    def _connect_layout(self):
        """Connects the current
        layout to the dialog.
        """
        content_area = self._dialog.get_content_area()
        content_layout = self._layout.main_component
        content_area.pack_start(content_layout, *PACK_ARGS)

    def _clear_layout(self):
        """Clears the current layout
        from the current dialog
        """
        if self._layout:
            self._disconnect_layout()
            self._clear_state()

    def _disconnect_layout(self):
        """Disconnects the current
        layout from the current dialog
        """
        content_area = self._dialog.get_content_area()
        content_layout = self._layout.main_component
        content_area.remove(content_layout)

    def _set_state(self, layout):
        """ sets the current layout
        @param layout: Gtk.Widget
        """
        self._layout = layout

    def _clear_state(self):
        """Clears the current state"""
        self._set_state(None)

    def _validate_layout(self):
        """validates the layout.

        @throws NameError: when layout
        is empty.
        """
        if not self._layout:
            raise NameError(self.ERROR_MSG)
        return True

    def _create_dialog_window(self):
        """ Creates the dialog window

        @return: Gtk.Dialog
        """
        dialog = generate_default_dialog()
        self._update_dialog_window(dialog)
        self._create_action_area(dialog)
        dialog.show_all()

        return dialog

    def _update_dialog_window(self, dialog):
        dialog.set_title(self._title)
        dialog.set_default_size(*self._default_size)
        dialog.set_transient_for(self._parent)

    def _create_action_area(self, dialog):
        """ Creates the area defined as the
        action area which holds the confirm
        and cancel buttons.
        """
        action_area = dialog.get_action_area()

        cancel_button = self._create_cancel_button()
        confirm_button = self._create_confirm_button()
        action_area.set_homogeneous(True)

        action_area.pack_start(confirm_button, *PACK_ARGS)
        action_area.pack_start(cancel_button, *PACK_ARGS)
        action_area.show_all()

    def _create_confirm_button(self):
        """Creates the confirm button

        @return: Gtk.Button
        """
        name = self.DEFAULT_CONFIRM_BUTTON_NAME
        func = self.confirm_button_clicked
        return generate_default_button(name, func)

    def _create_cancel_button(self):
        """Creates the cancel button

        @return: Gtk.Button
        """
        name = self.DEFAULT_CANCEL_BUTTON_NAME
        func = self.cancel_button_clicked
        return generate_default_button(name, func)

    def confirm_button_clicked(self, *args):
        """ Activated when the dialog has been
        confirmed
        """
        self._set_response(self.ACCEPT_RESPONSE)

    def cancel_button_clicked(self, *args):
        """ Activated whe the dialog has been
        cancelled
        """
        self._set_response(self.CANCEL_RESPONSE)

    def _set_response(self, response):
        """ Sets the dialogs response

        @param response: Gtk.ResponseType that
         represents the response of the dialog
        """
        self._dialog.response(response)
        self._dialog.hide()
        self._response = response

    def run_dialog(self):
        """Runs the stored dialog window.

        @raises NameError: if layout hasn't
        been set.

        @return: int representing the
        Gtk.ResponseType signal emitted
        """
        if self._validate_layout():
            self.run()

    def run(self):
        """Runs the stored dialog window.

        @return: int representing the
        Gtk.ResponseType signal emitted
        """
        if self.ACCEPT_RESPONSE is self._dialog.run():
            return self._confirmed()
        return self._cancelled()

    def _confirmed(self):
        """Gets the confirmed data stored in
        the layout.
        """
        return self._layout.confirm()

    def _cancelled(self):
        """Gets the cancelled data stored in
        the layout.
        """
        return self._layout.cancelled()