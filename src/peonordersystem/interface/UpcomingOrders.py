'''
This module contains classes that control and display
the upcoming orders that have been confirmed for the
user.

@group UpcomingOrders: Main object that provides the 
functionality for the user. Implementation details are
hidden behind components. This should be the only object
interacted with by the user in this module.

@group UpcomingOrdersComponents: Component objects that
provide the implementation details for the UpcomingOrders
group.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
'''

from gi.repository import Gtk

import time

from src.peonordersystem import ErrorLogger
from src.peonordersystem.standardoperations import tree_view_changed
from src.peonordersystem.ConfirmationSystem import TOGO_SEPARATOR
from src.peonordersystem.CustomExceptions import NoSuchSelectionError


class UpcomingOrdersView(Gtk.TreeView):
    """UpcomingOrdersView provides the basic
    Gtk.TreeView that display the information on
    an upcoming order
    
    @group UpcomingOrdersComponent: This class is a component
    class of the UpcomingOrders group. As such any changes
    in this class with alter the functionality of any class
    participating in the UpcomingOrders group
    """
    
    def __init__(self):
        """Initializes the UpcomingOrdersView
        object.
        """
        super(UpcomingOrdersView, self).__init__()

        selection = self.get_selection()
        selection.connect('changed', tree_view_changed, self)

        for column in self.generate_columns():
            self.append_column(column)

    def select_iter(self, itr):
        """Selects the given iter displayed
        in the tree_view.

        @param itr: Gtk.TreeIter pointing
        to a row in the tree view.

        @return: None
        """
        selection = self.get_selection()
        selection.select_iter(itr)
    
    def generate_columns(self, column_names=['Order Name',
                            'Order Confirmed At',
                            'Incoming Priorty']):
        """Generates the columns for the View. By default generates
        two columns 'Order Name', and 'Order Confirmed At' and
        expects type str for all.
        
        @keyword column_names: List of str representing the
        names to be displayed in the view. By default the
        list is ['Order Name', 'Order Confirmed',
        'has priorty order']
        
        @return: list of Gtk.TreeViewColumns representing
        the columns to be added to the view
        """
        col_list = []
        
        # ListStore will store (str, str, str, bool) representing
        # the name, and confirmation time, image used for the priorty display
        # and if the order has a priority item attached to it.
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(column_names[0],
                                 rend, text=0)
        col_list.append(col)
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(column_names[1],
                                 rend, text=1)
        col_list.append(col)
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(column_names[2],
                                 rend, text=2)
        col_list.append(col)
        
        return col_list
    
    def get_selected_iter(self):
        """Gets a Gtk.TreeIter represent the currently
        selected item in the UpcomingOrdersView.

        @return: Gtk.TreeIter representing the currently
        selected order.
        """
        tree_selection = self.get_selection()
        _, itr = tree_selection.get_selected()
        return itr


class UpcomingOrderStore(Gtk.ListStore):
    """UpcomingOrderStore class creates and stores
    the model to be displayed in the UpcomingOrdersView
    class.
    
    @group UpcomingOrdersComponent: This class is a component
    class of the UpcomingOrders group. As such any changes
    in this class with alter the functionality of any class
    participating in the UpcomingOrders group
    """
    
    def __init__(self):
        """Initializes the UpcomingOrderStore object.
        Generates a new UpcomingOrderStore that stores
        3 str types.
        """
        super(UpcomingOrderStore, self).__init__(str, str, str)

    def remove(self, itr):
        """Removes the selected item from
        the UpcomingOrderStore

        @param itr: Gtk.TreeIter pointing to
        the item to be removed.

        @return: str representing the name of
        the UpcomingOrder removed.
        """
        name = self[itr][0]
        super(UpcomingOrderStore, self).remove(itr)
        return name

    def append(self, order_name, priority_info, curr_time=None):
        """Appends the given order_name, and current_order
        to the UpcomingOrderStore.
        
        @param order_name: str representing the given name
        of the order that is being confirmed.

        @param priority_info: str representing the current
        list of selected MenuItems that represent the
        priority order associated with this order. None if
        there were no items.

        @keyword curr_time: time.struct_time object that
        represents the time to be displayed in lieu of
        the current time.
        
        @return: Gtk.TreeIter pointing at the added item
        """
        if not curr_time:
            display_time = time.asctime()
        else:
            display_time = time.asctime(curr_time)
        
        order_name = order_name.replace('_', ' ')
        order = (order_name, display_time, priority_info)
        
        return super(UpcomingOrderStore, self).append(order)

    def remove_by_name(self, order_name):
        """Searches for and removes the given
        order from the UpcomingOrderStore, if the
        order_name matches one stored in the Store.
        
        @param order_name: str representing the
        orders displayed name. All underscores will
        be replaced with whitespace.
        """
        order_name = order_name.replace('_', ' ')

        index = 0

        while index < len(self):
            value = self[index]

            if value[0] == order_name:
                itr = value.iter
                self.remove(itr)

            else:
                index += 1

    def update_priority(self, itr):
        """Updates the priority of the given
        item stored at itr.
        
        @param itr: Gtk.TreeIter pointing to the
        object to be updated.

        @return: str representing the name of the
        priority order confirmed.
        """
        self[itr][2] = ''

        return self[itr][0]

    def _dump(self):
        """Gets the information associated
        with this object in its entirety. This
        is used mainly for debugging purposes

        @return: list that represents the rows
        that are stored in this object.
        """
        info = []

        for row in self:
            info.append(tuple(row))

        return info


@ErrorLogger.error_logging
class UpcomingOrders(object):
    """UpcomingOrders class provides the component
    functionality. This object displays, stores, and
    adjusts UpcomingOrders.
    
    @group UpcomingOrders: This class is a main component
    of the UpcomingOrders group that has its functionality
    provided from the UpcomingOrdersComponents group.
    
    @var tree_view: UpcomingOrdersView that displays the stored
    information
    
    @var model: UpcomingOrderStore that stores the information to
    be displayed.
    
    """
    
    def __init__(self, parent, load_data=None):
        """Initializes UpcomingOrders object.
        
        @param parent: Gtk.Container subclass that will be holding the
        generated treeview.
        
        @param load_data: 2-tuple of dicts that represents the given
        saved orders. First entry is table orders, second entry is
        togo orders.
        """
        self.tree_view = UpcomingOrdersView()
        parent.add(self.tree_view)
        self.model = UpcomingOrderStore()
        
        self.tree_view.set_model(self.model)
        
        parent.show_all()
        
        if load_data != None:
            self._load_data(load_data)
    
    def _load_data(self, load_data):
        """Private Method.

        Loads the data from a previous
        session.
        
        @param load_data: 2-tuple of dicts.
        Where each dict has a key that represents
        the orders name and a value that is a list
        of MenuItems. The first entry is the dict
        of the table orders, the second entry is
        the dict of the misc orders
        """
        for order in load_data:
            for order_name, order_time in order:

                order_data = order[order_name, order_time]
                self.add_order(order_name, order_data, curr_time=order_time)

    def _get_selected_iter(self):
        """Private method.

        Gets the currently selected order.

        @raise InvalidOrderError: if no
        item was selected.

        @return: Gtk.TreeIter pointing to
        the currently selected order
        """
        itr = self.tree_view.get_selected_iter()

        if not itr:
            message = 'Expected value for itr as selection.'+ \
                      ' Instead got {}.'.format(type(itr))
            raise NoSuchSelectionError(message)

        return itr

    def add_order(self, order_name, current_order, priority_order=[],
                  curr_time=None):
        """Adds the given order to the UpcomingOrders
        display and stores it under the given order_name
        
        @param order_name: str that will be used as the display
        name for the given order. Any underscore characters will
        be replaced with whitespace.
        
        @param current_order: list of MenuItem objects that
        is the current order list being confirmed

        @keyword priority_order: list of MenuItem objects that
        represent the priority order associated with the
        current order. By default this value is an empty list.

        @keyword curr_time: time.struct_time object that represents
        the time that the order should be displayed as having been
        confirmed at. Default None
        """
        order_name = order_name.replace(TOGO_SEPARATOR, ' ')

        priority_info = [menu_item.get_name() for menu_item in priority_order]

        itr = self.model.append(order_name, str(priority_info)[1:-1], curr_time)
        self.tree_view.select_iter(itr)
    
    def remove_selected_order(self):
        """Removes the selected order from the
        UpcomingOrders.
        """
        itr = self._get_selected_iter()
        name = self.model.remove(itr)
        return name
    
    def remove_by_name(self, order_name):
        """Removes the name that is displayed by
        order_name

        @param order_name: str representing the
        order to be removed.

        @return: str representing the name of the
        order removed.
        """
        order_name = order_name.replace(TOGO_SEPARATOR, ' ')
        self.model.remove_by_name(order_name)
        return order_name
    
    def confirm_priority(self):
        """Confirms the priority flag on the selected
        order.

        @return: str representing the name of the
        priority order confirmed.
        """
        itr = self._get_selected_iter()
        return self.model.update_priority(itr)

    def _dump(self):
        """Gets the information relating
        to this object. This is used mainly
        for debugging purposes.

        @return: list of tuples that represents
        the rows stored and displayed by this
        object.
        """
        return self.model._dump()

