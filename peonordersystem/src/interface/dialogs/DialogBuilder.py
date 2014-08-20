"""This module encapsulates the base functionality
for creating new widgets

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.1
"""

from gi.repository import Gtk

PACK_ARGS = (True, True, 5.0)

PRIMARY_SELECTION_SIGNAL = 6000

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
    result.set_can_focus(True)
    result.set_size_request(*size_request)

    for action_type in DEFAULT_BUTTON_ACTION_TYPES:
        result.connect(action_type, f)
    result.show_all()
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
    result.show_all()
    return result


def generate_treeview():
    """Generates a treeview

    @return: Gtk.TreeView
    """
    view = Gtk.TreeView()
    view.show_all()
    return view


def generate_liststore(*types):
    """Generates a liststore of
    the given types

    @param types: list of types
    representing the types that
    the list store should expect.

    @return: Gtk.ListStore
    """
    return Gtk.ListStore(*types)


def generate_text_columns(titles):
    """Generates a list of text columns
    that match expected data at each index
    with the given title.

    @param titles: list of str

    @return: list of Gtk.TreeViewColumn
    objects that have been generated.
    """
    cols = []

    index = 0
    for title in titles:
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(title, rend, text=index)
        cols.append(col)
        index += 1

    return cols


def generate_scrolled_window():
    """Generates a scrolled window

    @return: Gtk.ScrolledWindow
    """
    window = Gtk.ScrolledWindow()
    window.show_all()
    return window


def generate_hbox():
    """Generates a default horizontal
    box.

    @return: Gtk.HBox
    """
    box = Gtk.HBox()
    box.show_all()
    return box


def generate_vbox():
    """Generates a default vertical
    box.

    @return: Gtk.VBox
    """
    box = Gtk.VBox()
    box.show_all()
    return box
