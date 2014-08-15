"""This module encapsulates the base functionality
for creating new widgets

@author: Carl McGraw
@email: cjmcgraw@u.washington.edu
@version: 1.1
"""

from gi.repository import Gtk

PACK_ARGS = (True, True, 5.0)

ACCEPT_RESPONSE = Gtk.ResponseType.ACCEPT
CANCEL_RESPONSE = Gtk.ResponseType.CANCEL

DEFAULT_BUTTON_ACTION_TYPES = ["clicked"]


def generate_default_button(name, f, size_request=(100, 50)):
    """Generates a generic button

    @param name: str representing the
    name for this button

    @param f: func representing the
    function that is called on clicked.

    @param size_request: tuple represent
    the size of the button

    @return: Gtk.Button
    """
    result = Gtk.Button(name)
    result.can_have_focus(True)
    result.set_size_request(*size_request)

    for action_type in DEFAULT_BUTTON_ACTION_TYPES:
        result.connect(action_type, f)
    return result


def generate_default_dialog():
    """Generates a default dialog window.

    @param title: str representing the
    title of this dialog

    @param default_size: tuple representing
    the size of the dialog.

    @return: Gtk.Dialog
    """
    result = Gtk.Dialog()
    result.set_modal(True)


def generate_hbox():
    """Generates a default horizontal
    box.

    @return: Gtk.HBox
    """
    return Gtk.HBox()


def generate_vbox():
    """Generates a default vertical
    box.

    @return: Gtk.VBox
    """
    return Gtk.VBox()
