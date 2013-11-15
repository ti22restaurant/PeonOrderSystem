"""Standard operations module provides functions that are standardized
across modules. These functions do not refer specifically to information
and as such may be utilized anywhere.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""


def tree_view_changed(selection, tree_view, *args):
    """Callback Function

    This function is designed to be utilized
    for objects that are expanding and are contained
    within a scrolled window, with the scrolled
    window as the parent.

    Standard usage of this function is to provide
    a callback when a Gtk.Selection assocaited with
    a tree view has been changed.

    @param selection: Gtk.Selection representing
    the selection that called this method when
    an item was selected.

    @param tree_view: Gtk.TreeView representing
    the associated tree view that the selection
    was made on.

    @return: None
    """
    model, itr = selection.get_selected()

    if itr:
        path = model.get_path(itr)
        tree_view.scroll_to_cell(path)