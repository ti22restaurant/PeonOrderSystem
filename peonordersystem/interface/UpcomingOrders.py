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
        for column in self.generate_columns():
            self.append_column(column)
    
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
        
        # ListStore will store (str, str, str) representing
        # the name, and confirmation time, and if the order
        # has a priority item attached to it.
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(column_names[0],
                                 rend, text=0)
        col_list.append(col)
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(column_names[1],
                                 rend, text=1)
        col_list.append(col)
        
        rend = Gtk.CellRendererPixbuf()
        col = Gtk.TreeViewColumn(column_names[2],
                                 rend, stock_id=2)
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
    
    def append(self, order_name, current_order):
        """Appends the given order_name, and current_order
        to the UpcomingOrderStore.
        
        @param order_name: str representing the given name
        of the order that is being confirmed.
        
        @param current_order: list of MenuItem objects that
        represents the current order being confirmed.
        
        @return: Gtk.TreeIter pointing at the added item
        """
        priority_icon = self._get_icon(current_order)
        curr_time = time.asctime()
        
        order_name = order_name.replace('_', ' ')
        
        order = (order_name, curr_time, priority_icon)
        
        return super(UpcomingOrderStore, self).append(row=order)
        
    
    def _order_has_priority(self, current_order):
        """Private Method.
        
        Checks if the given order list has any
        menu items that are of priority.
        
        @param current_order: list of MenuItem objects
        
        @return: bool True if the given order list has
        a MenuItem that has priority. False otherwise.
        """
        priority = False
        
        for menu_item in current_order:
            # TODO check if MenuItem has priorty
            pass
        
        return priority
    
    def remove_by_name(self, order_name):
        """Searches for and removes the given
        order from the UpcomingOrderStore, if the
        order_name matches one stored in the Store.
        
        @param order_name: str representing the
        orders displayed name. All underscores will
        be replaced with whitespace.
        """
        order_name = order_name.replace('_', ' ')
        itr = self.get_iter_first()
        
        if self.iter_is_valid(itr):
            itr = self._search_for_order(order_name, itr)
        
        if itr != None:
            self.remove(itr)
        
    
    def update_priority(self, itr):
        self[itr][2] = Gtk.STOCK_NO
    
    def _search_for_order(self, order_name, itr):
        """Private Method.
        
        Searches the given itr by calling the next on
        this store.
        
        @param order_name: str representing the displayed
        order_name. This object should have all underscores
        replaced with whitespace
        
        @param itr: Gtk.TreeIter that represents the given
        itr to search from.
        
        @return: Gtk.TreeIter pointing to the given value,
        or None if the value didn't exist in the Store.
        """
        if itr != None:
            curr_name = self.get_value(itr, 0)
            
            if curr_name == order_name:
                return itr
            else:
                itr = self.iter_next(itr)
                return self._search_for_order(order_name, itr)
        
        return None
    
    def _get_icon(self, current_order):
        """Private Method.
        
        Gets the icon associated with the given
        order list.
        
        @param current_order: list of MenuItem objects
        
        @return: str representing the Gtk.STOCK item that
        was associated with the given order_list.
        """
        if self._order_has_priority(current_order):
            return Gtk.STOCK_YES
        return Gtk.STOCK_NO

class UpcomingOrders(object):
    """UpcomingOrders class provides the component
    functionality. This object displays, stores, and
    adjusts UpcomingOrders.
    
    @group UpcomingOrders: This class is a main component
    of the UpcomingOrders group that has its functionality
    provided from the UpcomingOrdersComponents group.
    """
    
    def __init__(self, parent):
        """Initializes UpcomingOrders object.
        """
        self.tree_view = UpcomingOrdersView()
        parent.add(self.tree_view)
        self.model = UpcomingOrderStore()
        
        self.tree_view.set_model(self.model)
        
        parent.show_all()
    
    def add_order(self, order_name, current_order):
        """Adds the given order to the UpcomingOrders
        display and stores it under the given order_name
        
        @param order_name: str that will be used as the display
        name for the given order. Any underscore characters will
        be replaced with whitespace.
        
        @param current_order: list of MenuItem objects that
        is the current order list being confirmed
        """
        self.model.append(order_name, current_order)
    
    def remove_selected_order(self):
        """Removes the selected order from the
        UpcomingOrders.
        """
        itr = self.tree_view.get_selected_iter()
        self.model.remove(itr)
    
    def remove_by_name(self, order_name):
        """Removes the name that is displayed by
        order_name 
        """
        self.model.remove_by_name(order_name)
    
    def confirm_priority(self):
        itr = self.tree_view.get_selected_iter()
        self.model.update_priority(itr)
