#! /usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

"""Builder module extends Gtk.Builder and implements new features.
"""
from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport

from peonordersystem import path

import json

from peonordersystem.MenuItem import MenuItem

from collections import deque

from xml.etree.cElementTree import ElementTree

class Builder(Gtk.Builder):
    """ Generates and builds the UI from XML file passed into
objects add_from_file. Generates MenuItems in the UI from
a stored JSON file.
    
@var menu_items:    dict where each key is represents the
sub-category which the MenuItem belongs to. Each value is 
a list of MenuItems each representing one MenuItem object
generated from JSON data

@var widgets: dict with a str as keys representing the 
widget's name in the XML file and object as values 
representing the current widget.

@var generated_menu_buttons: List of all buttons that are
stored on menu tabs.

@var generated_table_buttons: List of all buttons that are
stored on table box. Last index is the 'TOGO' button.
    """
    
    def __init__(self):  # @IGNORE:E1002
        """ Constructs the Builder object with empty
        class attributes
        """
        # Gtk.builder is "old style" class. "Old style" super used
        super(Builder, self).__init__()
        
        self.widgets = {}
       
        # To assist in connecting signals for given menu buttons
        self.generated_menu_buttons = []
        self.generated_table_buttons = []
        
        self.order_buttons = []
        
        # placeholder variables
        self.window = None
        self.reservation_window = None
        self.order_window = None
        
    def add_from_file(self, filename, title):  # @IGNORE:E1002
        """ Generates the GUI from the given XML file utilizing 
        builder. Sets given title, and maximizes the display window
        
        @param filename: file represents the current XML file 
        from which the initial GUI will be established
        
        @param title: str that represents the title to be 
        display by the main GUI window
        """
        # Gtk.Builder is "old style" class. "old style" super used
        super(Builder, self).add_from_file(filename)
        
        self.widgets = {}
        
        menu_file = open(path.OPTIONS_DATA, 'r')
        
        option_choices = json.load(menu_file)
        
        tree = ElementTree()
        tree.parse(filename)

        elements = tree.getiterator('object')
        
        # Populate this objects attributes
        for current_widget in elements:
            name = current_widget.attrib['id']
            
            # Gtk.Buidler defines get_object
            widget = self.get_object(name)  # IGNORE:E1101
            self.widgets[name] = widget
            
            if name == 'POS_main_window':
                self.window = widget
                self.window.connect('delete_event', Gtk.main_quit)
            
            # find order window
            if name == 'orderView':
                self.order_window = widget
            
            # find and generate table buttons
            if name == 'tablesBox':
                self._generate_table_buttons(widget)
            
            if name == 'reservationsScrollWindow':
                self.reservation_window = widget
            
            if name == ('editstarsButton' or 
                'editnoteButton' or 'edititemButton'):
                self.order_buttons.append(widget)
                
                
        # Populate menu tabs
        for each in option_choices.values():
            self._generate_menu_tabs(each)
        
        self.window.set_title(title)
        self.window.show_all()
        self.window.maximize()
        
    def _generate_table_buttons(self, tables_box, num_of_tables=10):
        """Private Method.
        Generates the table buttons and populates the current
        table button box with each button.
        
        @param tables_box: Gtk.box that represents the current
        tablesBox to have the table buttons populate
        
        @param num_of_tables: int representint the current number 
        of table buttons to generate. Populates the 
        generated_table_buttons attribute Default value of 
        10 + 1 representing 'TOGO' button
        """
        for i in range(1, num_of_tables + 1):
            button = Gtk.Button('TABLE ' + str(i))
            tables_box.pack_start(button, True, True, 2.5)
            self.generated_table_buttons.append(button)
        
        # additional TOGO button
        button = Gtk.Button('TOGO')
        tables_box.pack_start(button, True, True, 2.5)
        self.generated_table_buttons.append(button)
            
    def _generate_menu_tabs(self, option_list):
        """Private method
        Helper method for add_from_file() Generates menu tabs 
        from the 'menuNotebook', each tab has
        a number of boxes stored in it based on the 
        len(option_list). Then have each table button associated
        with the option_list placed in them.
        
        The Gtk.Notebook is pulled from the builder through
        the GUI XML file.
            
        @param option_list: list that represents which categories will be
        displayed. Two possibilies may occur here:
        
        (1)the len(option_list) = 1 and one a single box 
        is generated per tab
        
        (2)len(option_list) > 1 and len(option_list) boxes are generated
        and populated into the tab.
        """
        
        # Two possible cases for option_list:
        #
        # 1)    contains only one set of menu items, and thus
        #       doesn't require additional subsets of menu boxes.
        #
        # 2)    Contains multiple sets of menu items and thus
        #       requires additional subsets of menu boxes. 
        notebook = self.widgets['menuNotebook']
        
        # list to store button-box queues. Each index corresponds to the
        # buttonboxes for each option_list
        temp = []
        
        # Generate new page with label for Notebook
        label = Gtk.Label()
        label.set_use_markup(True)
        label.set_markup('<span size="x-large">' + option_list[0]
            + "</span>")
        
        main_box = Gtk.Box()
        main_box.set_homogeneous(True)
        notebook.append_page(main_box, tab_label=label)
        
        if len(option_list) == 1:
            # Case 1
            temp.append(generate_menu_layout(main_box))
        else:
            # Case 2
            # VBox so that the menu items can efficiently use space
            #   for subdivisions
            box = Gtk.VBox()
            main_box.add(box)
            
            # Subdivide for each option
            for menu_option in option_list:
            
                # label box
                sub_box1 = Gtk.HBox()
                sub_box1.add(Gtk.Label(menu_option))
                box.pack_start(sub_box1, False, False, 5)
                
                # button box
                sub_box2 = Gtk.HBox()
                sub_box2.set_homogeneous(True)
                box.pack_start(sub_box2, True, True, 5)
                
                # generate queues for boxes and add them to list
                temp.append(generate_menu_layout(sub_box2))
                
        self._generate_menu_buttons(temp,
            option_list, load_menu_items())
        
    def _generate_menu_buttons(self, box_list, option_list, menu_items):
        """ Helper method for generate_menu_tabs(). Generates, 
        each menu button, associates it with a given MenuItem, and
        populates the menu tabs with buttons.
        
        @param box_list: list of deque each index has a one to one
        correspondence to a key value in menu_items. Each deque holds
        a number of Gtk.Box objects to which the menu_buttons need to
        be added
        
        @param option_list: list each index represents the
        categories that have been chosen to be displayed 
        on the current menu tab by the user
        
        @param menu_items: dict each key represents a category and
        each value represents a list of MenuItem objects
        """
        for option in option_list:
            
            # obtain queue from list.
            box_queue = box_list.pop(0)
            
            # get sublist of menu items
            menu = menu_items[option]
            for item in menu:
            
                # Get current box from queue
                box = box_queue.popleft()
                
                # Generate button
                button = Gtk.Button(item.get_name())
                
                # Store MenuItem in button
                button.MenuItem = item
                box.pack_start(button, True, True, 5)
                
                # Cycle queue of boxes for evenly distributed
                #   button placement
                box_queue.append(box)
                
                # Populate this objects generated_menu_buttons
                self.generated_menu_buttons.append(button)
                
    def connect_signals(self, parent):  # @IGNORE:E1002
        """Connects the generated_menu_buttons to the parent's
        menu_button_clicked method and the generated_table_buttons
        to the table_button_clicked method
        
        @param parent:  call_back obj for methods represents the
        parent that operates higher level GUI methods
        """
        # Gtk.Builder is "old style" class. "old style" super used
        super(Builder, self).connect_signals(parent)
        
        for button in self.generated_menu_buttons:
            button.connect('clicked',
                parent.menu_button_clicked)
        
        for button in self.generated_table_buttons:
            function = parent.table_button_clicked
            label = button.get_label()
            print(label)
            print label == 'TOGO'
            if label == 'TOGO':
                print (label)
                function = parent.confirm_togo
            button.connect('clicked', function, label)
        
    def set_table(self, string):
        """Sets the current table display label to the given str
        
        @param string: str represents the string of the current
        table choice. This string is set directly to display the
        given str in its label
        """
        self.widgets['orderListLabel'].set_text(string)
    
    def set_accessible_buttons(self, menu_item):
        """Sets the menu buttons associated with editing a given
        menu_option to either be sensitive or not.
        """   
        pass


def load_menu_items():
    """Generates a dict of current MenuItem objects and returns
    the dict where keys represent categories and values are list
    of MenuItem objects that correspond to the specified categories
    
    @return: dict where each key represents a menu item category
    and each value is a list of MenuItems in that category.
    """
    # Open JSON file
    menu = open(path.MENU_DATA, 'r')
    
    # object_hook function utilized to generate MenuItems in
    #   JSON load.
    def generate_menu(curr) :
        """Returns a menu item associated with the given
        dict passed in.
        
        @param curr: dict generated from JSON file which has
        the str keys of '__MenuItem__', 'price', 'stars', 
        'confirmed', 'editable' and could have 'options' with
        values that match each.
        
        @return: new MenuItem object that represents the given
        dict.
        """
        options = None
        if '__MenuItem__' in curr:
            if 'options' in curr:
                options = curr['options']
            return MenuItem(curr['__MenuItem__'], curr['price'],
                            curr['stars'], curr['editable'],
                            curr['confirmed'], options)
        return curr
    
    
    # Generate MenuItem's from JSON file
    return json.load(menu, object_hook=generate_menu)
    
def generate_menu_layout(main_box):
    """ Generates the menu layout for any given menu box.
    
    This is a helper method called from inside of
    generate_menu_tabs. It returns a deque of boxes
    designed to hold the menu buttons
        
    Main boxes are passed into this method, which subdivides
    the main box into two equally large vertical boxes.
        
    @param - main_box(Gtk.Box) represents the box to have the
    menu buttons diplayed in
    """
    # deque is convenient for evenly distributing boxes
    box_queue = deque()
    # subdivide box
    for _ in range(2):
        box = Gtk.VBox()
        # box.set_homogeneous(True)
        box_queue.append(box)
        main_box.pack_start(box, True, True, 5)
    return box_queue
