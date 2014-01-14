"""

"""

from abc import ABCMeta, abstractmethod


class SpreadsheetArea(object):
    """

    """
    #================================================================================
    # Constants used for generating the columns area.
    #================================================================================
    AREA_COL_NUM = 3
    AREA_COL_WIDTH = 30

    #================================================================================
    # Constants used for generating the title area.
    #================================================================================
    MAIN_TITLE_ROWS = 1
    SUBTITLE_ROWS = 1

    # Subtract one because of zero based indexing.
    TITLE_AREA_START = 0
    TITLE_AREA_END = TITLE_AREA_START + MAIN_TITLE_ROWS + SUBTITLE_ROWS - 1

    TITLE_AREA_ROW_HEIGHT = 30

    #================================================================================
    # Constants used for generating the total area.
    #================================================================================
    MAIN_TOTAL_ROWS = 1
    SUBTOTAL_ROWS = 2

    # Alter by one because of zero based indexing
    TOTAL_AREA_START = TITLE_AREA_END + 1
    TOTAL_AREA_END = TOTAL_AREA_START + MAIN_TOTAL_ROWS + SUBTOTAL_ROWS - 1

    TOTAL_AREA_ROW_HEIGHT = 20

    #================================================================================
    # Constants used for generating the data area.
    #================================================================================
    # Alter by one because of zero based indexing
    DATA_AREA_START = TOTAL_AREA_END + 1


    def __init__(self, format_dict):
        """

        @return:
        """
        self.format_dict = format_dict

    @property
    def area_end_col(self):
        """

        @return:
        """
        return self.col + self.AREA_COL_NUM - 1

    def connect(self, worksheet):
        """

        @param worksheet:
        @return:
        """
        self.row = worksheet.row
        self.col = worksheet.col

        self.worksheet = worksheet
        self.format_area()
        self.create_title_area()
        self.create_total_area()

        return self.row, self.col + self.AREA_COL_NUM

    def format_area(self):
        """

        @return:
        """
        pass

    @abstractmethod
    def create_title_area(self):
        """

        @return:
        """
        pass

    @abstractmethod
    def create_total_area(self):
        """

        @return:
        """
        pass

    @abstractmethod
    def add(self):
        """

        @return:
        """
        pass

class GeneralDatesheetOrderArea(SpreadsheetArea):
    """

    """

    def __init__(self, packaged_data, format_dict):
        """

        @param packaged_data:
        @param format_dict:
        @return:
        """
        self.packaged_data = packaged_data
        super(GeneralDatesheetOrderArea, self).__init__(format_dict)

    def create_title_area(self):
        """

        @return:
        """
        super(GeneralDatesheetOrderArea, self).create_title_area()

    def create_total_area(self):
        """

        @return:
        """
        super(GeneralDatesheetOrderArea, self).create_total_area()

    def add(self):
        """

        @return:
        """
        pass