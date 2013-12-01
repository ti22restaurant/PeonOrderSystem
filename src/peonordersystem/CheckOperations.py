'''This module provides the basic functions
that calculate the total and taxes on any
given check.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
'''
import math

from src.peonordersystem.Settings import SALES_TAX

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
        
    return total

def get_total_tax(subtotal):
    """Gets the total tax to be added from
    a given subtotal.
    
    @param subtotal: double representing the 
    subtotal of an order.
    
    @return: double representing the tax to be added
    to the total.
    """
    return math.ceil(subtotal * SALES_TAX * 100) / 100

def get_total(order_list):
    """Gets the total of the order, tax included.
    
    @param order_list: list of MenuItem objects that
    comprise an order.
    
    @return: double representing the total value to be
    charged to the customer
    """
    sub_total = get_order_subtotal(order_list)
    return sub_total + get_total_tax(sub_total)