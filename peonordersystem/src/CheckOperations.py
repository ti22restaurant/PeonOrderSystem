"""This module provides the basic functions
that calculate the total and taxes on any
given check.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import math

from Settings import SALES_TAX


def get_totals(order_list):
    """Gets a tuple of totals
    that represent the totals
    associated with the given
    order list.

    @param order_list: list of
    MenuItem objects representing
    the data to parse.

    @return: three tuple of
    (float, float, float)
    representing the subtotal,
    tax, and total respectively.
    """
    subtotal = get_order_subtotal(order_list)
    tax = get_total_tax(subtotal)

    return subtotal, tax, round(subtotal + tax, 2)


def get_order_subtotal(order_list):
    """Gets the current subtotal of the given
    order_list. 
    
    @param order_list: list of MenuItems that comprise
    an order.
    
    @return: double value representing the subtotal obtained
    by combining each MenuItem's price.
    """
    total = 0.0
    
    for menu_item in order_list:
        total = total + menu_item.get_price()
        
    return round(total, 2)


def get_total_tax(subtotal):
    """Gets the total tax to be added from
    a given subtotal.
    
    @param subtotal: double representing the 
    subtotal of an order.
    
    @return: double representing the tax to be added
    to the total.
    """
    tax = math.ceil(subtotal * SALES_TAX * 100) / 100
    return round(tax, 2)


def get_total(order_list):
    """Gets the total of the order, tax included.
    
    @param order_list: list of MenuItem objects that
    comprise an order.
    
    @return: double representing the total value to be
    charged to the customer
    """
    sub_total = get_order_subtotal(order_list)
    return sub_total + get_total_tax(sub_total)