""" This module contains the MenuItem class that stores
information about MenuItems, and the OptionItem class that
stores information about OptionItems

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
        self._notification_message = None
        
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
        return self._price_scalar == 0.0 and self._notification_message

    def get_comp_message(self):
        """Gets the comp message associated
        with this item.

        @return: str representing the message
        associated with the comp. None if there
        is_comped returns false.
        """
        return self._notification_message

    def comp(self, value, message):
        """

        @param value: bool if the menu item
        should be comped, or not.

        @param message: str representing the
        message associated with this comp.
        """
        if value:
            self._price_scalar = 0.0
            self._notification_message = message
        else:
            self._price_scalar = 1.0
            self._notification_message = None
    
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

    def is_notification(self):
        """Checks if the current MenuItem
        object is a notification item.

        @return: bool representing if the
        MenuItem is a notification item.
        """
        return self.is_comped()
    
    def get_option_choices(self):
        """Gets a copy of the current options choices dict.
        
        @return: dict where each key is a str that represents
        an option, and each value is a float that represents
        the cost.
        """
        options_copy = copy(self._option_choices)

        for option in options_copy:

            if not option._price_scalar == 0.0:
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
        return self.__dict__ == other.__dict__


class DiscountItem(MenuItem):
    """This object stored information relating to the
    DiscountItem which is a special type of MenuItem
    that represents a discount to be applied.
    """

    def __init__(self, name, price, discount_message):
        """Initializes a new DiscountItem.

        @param name: str representing the name to be
        associated with this discount.

        @param price: float representing the price to
        be associated with this discount item. Negative
        prices will be subtracted from an order, positive
        prices will be added to an order.

        @param discount_message: str representing the
        message to be associated with the DiscountItem
        """
        super(DiscountItem, self).__init__(name, price)
        self._notification_message = discount_message

    def get_discount_message(self):
        """Gets the discount message associated
        with this DiscountItem.

        @return: str representing the message
        associated with this DiscountItem.
        """
        return self._notification_message

    def is_notification(self):
        """Checks if the DiscountItem is
        a notification item.

        By default always returns true.

        @return: True because all DiscountItems
        by definition are notification items.
        """
        return True


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
    def __init__(self, name, category, price):
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
        self._category = category

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

    def get_category(self):
        """Gets the category that this
        option is associated with.

        @return: str representing the
        category in all caps.
        """
        return self._category

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
        return self._relation

    def __repr__(self):
        """Get a string representation of this
        OptionItem.

        @return: str representing the option
        """
        return str(self.get_option_relation()) + ': ' + self._name

    def __eq__(self, other):
        """Compares this option item to
        the given option item.

        @param other: OptionItem object that
        is to be compared to this OptionItem

        @return: bool value that is True if the
        two OptionItems are equal, False otherwise.
        """
        return self.__dict__ == other.__dict__

    def __cmp__(self, other):
        """Compares to OptionItem
        to another OptionItem. Comparison
        is made according to the relation
        that they hold, following the order
        of "ADD" < SUB" < "NO". If both items
        hold the same relation then the
        comparison is made on name.

        @param other: OptionItem object that
        is to be compared to this object.

        @return: Value representing the
        comparison of the two objects. If
        positive this object is considered
        greater than the other, if 0 then
        they are considered equal, if
        negative the given object is greater
        than this one.
        """
        cmp_value = cmp(self._relation, other._relation)

        if cmp_value == 0.0:
            cmp_value = cmp(self._name, other._name)

        return cmp_value
