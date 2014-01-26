"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from .ValueDataArea import ValueDataArea

from src.peonordersystem.audit.datasheet.parsers.PackagedDataParser import \
    PackagedDataParser


class ItemsTimeDataArea(ValueDataArea):
    """This class represents an area used
    for storing the items data by time
    keys
    """

    def __init__(self, keys_area):
        """Initializes a new ItemsTimeDataArea
        object.

        @param keys_area: DataArea that represents
        the data area that stores the keys data.
        """
        package_value = PackagedDataParser('TIME', 'ITEMS')
        self.keys_area = keys_area
        super(ItemsTimeDataArea, self).__init__(package_value, keys_area.data)


class OrdersTimeDataArea(ValueDataArea):
    """This class represents an area used
    for storing orders data by time keys.
    """

    def __init__(self, keys_area):
        """Initializes a new OrdersTimeDataArea
        object.

        @param keys_area: DataArea that represents
        the data area that stores the keys data.
        """
        package_value = PackagedDataParser('TIME', 'ORDERS')
        self.keys_area = keys_area
        super(OrdersTimeDataArea, self).__init__(package_value, keys_area.data)


class TotalsTimeDataArea(ValueDataArea):
    """This class represents an area
    used for storing totals data by time
    keys.
    """

    def __init__(self, keys_area, data=[]):
        """Initializes a new TotalsTimeDataArea
        object.

        @param keys_area: DataArea that represents
        the data area that stores the keys data.
        """
        package_value = PackagedDataParser('TIME', 'TOTALS')
        self.keys_area = keys_area
        super(TotalsTimeDataArea, self).__init__(package_value, keys_area.data)


class ItemsDateDataArea(ValueDataArea):
    """
    
    """
    
    def __init__(self, keys_area, data=[]):
        """
        
        @param keys_area: 
        @param data: 
        @return:
        """
        package_value = PackagedDataParser('DATE', 'ITEMS')
        self.keys_area = keys_area
        super(ItemsTimeDataArea, self).__init__(package_value, keys_area.data)

class OrdersDateDataArea(ValueDataArea):
    """

    """

    def __init__(self, keys_area, data=[]):
        """

        @param keys_area:
        @param data:
        @return:
        """
        package_value = PackagedDataParser('DATE', 'ORDERS')
        self.keys_area = keys_area
        super(OrdersDateDataArea, self).__init__(package_value, keys_area.data)

class TotalsDateDataArea(ValueDataArea):
    """

    """

    def __init__(self, keys_area, data=[]):
        """

        @param keys_area:
        @param data:
        @return:
        """
        package_value = PackagedDataParser('DATE', 'TOTALS')
        self.keys_area = keys_area
        super(TotalsDateDataArea, self).__init__(package_value, keys_area.data)