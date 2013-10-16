""" This module contains the MenuItem class that stores
information about MenuItems.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from copy import copy


class MenuItem(object):
    """ This object stores information regarding a MenuItem.
    
    @var _name: private attribute. int represents the name of
    the item stored.
    
    @var _price: private attribute. float representing the
    cost of the item 
    
    @var _editable: private attribute. bool representing if
    the item is editable
    
    @var _locked: private attribute. bool representing if the
    item has been locked and shouldn't be editable.
    
    @var star: int representing the value of the items stars
    
    @var notes: str representing the notes associated with
    an item
    
    @var options: list of str representing the options 
    that have been chosen with the associated item.
    
    @var _option_choices: dict of str, float pairs where
    each key represents a potential option choice for
    the item, each value pair is the cost of said choice. 
    """
    
    def __init__(self, name, price, stars=0, editable=True,
        confirmed=False, option_choices={}):
        
        self._name = name
        self._price = price
        self._option_choices = option_choices
        self._locked = False
        self._price_scalar = 1.0
        self.comp_message = None
        
        self.editable = bool(editable)
        self.stars = int(stars)
        self.notes = ''
        self.options = []
        self.confirmed = bool(confirmed)
    
    def toggle_lock_menu_item(self):
        """Toggles if the MenuItem is locked.
        If true toggles to false, if false toggles
        true.
        """
        self._locked = not self._locked

    def is_comped(self):
        """Returns if this MenuItem object
        is comped.

        @return: bool value that represents
        if this menu item has been comped or
        not.
        """
        return self._price_scalar == 0.0 and self.comp_message

    def get_comp_message(self):
        """Gets the comp message associated
        with this item.

        @return: str representing the message
        associated with the comp. None if there
        is_comped returns false.
        """
        return self.comp_message

    def comp(self, value, message):
        """

        @param value: bool if the menu item
        should be comped, or not.

        @param message: str representing the
        message associated with this comp.
        """
        if value:
            self._price_scalar = 0.0
            self.comp_message = message
        else:
            self._price_scalar = 1.0
            self.comp_message = None

    
    def is_locked(self):
        """Returns the value of the locked attribute.
        
        @return: bool representing if the MenuItem is
        locked.
        """
        return self._locked
    
    def edit_price(self, value):
        """Sets the MenuItem's price to the given amount.
        """
        price = self._price

        for key in self.options:
            price += self._option_choices[key]

        self._price_scalar = value / price

        if self._price_scalar > 1.0:
            self._price_scalar = 1.0

    def get_name(self):
        """Gets the name of the MenuItem.
        
        @return: str representing the associated
        name of the Menuitem
        """
        return self._name
    
    def get_price(self):
        """Gets the prices associated with the
        MenuItem.
        
        @return: float representing the price.
        """
        price = self._price
        for key in self.options:
            price += self._option_choices[key]

        return self._price_scalar * price
    
    def is_editable(self):
        """Checks if the item is editable.
        
        @return: bool, True if the item is editable,
        false otherwise.
        """
        return self.editable and not self._locked
    
    def get_option_choices(self):
        """Gets a copy of the current options choices dict.
        
        @return: dict where each key is a str that represents
        an option, and each value is a float that represents
        the cost.
        """
        options_copy = copy(self._option_choices)

        for key in options_copy:
            options_copy[key] *= self._price_scalar

        return options_copy

    def has_note(self):
        """Checks if the item as a note associated with it.
        
        @return: bool, True if there is a non-empty note.
        False otherwise.
        """
        return self.notes is not ''
    
    def has_options(self):
        """Checks if the item has had options chosen for
        it.
        
        @return: boolean representing if options have been
        selected for the MenuItem
        """
        return len(self.options) > 0
    
    def __repr__(self):
        """Gets a string representation of the MenuItem.
        
        @return: str that is a representation of information
        stored in the MenuItem
        """
        return str(self.__dict__)