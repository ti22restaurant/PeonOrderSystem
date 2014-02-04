"""This module contains the CategoryMean
class which is used to store and update
mean data based on categories.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""


class CategoryMean(object):
    """This class stores the mean data for a
    single category by storing the number of occurrences
    of that category and the sum of all category values.
    """

    def __init__(self, round_digits=4):
        """Initializes a new CategoryMean"""
        self._round_digits = round_digits
        self._categories = set()
        self._sum = 0.0

    @property
    def data(self):
        """Gets the mean value associated
        with the CategoryMean

        @return: float representing the mean
        """
        if self._categories:
            return round(self._sum / len(self._categories), self._round_digits)
        return 0.0

    def update(self, category, value):
        """Updates by adding the given
        value to the mean and adds the
        category. If the category already
        exists then the value is updated.

        @param category: representing
        the category.

        @param value: int representing the
        value.

        @return: float representing the
        value that the mean was adjusted
        by.
        """
        self._check_data(category)
        self._check_data(value)

        prev_mean = self.data
        self._categories.add(category)
        self._sum += value
        return self.data - prev_mean

    def _check_data(self, data):
        """

        @param data:
        @return:
        """
        if data == None:
            raise ValueError('Mean cannot be update given a null value or category')
        return True
