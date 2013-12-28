"""Standard operations module provides functions that are standardized
across modules. These functions do not refer specifically to information
and as such may be utilized anywhere.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import os
import sqlite3
import datetime

def tree_view_changed(selection, tree_view, *args):
    """Callback Function

    This function is designed to be utilized
    for objects that are expanding and are contained
    within a scrolled window, with the scrolled
    window as the parent.

    Standard usage of this function is to provide
    a callback when a Gtk.Selection associated with
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


#====================================================================================
# This block represents utility functions that are utilized for checking and
# raising errors with reference only to external libraries.
#====================================================================================
def check_datetime(date_time):
    """Checks that the given object is
    a subclass or instance of the datetime
    object.

    @raise ValueError: If not subclass or
    instance or datetime object.

    @param date_time: object to be tested.

    @return: bool value representing if the
    test was passed or not.
    """
    if (not date_time) or (not isinstance(date_time, datetime.datetime)):
        cls_type = str(datetime.datetime)
        curr_type = str(type(date_time))
        raise ValueError('Invalid datetime supplied. Expected ' + cls_type +
                         ' got ' + curr_type + ' instead.')
    return True


def check_date(date):
    """Checks that the given object is a subclass
    or instance of the date object.

    @raise ValueError: If not subclass or instance
    of date object

    @param date_time: object to be tested.

    @return: bool value representing if the
    test was passed or not
    """
    if (not date) or (not isinstance(date, datetime.date)):
        cls_type = str(datetime.date)
        curr_type = str(type(date))
        raise ValueError('Invalid date supplied. Expected ' + cls_type +
                         ' got ' + curr_type + ' instead.')
    return True


def check_directory(curr_dir):
    """Checks that the given directory exists
    and is valid.

    @param curr_dir: str representing the directory
    to be checked.

    @return: bool value representing if the
    test was passed or not.
    """
    if (not curr_dir) or (not os.path.exists(curr_dir)):
        raise ValueError('Invalid directory supplied. Expected '
                         'a directory that exists. Got ' + str(curr_dir) +
                         " which doesn't exist or is None.")
    return True


def check_database(db):
    """Checks that the given database exists
    and is a valid sqlite3.connection object

    @param db: object that is to be tested.

    @return: bool value representing if the
    test was passed or not.
    """
    if (not db) or (not isinstance(db, sqlite3.Connection)):
        cls_type = str(sqlite3.connect)
        curr_type = str(type(db))
        raise ValueError('Invalid database supplied. Expected '
                         'a ' + cls_type + ' got ' + curr_type +
                         ' instead.')
    return True
