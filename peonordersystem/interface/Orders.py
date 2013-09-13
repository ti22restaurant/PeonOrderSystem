#! /usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

"""This module contains all UI interaction for the
orders panel of the PeonOrderSystem UI. Three classes
are defined in this module. They are represented in
two subgroups

@group Orders: This group represents client side code.
This object may be interacted with after having been
instantiated and given the necessary components to function.
This object is built from the Orders_Components group and
provides all top level functionality to user.

@group Orders_Components: This group represents the 
implementation components of the Orders object. This is
where changes are made that would 
    
@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport

from peonordersystem.MenuItem import MenuItem

import time

class OrderTreeView(Gtk.TreeView):
    """OrderTreeView object that creates
    and operates basic TreeView functionality. Extends
    Gtk.TreeView
    
    @group Orders_Components: member of Orders_Components
    group. This object is utilized in the Orders object as
    an implementation component.
    """
    
    def __init__(self):  # @IGNORE:E1002
        """Initalizes a new OrderTreeView
        object. All columns are generated and added
        to the OrderTreeView object via this method.
        
        @requires: OrderTreeView object must still be
        added to the window it is displayed in. Init
        does not perform this task as it is independent
        on the parent window.
        """
        super(OrderTreeView, self).__init__()
        column_list = self._generate_columns()
        for col in column_list:
            self.append_column(col)
    
    def _generate_columns(self, wrap_width=250,
                         col_names=('Menu Items', 'Stars', 'Notes')):
        """Genertes the columns to be stored in the OrderTreeView
        object.
        
        @param wrap_width: keyword argument that represents the
        character length for the word wrap in the first column.
        By default wrap_with=250
        
        @keyword col_names: keyword argument that represents a
        3-tuple where each entry represents a column to be
        generated in the OrderTreeView. By default
        col_names=('Menu Items', 'Stars', 'Notes')
        
        @return: list where each entry represents a column
        to be added directly to the OrderTreeView for 
        display.
        """
        col_list = []
        
        rend = Gtk.CellRendererText()
        rend.set_property('wrap-width', wrap_width)
        
        # Each entry in list_store = (str, str, str, str, bool)
        # representing: 
        #
        # 0. name: str of the menu_items name
        # 1. stars: str of the menu_items stars rating
        # 2. image: str representing Gtk.STOCK_image to be used for note display
        # 3. color: str representing the hexadecimal color for the foreground
        # 4. has note: bool representing if the image should be displayed
        
        column = Gtk.TreeViewColumn(col_names[0], rend, text=0, foreground=3)
        col_list.append(column)
        
        rend = Gtk.CellRendererText()
        column2 = Gtk.TreeViewColumn(col_names[1], rend, text=1, foreground=3)
        col_list.append(column2)
        
        rend = Gtk.CellRendererPixbuf()
        column3 = Gtk.TreeViewColumn(col_names[2], rend, stock_id=2, visible=4)
        col_list.append(column3)
        
        return col_list
    
    def get_selected_iter(self):
        """Gets a Gtk.TreeIter representing the
        currently selected item in the OrderTreeView.
        
        @return: Gtk.TreeIter representing the currently
        selected item.
        """
        tree_selection = self.get_selection()
        _, itr = tree_selection.get_selected()
        return itr

class OrderStore(Gtk.TreeStore):
    """OrderStore class creates and stores
    the model to be sored in the OrderTreeView
    as well as additional menu item and order
    information.
    
    @attention: Append is the only valid method
    for adding items to the OrderStore. All other
    methods (swap, insert, prepend, ..etc) are not
    supported.
    
    @group Orders_Components: a member of the
    Orders_Components group. This class is used
    to build the functionality of the Orders class.
    
    @var order_list: list of MenuItem objects that
    is the current orders selected menu items.
    """
    
    def __init__(self):
        """Initalizes the OrderStore object. Generates
        a new OrderStore that stores a 3 str types.
        """
        # Complicated list store. Stores information to be displayed.
        #
        # 0. name: str of the menu_items name
        # 1. stars: str of the menu_items stars rating
        # 2. image: str representing Gtk.STOCK_image to be used for note display
        # 3. color: str representing the hexadecimal color for the foreground
        # 4. has note: bool representing if the image should be displayed
        
        super(OrderStore, self).__init__(str, str, str, str, bool)
        self.order_list = []
        
    def append(self, menu_item):
        """Appends the given menu_item to the
        OrderStore storing its values for display.
        
        @raise Exception: If a non-MenuItem is given
        as the menu_item parameter.
        
        @attention: This is the only valid method for
        adding MenuItems to the OrderStore. All other
        methods are not supported (swap, insert, prepend..etc)
        
        @param menu_item: MenuItem object that represents
        the current menu item to be appended to the OrderStore.
        
        @return: Gtk.TreeIter pointing to the currently added
        item.
        """
        if type(menu_item) is not MenuItem:
            raise Exception("Tried to append a non-MenuItem "
                            + "to the OrderStore." + 
                            " Type Expected: MenuItem" + 
                            " Type Received: " + 
                            str(type(menu_item)))
            
        self.order_list.append(menu_item)
        new_entry = []
        
        name = menu_item.get_name()
        stars = ''
        
        if menu_item.is_editable():
            stars = str(menu_item.stars)
            
        # 0. name: str representing menu_item name
        new_entry.append(name)
        
        # 1. stars: str representing menu_item star rating.
        new_entry.append(stars)
        
        # 2. image: str representing the image to be displayed
        # in the notes column.
        new_entry.append(Gtk.STOCK_DND)
        
        # 3. color: str representation of hexadecimal color for
        # the item to be displayed at.
        new_entry.append(self._get_color(menu_item.confirmed))
        
        # 4. display_image: bool representing if the image should
        # be displayed.
        new_entry.append(menu_item.has_note())
        
        return super(OrderStore, self).append(None, new_entry)
    
    def _get_color(self, is_confirmed):
        """Private Method.
        
        Gets the hexadecimal color associated with
        the value. 
        
        @return: str representing hexadecimal number for
        gray if True, black otherwise.
        """
        if is_confirmed:
            # Hexadecimal GRAY
            return '#999999'
        # Hexadecimal BLACK
        return '#000000'
    
    def _ensure_top_level_iter(self, tree_iter):
        """Private Method.
        Ensures that the current tree_iter is
        the top level and thus representative of
        a MenuItem.
        
        @param tree_iter: Gtk.TreeIter pointing at
        the selected item.
        
        @raise Exception: If invalid Gtk.TreeIter passed
        as argument.
        
        @return: Gtk.TreeIter pointing to the top
        level parent. If a top level parent is
        given then that is returned by this method.
        """
        if tree_iter is None or not self.iter_is_valid(tree_iter):
            raise Exception("Invalid Gtk.TreeIter " + 
                            "given as parameter." + 
                            "Given TreeIter: " + 
                            (str(type(tree_iter))))
        parent = self.iter_parent(tree_iter)
        if parent is None:
            return tree_iter
        else:
            return self._ensure_top_level_iter(parent)
    
    def get_index(self, tree_iter):
        """Gets the index of the selected MenuItem at
        tree_iter. This method only returns the value
        of the top most parent.
        
        @param tree_iter: Gtk.TreeIter pointing at the
        currently selected item.
        
        @return: int representing the selected MenuItem's
        index.
        """
        if tree_iter is None or not self.iter_is_valid(tree_iter):
            Exception("Invalid Tree Iter " + 
                      "given as parameter.")
        path = self.get_path(tree_iter)
        value = path.get_indices()
        return value[0]
    
    def get_menu_item(self, tree_iter):
        """Gets the MenuItem at tree_iter 
        
        @attention: This method returns the given
        associated MenuItem even if one of its children
        is selected.
        
        @param tree_iter: Gtk.TreeIter representing the
        selected MenuItem.
        
        @return: MenuItem object that represents the
        selected MenuItem object pointed at by tree_iter
        """
        
        # Possible Exception raised via ensure_top_level_iter
        tree_iter = self._ensure_top_level_iter(tree_iter)
        
        index = self.get_index(tree_iter)
        return self.order_list[index]
    
    def remove(self, tree_iter):
        """Removes the MenuItem at the selected
        tree_iter from the order list.
        
        @param tree_iter: Gtk.TreeIter representing
        the selected MenuItem.
        
        @return: MenuItem object representing the
        MenuItem removed from the order list.
        """
        # Potential Exception raised on ensure_top_level_iter
        tree_iter = self._ensure_top_level_iter(tree_iter)
        
        index = self.get_index(tree_iter)
        if index is not None:
            super(OrderStore, self).remove(tree_iter)
            return self.order_list.pop(index)
        return None
    
    def update_item(self, tree_iter):
        """Updates the current item to accurately
        display any changed information. Options and
        notes are added as children in the tree. Any
        previous adjustments are removed and then
        new values are retrieved.
        
        @param tree_iter: Gtk.TreeIter representing the
        selected MenuItem.
        
        @return: Gtk.TreeIter pointing to the updated
        MenuItem
        """
        
        # Potential exception raised
        tree_iter = self._ensure_top_level_iter(tree_iter)
        
        menu_item = self.get_menu_item(tree_iter)
        
        # remove pre-update information
        while self.iter_has_child(tree_iter):
            itr = self.iter_children(tree_iter)
            super(OrderStore, self).remove(itr)
        
        text_color = self._get_color(menu_item.confirmed)
        
        # add post-update information
        if menu_item.has_note():
            super(OrderStore, self).append(tree_iter,
                                           (menu_item.notes,
                                            '', None, text_color, False))
        if menu_item.has_options():
            super(OrderStore, self).append(tree_iter,
                                           (str(menu_item.options)[1:-1],
                                            '', None, text_color, False))
        self[tree_iter][1] = str(menu_item.stars)
        self[tree_iter][3] = text_color
        self[tree_iter][4] = menu_item.has_note()
        
        return tree_iter
        
    def confirm_order(self, tree_iter):
        """Sets all MenuItem's in the order to confirmed.
        """
        if tree_iter != None:
            menu_item = self.get_menu_item(tree_iter)
            if not menu_item.confirmed:
                menu_item.confirmed = True
                menu_item.editable = False
                self.update_item(tree_iter)
            self.confirm_order(self.iter_next(tree_iter))

class Orders(object):
    """Orders represents the main interactions with
    the Orders for the user. This object will add a
    TreeView to the parent window passed in. This object
    displays, and stores all information regarding MenuItems
    added to a number of tables.
    
    @group Orders: Member of the Orders group which combines
    members of the Orders_Components groups to create their
    base functionality.
    
    @var order_list: list of OrderStores where each nth entry
    represents the table at n + 1. 
    
    @var tree_view: OrderTreeView represents the OrderTreeView
    where each OrderStore is displayed.
    
    @var current_order: OrderStore object that represents the
    currently selected OrderStore.
    
    @var to_go_dict: dict that represents the to go orders 
    placed. Keys are 2-tupes represented by name and phone
    number. Values are OrderStores that represent that
    order.
    
    """
    
    def __init__(self, parent, load_data=None, num_of_tables=10):
        """Initializes and creates the Orders object.
        
        @param parent: Gtk.Container subclass from
        which the TreeView will be displayed.
        
        @keyword load_data: represents the data that the
        orders should be loaded from. This is either None
        or a 2-tuple of Dicts, where load_data[0] is
        representative of the table orders and load_data[1]
        is representative of the togo_orders.
        
        @keyword num_of_tables: represents the number
        of tables for orders to be generated for.
        
        @raise TypeError: If parent is not a subclass
        of Gtk.Container.
        """
        if not isinstance(parent, Gtk.Container):
            raise TypeError("Expected a subclass of " + 
                            "Gtk.Container. Instead got " + 
                            str(type(parent)))
        self.tree_view = OrderTreeView()
        parent.add(self.tree_view)
        
        self.order_list = []
        for _ in range(num_of_tables):
            tree_model = OrderStore()
            self.order_list.append(tree_model)
            
        self.to_go_dict = {}
        self.current_order = None
        
        if load_data is not None and type(load_data) is tuple:
            try:
                self._load_data(load_data)
            finally:
                print('Unable to load data from file')
                
    
    def _load_data(self, load_data):
        """Loads the data from the files, and
        places them in the orders.
        """
        table_orders = load_data[0]
        togo_orders = load_data[1]
        
        if type(table_orders) is not dict or type(togo_orders) is not dict:
            raise TypeError("LOADING DATA FROM FILE. " + 
                            "Expected load_data provided to orders " + 
                            "to be type(obj) = dict. Instead got a 2-tuple " + 
                            "of {}, and {}".format(type(table_orders),
                                                   type(togo_orders)))
        
        for table_num in table_orders:
            table, num = table_num.split('_')
            
            num = int(num) - 1
            
            self.current_order = self.order_list[num]
            
            load_order = table_orders[table_num]
            
            for menu_item in load_order:
                self.add(menu_item)
        
        for togo_name in togo_orders:
            name, number = togo_name.split('_')
            
            # standard Dialog generated time format.
            curr_time = time.strftime('%X, %A, %m/%y')
            
            key = (name, number, curr_time)
            
            self.select_togo_order(key)
            load_order = togo_orders[togo_name]
            
            for menu_item in load_order:
                self.add(menu_item)
        
    def get_togo_orders(self):
        """Gets a list of the current togo orders.
        
        @return: list of 3-tuples where each entry
        represents a togo order. Each 3-tuple is
        of the form (str, str, str) = (name, number, time)
        """
        return self.to_go_dict.keys()
    
    def select_togo_order(self, key):
        """Selects the given 3-tuple which represents
        a given order.
        """
        if key in self.to_go_dict:
            self.current_order = self.to_go_dict[key]
        else:
            self.current_order = OrderStore()
            self.to_go_dict[key] = self.current_order
        self._set_model()

    def _set_model(self):
        """Private Method
        
        sets the model to the current order.
        """
        self.tree_view.set_model(self.current_order)
        self.tree_view.show_all()
        
    
    def set_current_table(self, num):
        """Sets the current table and order considered
        to the given value.
        
        @param num: int value representing the selected
        table
        
        @raise IndexError: If number given is outside
        of the range of the the length of order_list.
        """
        if num not in range(len(self.order_list)):
            raise IndexError()
        self.current_order = self.order_list[num]
        self._set_model()
    
    def get_current_order(self):
        """Gets the current order.
        
        @return: list of MenuItem objects representing
        the current order list. None if no order has
        been selected.
        """
        if self.current_order != None:
            order_list = self.current_order.order_list
            return order_list
        return None
    
    def get_selected(self):
        """Gets the selected MenuItem.
        
        @return: MenuItem object representing the
        currently selected MenuItem
        """
        itr = self.tree_view.get_selected_iter()
        return self.current_order.get_menu_item(itr)
    
    def add(self, menu_item):
        """Adds the given menu_item to the
        current order.
        
        @raise TypeError: if given menu_item is
        not of type MenuItem
        
        @param menu_item: MenuItem object representing
        the menu item to be added to the current order.
        """
        if not type(menu_item) is MenuItem:
            raise TypeError('Expected MenuItem object, ' + 
                            'got ' + str(type(menu_item)))
        itr = self.current_order.append(menu_item)
    
    def remove(self):
        """Removes the currently selected
        MenuItem from the orders.
        
        @return: MenuItem object that represents
        the removed MenuItem
        """
        itr = self.tree_view.get_selected_iter()
        if self.current_order != None:
            return self.current_order.remove(itr)
    
    def update(self):
        """Updates the currently selected MenuItem
        so that it displays updated information.
        """
        itr = self.tree_view.get_selected_iter()
        self.current_order.update_item(itr)
    
    def get_order_info(self):
        """Gets the label associated with the
        current table.
        
        @return: str representing the given current
        order. Either table_n, where n is the number,
        or name_number if the order is a togo order.
        """
        if self.current_order in self.order_list:
            index = self.order_list.index(self.current_order)
            return 'table_{}'.format(index + 1)
        else:
            for keys in self.to_go_dict:
                if self.current_order == self.to_go_dict[keys]:
                    return '{}_{}'.format(keys[0], keys[1])
        
    
    def confirm_order(self):
        """Set all MenuItems in the current order to
        confirmed
        """
        tree_iter = self.current_order.get_iter_first()
        self.current_order.confirm_order(tree_iter)
