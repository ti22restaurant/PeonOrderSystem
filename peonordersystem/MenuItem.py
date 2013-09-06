""" MenuItem object that stores information relating to a specific MenuItem.
"""

class MenuItem(object):
    """ This object stores information regarding a MenuItem.
        
        Attrbutes: 
        
            stars   :   The current stored star value of the object
            notes   :   String representing a note added to the item
            confirmed:  boolean representing if the item has been confirmed.
            This value is true for all non-kitchen items.
    """
    
    def __init__(self, name, price, stars=0, editable=True,
        confirmed=False, option_choices=None):
        self.__name = name
        self.__price = price
        self.__editable = bool(editable)
        # self.__options = self.set_options_choices(options)
        self.stars = int(stars)
        self.notes = ''
        self.options = []
        self.__option_choices = option_choices
        self.confirmed = bool(confirmed)
        
    def get_name(self):
        """return the MenuItem's name"""
        return self.__name
    
    def get_price(self):
        """return: String representing the MenuItem's price"""
        return self.__price
    
    def is_editable(self):
        """return: boolean if the MenuItem has options that
        can be edited
        """
        return len(self.__option_choices) is not 0
    
    def get_option_choices(self):
        """returns the MenuItem's options choices"""
        return self.__option_choices
    
    def has_note(self):
        """returns if the MenuItem contains a note"""
        return self.notes is not ''
    
    def has_options(self):
        """returns if the MenuItem currently has selected
        options.
        
        @return: boolean representing if options have been
        selected for the MenuItem
        """
        return len(self.options) > 0
    
    def __repr__(self):
        """returns a representation of the MenuItem for printing
            purposes
        """
        return self.__name
