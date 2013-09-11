'''

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
'''
import os
import cPickle
import time

from peonordersystem import path


directory = path.SYSTEM_ORDERS_PATH

current_date = time.localtime()[:3]

for value in current_date:
    directory = directory + '{}/'.format(value)
    
    if not os.path.exists(directory):
        os.mkdir(directory)



def generate_files():
    """
    """
    table_orders = {}
    togo_orders = {}
    
    curr_directory = directory + 'confirmed/'
    
    if not os.path.exists(curr_directory):
        os.mkdir(curr_directory)
        os.mkdir(directory + 'checkout/')
    else:
        itr = os.walk(curr_directory)
        dirpath, dirnames, filenames = itr.next()
        
        for curr_filename in filenames:
            
            filename, filetype = curr_filename.split('.')
            
            if filetype is 'table':
                current_orders = table_orders
            else:
                current_orders = togo_orders
            
            for f in curr_filename:
                unpickle = cPickle.Unpickler(curr_directory + f)
                current_orders[filename] = unpickle.load()
                
    return (table_orders, togo_orders)

def order_confirmed(order_name, order_list):
    curr_directory = directory + '/confirmed/'
    
    curr_file = open(curr_directory + order_name, 'w')
    
    cPickle.dump(order_list, curr_file)
            
                