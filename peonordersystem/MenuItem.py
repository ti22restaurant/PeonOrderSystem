""" This module contains the MenuItem class that stores
information about MenuItems.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

class MenuItem(object):
    """ This object stores information regarding a MenuItem.
    
    @var _name: private attribute. int represents the name of
    the item stored.
    
    @var _price: private attribute. float representing the
    cost of the item 
    
    @var _editable: private attribute. bool representing if
    the item is editable
    
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
        confirmed=False, option_choices=None):
        self._name = name
        self._price = price
        self.editable = bool(editable)
        self.stars = int(stars)
        self.notes = ''
        self.options = []
        self._option_choices = option_choices
        self.confirmed = bool(confirmed)
        
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
        return self._price
    
    def is_editable(self):
        """Checks if the item is editable.
        
        @return: bool, True if the item is editable,
        false otherwise.
        """
        return self.editable
    
    def get_option_choices(self):
        """Gets the available option choices for the item
        
        @return: dict where each key is a str that represents
        an option, and each value is a float that represents
        the cost
        """
        return self._option_choices
    
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
        return self._name
    