""" This module contains the MenuItem class that stores
information about MenuItems.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from copy import deepcopy as copy


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
                 confirmed=False, option_choices=[]):

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

        for option in self.options:
            price += option.get_price()

        self._price_scalar = value / price

        if self._price_scalar > 1.0:
            self._price_scalar = 1.0

    def get_name(self):
        """Gets the name of the MenuItem.
        
        @return: str representing the associated
        name of the MenuItem
        """
        return self._name
    
    def get_price(self):
        """Gets the prices associated with the
        MenuItem.
        
        @return: float representing the price.
        """
        price = self._price
        for option in self.options:
            price += option.get_price()

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

        for option in options_copy:
            if option._price_scalar is not 0.0:
                option._price_scalar = self._price_scalar

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

    def __eq__(self, other):
        """Gets a bool representation of whether
        this MenuItem is equal to another MenuItem
        given

        @param other: MenuItem object that is to
        be checked if equal.

        @return: bool value representing True if
        the two items are considered equal, false
        otherwise.
        """
        share_name = self._name is other._name
        share_price = self._price is other._price
        share_options = (self.options == other.options)
        share_option_choices = (self.get_option_choices() == other.get_option_choices())
        share_notes = self.notes is other.notes
        share_stars = self.stars is other.stars
        share_locked = self._locked is other._locked
        share_editable = self.editable is other.editable
        share_confirmed = self.confirmed is other.confirmed

        equality_value = (share_name and share_price and share_options
                          and share_option_choices and share_notes and share_stars
                          and share_locked and share_editable and share_confirmed)

        return equality_value


class OptionItem(object):
    """OptionItem stores information about
    an option.

    @var _name: private field. str representing
    the name associated with this option.

    @var _price: private field. double representing
    the price associated with this option.

    @var _price_scalar: private field. double representing
    the multiplicative price associated with this item. This
    field is used to adjust dependent on the relation value.

    @var _relation: str representing "ADD" if the relation is
    additive and thus when options are combined with MenuItems,
    "NO" if the relation is removal and thus signifies the removal
    the this option from a MenuItem, or "SUB" and thus signifies a
    substitution made on this MenuItem

    """
    def __init__(self, name, price):
        """Initializes a new OptionItem
        object.

        @param name: str representing
        the name associated with this
        option

        @param price: float representing
        the cost associated with this option
        """
        self._name = name
        self._price = price
        self._price_scalar = 1.0
        self._relation = None

    def get_name(self):
        """Gets the name associated
        with this option.

        @return: str representing
        the name associated with
        this option.
        """
        return self._name

    def get_price(self):
        """Gets the price associated
        with this option.

        @return: double representing
        the price associated with this
        option.
        """
        return self._price * self._price_scalar

    def set_option_relation(self, relationship):
        """Sets the relation of this option.
        This relation effects how this option
        will act with other options or MenuItem
        objects.

        Three possible conditions exist:

            ADD: relation > 0
            NO: relation = 0
            SUB: relation < 0

        @param relationship: int representing the
        relationship the option will hold to
        MenuItems and other options. Positive
        will cause the relationship to be additive,
        Zero will cause the relationship to be void
        and the option should be considered removed,
        negative will cause the relationship to be
        a substitution.

        @return: str representing the associated
        relationship. "ADD", "NO", or "SUB"
        respectively
        """
        relation = 'NO'
        price_scalar = 0.0

        if relationship > 0:
            relation = 'ADD'
            price_scalar = 1.0
        elif relationship < 0:
            relation = 'SUB'

        self._relation = relation
        self._price_scalar = price_scalar
        return relation

    def get_option_relation(self):
        """Gets the relation of this option.
        This relation effects how this option
        interacts with other options or MenuItems.

        @return: str representing if the relation
        is additive and thus "ADD", removal and thus
        "NO" or substitution and thus "SUB".
        """
        return self.relation

    def __repr__(self):
        """Get a string representation of this
        OptionItem.

        @return: str representing the option
        """
        return self.get_name()
