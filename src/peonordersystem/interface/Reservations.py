#! /usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

"""Reservations Module provides all basic functionality and display
for the Reservations class.

This module is subdivided into two groups:

@group Reservations_Components: This group represents implementation
classes for the Reservations group. These classes provide the underlying
functionality for the Reservations.

members:

    Reserver: Wrapped class that holds the information for any given
    reservation.
    
    ReservationTreeView: Gtk.TreeView extending class that provides the
    display for the Reservation object
    
    ReservationStore: Gtk.ListStore extending class that provides the
    data storage and basic functions to be displayed.

@group Reservations: This group represents the user interaction classes
that perform wrap the functionality from the Reservations_Components
group.

members:
    
    Reservations: Class that provides the basic functionality with
    implementation hidden from the user.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from datetime import datetime

from gi.repository import Gtk, GObject  # IGNORE:E0611 @UnresolvedImport

from src.peonordersystem.standardoperations import tree_view_changed

from src.peonordersystem.Settings import (RESERVATION_UPDATE_TIME_FRAME,
                                          RESERVATION_NOTIFICATION_TIME_MAX,
                                          RESERVATION_NOTIFICATION_TIME_MIN)

from src.peonordersystem.CustomExceptions import (NoSuchSelectionError,
                                                  InvalidReservationError)


class Reserver(object):
    """Reserver class represents a single reservation. This
    class stores information pertaining to a reservation and
    provides access and comparison methods.
    
    @group Reservations_Component: member of the 
    Reservations_Component group. As such this class
    provides the basic functionality for the Reservations
    group. Changes in this class will effect the basic
    functions of the Reservations group members.
    
    @var name: str representing the name that the reservation
    is stored under.
    
    @var number: str representing the number that is associated
    with the reservation.
    
    @var arrival_time: float representing the time 
    of the expected arrival. This is represented as the number
    of seconds since the epoch.
    
    @var _curr_time: float representing the time that the order
    was placed. This value is utilized for determining an accurate
    percentage. As such it should not be altered.
    """
    def __init__(self, name, number, arrival_time):
        """Initializes a new Reserver object.
        
        @param name: str representing the name to be
        stored for this reservation.
        
        @param number: str representing the number
        to be stored for this reservation.
        
        @param arrival_time: float representing
        the time of the arrival. Expected to be
        generated from time import.
        
        @raise ValueError: If the given time is
        in the past
        """
        self._curr_time = datetime.now()
        
        if self._curr_time > arrival_time:
            raise ValueError('Reserver expects reservation time to be '
                             'before current time.')
        
        self.name = name
        self.number = number
        self._arrival_time = arrival_time

    def get_arrival_time(self):
        """Gets the current arrival time in
        number of seconds since epoch.

        @return: datetime object that represents
        the arrival time of this reservation.
        """
        return self._arrival_time

    def get_time_until_arrival(self):
        """Gets the number of second until the
        expected reservations arrival.

        @return: timedelta that represents the
        length of time until arrival.
        """
        curr_time = datetime.now()
        return self._arrival_time - curr_time
    
    def get_arrival_time_str(self):
        """Gets the current arrival time in str
        form. 
        
        @return: str representing the current
        times "Hours:Mins, weekday, mth/yr' as
        the format.
        """
        return self._arrival_time.ctime()
        
    def get_eta(self):
        """Gets the expected time of arrival as a number
        representing the percentage away from the current
        time.
        
        @return: float representing the percentage value as
        the distance from the arrival. 0.0 for far distance,
        100.0 for right now or already occurred.
        """
        arrival_time = self._arrival_time
        curr_time = datetime.now()
        
        if arrival_time >= curr_time:
            return (((curr_time - self._curr_time).total_seconds()) /
                    ((arrival_time - self._curr_time).total_seconds())) * 100
        return 100.0
    
    def __cmp__(self, other):
        """Comparison function that is used for
        comparing two Reserver objects to eachother.
        The comparison is made solely on their arrival
        times.
        
        @param other: Reserver object that is being
        compared to this one.
        
        @return: int representing the total number
        of seconds between the two orders.
        """
        return (self._arrival_time - other._arrival_time).total_seconds()
    
    def __repr__(self):
        return str(self.__dict__)


class ReservationTreeView(Gtk.TreeView):
    """ReservationTreeView class provides the basic
    functionality for the TreeView to be displayed.
    
    @group Reservations_Component: member of the 
    Reservations_Component group. As such this class
    provides the basic functionality for the Reservations
    group. Changes in this class will effect the basic
    functions of the Reservations group members.
    """
    
    def __init__(self):
        """Initializes the ReservationTreeView object.
        """
        super(ReservationTreeView, self).__init__()

        selection = self.get_selection()
        selection.connect('changed', tree_view_changed, self)

        col_list = self.generate_columns()
        
        for col in col_list:
            self.append_column(col)

    def select_iter(self, itr):
        """Selects the given iter displayed
        in the tree view.

        @param itr: Gtk.TreeIter representing
        an iter pointing to a row in the displayed
        view.

        @return: None
        """
        selection = self.get_selection()
        selection.select_iter(itr)
    
    def generate_columns(self, col_names=['Name', 'Number',
        'ArrivalTime', 'Estimated Arrival']):
        """Generates the columns for the display. At default
        names for each column are obtained from keyword.
        
        @keyword col_names: list of str that represents the names 
        of the generated columns. DEFAULT = ['Name', 'Number', 
        'ArrivalTime', 'Estimated Arrival']
        
        @return: list of Gtk.TreeViewColumns representing the
        columns to be added.
        """
        col_list = []
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(col_names[0], rend, text=0)
        col_list.append(col)
        
        col = Gtk.TreeViewColumn(col_names[1], rend, text=1)
        col_list.append(col)
        
        col = Gtk.TreeViewColumn(col_names[2], rend, text=2)
        col_list.append(col)
        
        rend = Gtk.CellRendererProgress()
        col = Gtk.TreeViewColumn(col_names[3], rend, value=3)
        col_list.append(col)
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('', rend)
        col_list.append(col)
        
        return col_list
    
    def get_selected_iter(self):
        """Gets the iter representing the currently
        selected item.
        
        @return: Gtk.TreeIter representing the currently
        selected item.
        """
        tree_selection = self.get_selection()
        model, itr = tree_selection.get_selected()
        return itr
    

class ReservationStore(Gtk.ListStore):
    """ReservationStore class controls the creation
    and insertion of data and values into the model
    that will be displayed in pair with the Reservation
    TreeView.
    
    @group Reservations_Component: member of the 
    Reservations_Component group. As such this class
    provides the basic functionality for the Reservations
    group. Changes in this class will effect the basic
    functions of the Reservations group members.
    
    @var _reservation_list: list of Reserver objects that
    is representative of the information displayed. This
    list is sorted, and changes in it will have unintended
    consequences.
    
    @var _timeout_id: GObject id that runs every 10 minutes
    to update the displayed ETA. 
    """
    
    def __init__(self):
        """Initializes the ReservationStore
        object and generates the timeout_id.
        """
        super(ReservationStore, self).__init__(str, str, str, float)
        self._reservation_list = []
        self._reservation_notifications = []
        self._timeout_id = GObject.timeout_add(RESERVATION_UPDATE_TIME_FRAME,
                                               self._on_timeout, None)
    
    def add_reservation(self, reserver):
        """Adds the given information as a new Reserver
        on model to be displayed.
        
        @param name: str representing the name to be
        stored in the Reserver object
        
        @param number: str representing the number to
        be stored in the REserver object
        
        @param arrival_time: float representing time value
        generated from time.time
        
        @return: tuple of Gtk.TreeIter pointing to the row,
        and Reserver containing the data that is pointed
        to.
        """
        # find insertion
        index = self._insertion_index(reserver, self._reservation_list)

        self._reservation_list.insert(index, reserver)
        values = (reserver.name, reserver.number,
                  reserver.get_arrival_time_str(),
                  reserver.get_eta())
            
        itr = self.insert(index, row=values)
        
        return itr, reserver
    
    def _insertion_index(self, other, curr_list):
        """Private Method.
        Performs a search on the given list to find
        the index that the given value should be placed.
        
        @param other: Reserver object that is to be placed
        in the list.
        
        @param curr_list: list of Reserver objects that is
        to have the other placed into it.
        
        @return: int representing the index that the value
        should be inserted at.
        """
        if len(curr_list) > 0:
            start = curr_list[0].__cmp__(other)
            end = curr_list[-1].__cmp__(other)
            if start > 0 or end <= 0:
                if end <= 0:
                    return len(curr_list) + 1
                    
            else:
                new_length = len(curr_list) / 2
                middle = curr_list[new_length].__cmp__(other)
                
                if middle > 0:
                    return self._insertion_index(other, curr_list[1:new_length]) + 1
                else:
                    new_list = curr_list[new_length:-1 - 2]
                    return self._insertion_index(other, new_list) + new_length + 1
        return 0
    
    def _get_index(self, itr):
        """Gets the index of the given
        iter.
        
        @param itr: Gtk.TreeIter object that
        represents a valid iter.
        
        @return: int representing the index of
        the entry selected by the given iter
        """
        path = self.get_path(itr)
        path = path.get_indices()
        return path[0]
    
    def get_selected_reservation(self, itr):
        """Gets the selected Reserver object
        assocaited with the iter.
        
        @param itr: Gtk.TreeIter representing
        the Reserver object that was selected.
        
        @return: Reserver object linked to the
        model.
        """
        index = self._get_index(itr)
        return self._reservation_list[index]
    
    def remove_selected(self, itr):
        """Removes the Reserver object
        from the model that is represented
        by the value pointed to by the given
        iter.
        
        @param itr: Gtk.TreeIter that represents
        the selected Reserver object.
        
        @return: Reserver object that was removed
        from the model
        """
        index = self._get_index(itr)
        self.remove(itr)
        reserver = self._reservation_list.pop(index)

        if reserver in self._reservation_notifications:
            self._reservation_notifications.remove(reserver)

        return reserver

    def get_reservation_notifications(self):
        """Gets the stored reservation notifications.

        @return: list of Reserver objects that represents
        the reservations that are incoming within the
        time frame.
        """
        return self._reservation_notifications

    def clear_reservation_notifications(self):
        """Clears the currently stored reservation
        notifications.

        @return: None
        """
        self._reservation_notifications = []
    
    def _on_timeout(self, *args):
        """Callback method that is performed
        on the given interval by the _timeout_id.
        
        @param *args: Wildcard parameter used as a
        catchall.
        
        @return bool that lets the _timeout_id know
        if the process should continue. 
        """
        for row, reserver in zip(self, self._reservation_list):
            row[3] = reserver.get_eta()

            until_reservation = reserver.get_time_until_arrival()

            if (until_reservation <= RESERVATION_NOTIFICATION_TIME_MAX) and \
               (until_reservation > RESERVATION_NOTIFICATION_TIME_MIN) and \
               (reserver not in self._reservation_notifications):

                self._reservation_notifications.append(reserver)

        return True

    def _dump(self):
        """Dumps the information stored in this
        object. This is mainly used for debugging
        purposes.

        @return: 2-tuple where the first index
        is a list of the Reserver objects that
        are stored, and the second index is
        a list of tuples, that represent the
        rows that were being displayed.
        """
        reserver_dump = self._reservation_list
        reserver_info = []

        for row in self:
            reserver_info.append(tuple(row))

        return reserver_dump, reserver_info
    
    def __repr__(self):
        """Gets a string representation of the
        reservations stored in this object.
        
        @return: str representation of a list
        of reservations as 3-tuples
        """
        return str(self._reservation_list)


class Reservations(object):
    """Reservations class generates and
    performs the functionality of displaying
    and maintaining the reservations list windows.
    
    @group Reservations: member of the Reservations
    group. This group relies on the Reservations_Components
    group for its functionality.
    
    @var tree_view: ReservationTreeView object that
    represents the display.
    
    @var model: ReservationStore object that represents
    the model to store the data.
    """
    def __init__(self, parent, reservation_data):
        """Intializes a new Reservations object that
        displays and controls data.
        
        @param parent: subclass of Gtk.widget. Used
        to display the stored information.
        """
        self.tree_view = ReservationTreeView()
        self.model = ReservationStore()
        parent.add(self.tree_view)
        
        self.tree_view.set_model(self.model)
        self.tree_view.show_all()

        for reserver in reservation_data:
            self.model.add_reservation(reserver)

    def _get_selected_iter(self):
        """Private Method.

        Gets the Gtk.TreeIter associated with
        the selected reservation.

        @raise NoSuchSelectionError: If no selection
        has been made.

        @return: Gtk.TreeIter pointing to the reservation
        selected.
        """
        itr = self.tree_view.get_selected_iter()

        if not itr:
            message = 'Expected Gtk.TreeIter from ' +\
                      'selection. Got {} instead'.format(type(itr))

            raise NoSuchSelectionError(message)

        return itr
    
    def add_reservation(self, name, number, arrival_time):
        """Adds a reservation to the display and keeps
        track of the reservation.
        
        @param name: str representing the reservations stored
        name.
        
        @param number: str representing the reservations stored
        number.
        
        @param arrival_time: float representing the expected
        arrival time of this reservation. This is expected to
        be generated from the time.time function.

        @return: 3-tuple of str type that represent the
        added name, number, and arrival time respectively
        """
        reserver = Reserver(name, number, arrival_time)

        itr, _ = self.model.add_reservation(reserver)
        self.tree_view.select_iter(itr)

        return reserver

    def get_reservation_notifications(self):
        """Gets a list representing the current
        reservation notifications.

        @return: list of tuple where each entry
        represents an upcoming reservation within
        the time frame. Each tuple is of type str
        representing the (name, number, time)
        of the expected arrival, respectively.
        """
        notifications = []
        reservation_notifications = self.model.get_reservation_notifications()

        for reserver in reservation_notifications:

            name = reserver.name
            number = reserver.number
            arrival_time = reserver.get_arrival_time_str()

            data = name, number, arrival_time

            notifications.append(data)

        return notifications

    def clear_reservation_notifications(self):
        """Clears the reservation notifications
        list of all current notifications.

        @return: None
        """
        return self.model.clear_reservation_notifications()

    def remove_selected_reservation(self):
        """Removes the selected reservation.
        """
        itr = self._get_selected_iter()
        reserver = self.model.remove_selected(itr)
        return reserver
    
    def __repr__(self):
        """Gets a string representation of the
        state stored in this object.
        
        @return: str representing the classes
        __dict__
        """
        return str(self.__dict__)

    def _dump(self):
        """Dumps the information associated
        with this object. This is used for
        debugging purposes mainly.

        @return: 2-tuple representing the
        reservation objects, and reservation
        information displayed respectively.
        """
        return self.model._dump()
