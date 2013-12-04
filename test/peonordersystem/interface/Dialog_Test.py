"""This module provides classes for testing each
dialog window present in the dialog module.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
from src.peonordersystem import path
from src.peonordersystem.interface import Dialog

from test.peonordersystem.standardoperations_test import generate_random_date

from gi.repository import Gtk # IGNORE:E0611 @UnresolvedImport

import unittest
import datetime
import random


TEST_CASE_FAILURE = 'Dialog_Test.py'

TABS = '    '

print TEST_CASE_FAILURE


class AuditDataSelectionDialogTest(unittest.TestCase):
    """Test class for the AuditDataSelectionDialog class.

    This class tests all the functionality of the dialog
    window not pertaining to used libraries.
    """
    print TABS + 'AuditDataSelectionDialogTest'

    def setUp(self):
        """Sets up before a test is run.

        @return: None
        """
        self.dialog = Dialog.AuditDataSelectionDialog(None, self.confirm_func)
        self.start_date = None
        self.end_date = None
        self.location = None
        self.name = None

    def tearDown(self):
        """Clears all data after a test has been run.

        @return: None
        """
        del self.dialog
        del self.start_date
        del self.end_date
        del self.location
        del self.name

    def set_calendar_selection(self, date):
        """Sets the dialogs calendar selection
        to the date pointed to by the given parameter.

        @param date: datetime.date object that
        represents the date to be selected.

        @return: None
        """
        calendar = self.dialog.selection_calendar
        calendar.select_month(date.month - 1, date.year)
        calendar.select_day(date.day)

    def confirm_func(self, start_date, end_date, location=None, name=None):
        """Tests the confirm_func given to the audit dialog
        that is called upon confirmation. This method checks
        for the proper parameters passed to the function

        @param start_date: datetime.date object that represents
        the beginning date for the audit. Inclusive.

        @param end_date: datetime.date object that represents
        the ending date for the audit. Inclusive.

        @keyword location: str representing the directory location
        for the file to be saved to.

        @keyword name: str representing the name for the file
        to be saved as.

        @return: None
        """
        # Case 1: Sanity check. Dates range makes sense,
        # and the path exists.
        self.assertTrue(start_date <= end_date)

        if location:
            self.assertTrue(len(location) > 0)
        if name:
            self.assertTrue(len(name) > 0)

        # Case 2: Check that information given from called audit
        # dialog is the same information that was set up to be
        # sent.
        self.assertEqual(self.start_date, start_date)
        self.assertEqual(self.end_date, end_date)
        self.assertEqual(self.location, location)
        self.assertEqual(self.name, name)

    def test_date_selection_display(self):
        """Tests the date selection display.

        Specifically the dates selection display
        regards the two Gtk.Entry objects that
        display which date has been selected for
        their respective ranges. This method checks
        that altering the dates selection doesn't
        alter the information displayed to the user.

        @return: None
        """
        print TABS * 2 + 'Testing date selection display'

        start_date_entry = self.dialog.from_date_display
        end_date_entry = self.dialog.until_date_display

        # For the display there could exist an error when the
        # display changes. By either not accurately displaying
        # the correctly selected date, or by not persisting the
        # values when the calendar or the other date is changed.

        print TABS * 3 + 'Testing changing dates selections...',

        # set previous entry str to expected initial value.
        prev_start_str = ''
        prev_end_str = ''

        for x in range(5):

            # ensure that changing the end date had no effect on the start
            # date displayed.
            self.assertEqual(prev_start_str, start_date_entry.get_text())

            start_date = generate_random_date()
            self.set_calendar_selection(start_date)
            self.dialog.set_start_date()

            prev_start_str = self.dialog._get_date_str(start_date)
            self.assertEqual(prev_start_str, start_date_entry.get_text())

            # ensure that changing the start date had no effect on the end
            # date displayed.
            self.assertEqual(prev_end_str, end_date_entry.get_text())

            end_date = generate_random_date()
            self.set_calendar_selection(end_date)
            self.dialog.set_end_date()

            prev_end_str = self.dialog._get_date_str(end_date)
            self.assertEqual(prev_end_str, end_date_entry.get_text())

        print 'done'

        # This area will test the range of the displays to determine
        # if there is any errors in the ranges of the dates
        #
        # Three possible cases:
        #   1. start_date < end_date
        #   2. start_date = end_date
        #   3. start_date > end_date
        #
        #   These three cases should encompass all possibilities
        #   of code display. All three should be adequately displayed.

        print TABS * 3 + 'Testing changing dates range...',

        start_date = generate_random_date()

        self.set_calendar_selection(start_date)
        self.dialog.set_start_date()

        # Index : Case#
        #   0   :   1
        #   1   :   2
        #   2   :   3
        domain_values = [(1, 250), (0, 0), (-250, -1)]

        for low, high in domain_values:

            # Additional for loop to ensure uniformity
            # in results over short and large gaps.
            for x in range(10):

                delta_time = datetime.timedelta(days=random.randint(low, high))

                end_date = start_date + delta_time

                self.set_calendar_selection(end_date)
                self.dialog.set_end_date()

                start_date_str = self.dialog._get_date_str(start_date)
                end_date_str = self.dialog._get_date_str(end_date)

                self.assertEqual(start_date_str, start_date_entry.get_text())
                self.assertEqual(end_date_str, end_date_entry.get_text())

        print 'done'

        print TABS * 2 + 'Finished Date selection display tests'

    def test_date_selection_bounds_update(self):
        """Tests the date selection portion of
        the dialog.

        This testing method checks if the date bounds
        are updated when new selections are made

        @return: None
        """
        print TABS * 2 + 'Testing date selection bounds updating'
        date_bounds = self.dialog.date_bounds

        # Similar to the display testing this testing
        # is focused on the changing of start and end
        # dates and if it adequately reflects the changes
        # in the dialog wide date bounds, and if these
        # associated date bounds match up with the
        # expected data.

        # set previous dates to expected initial values.

        # Cases:
        #
        # Possible cases exist at the boundary conditions
        # specifically three possible cases which need to
        # be tested for.
        #
        #   1. start_date < end_date
        #   2. start_date = end_date
        #   3. start_date > end_date

        print TABS * 3 + 'Testing changing selection bounds...',
        prev_start_date = 0.0
        prev_end_date = 0.0

        # index | case#
        #   0       1
        #   1       2
        #   2       3
        domain_values = [(1, 250), (0, 0), (-250, -1)]

        for low, high in domain_values:

            # Additional for loop to test additional cases
            # to ensure uniformity from small vs great differences.
            for x in range(10):

                self.assertEqual(prev_start_date, date_bounds[0])

                prev_start_date = generate_random_date()
                self.set_calendar_selection(prev_start_date)
                self.dialog.set_start_date()

                self.assertEqual(prev_start_date, date_bounds[0])

                self.assertEqual(prev_end_date, date_bounds[1])

                time_delta = datetime.timedelta(days=random.randint(low, high))
                prev_end_date = prev_start_date + time_delta

                self.set_calendar_selection(prev_end_date)
                self.dialog.set_end_date()

                self.assertEqual(prev_end_date, date_bounds[1])

        print 'done'

        print TABS * 2 + 'Finished date selection bounds updating tests'

    def test_name_edit_toggle(self):
        """Tests the method that is used to edit
        the name associated with the file that is
        supposed saved as.

        @return: None
        """
        print TABS * 2 + 'Testing name edit toggle'
        toggle_button = Gtk.ToggleButton()
        name_entry = self.dialog.name_entry

        # Two testing cases here.
        #
        #   name entry sensitivity
        #   1. Gtk.Widget name_entry and toggle_button are both linked in
        #   reference to sensitivity. When toggle is toggled the sensitivty
        #   of the name_entry changes as well.
        #
        #   name entry text
        #   2. Gtk.Widget name_entry are toggle_button are both linked in
        #   reference to the stored text for the name_entry. When toggle
        #   is toggled the stored text should be either the class constant
        #    DEFAULT_FILE_NAME or '' an empty str.

        print TABS * 3 + 'Testing name entry sensitivity...',

        # Check initial state where both values are false
        self.assertEqual(name_entry.is_sensitive(), toggle_button.get_active())

        # Check if the toggle and untoggle cases work properly for
        # multiple toggles.
        for x in range(3):
            is_active = toggle_button.get_active()
            toggle_button.set_active(not is_active)
            self.dialog.name_toggled(toggle_button)

            self.assertEqual(name_entry.get_sensitive(),
                             toggle_button.get_active())
        print 'done'
        print TABS * 3 + 'Testing name entry text...',

        # Check initial state enter this test phase.
        self.assertEqual(name_entry.get_text(), '')

        # Check if the stored text in the entry matches
        # the associated toggle state.
        for x in range(3):
            is_active = toggle_button.get_active()
            toggle_button.set_active(not is_active)
            self.dialog.name_toggled(toggle_button)

            if toggle_button.get_active():
                self.assertEqual(name_entry.get_text(), '')
            else:
                self.assertEqual(name_entry.get_text(),
                                 self.dialog.DEFAULT_FILE_NAME)
        print 'done'
        print TABS * 2 + 'Finished name edit toggle tests'

    def test_location_edit_toggle(self):
        """Tests the methods that are associated
        with editing the location that the audit
        will be saved at.

        @return: None
        """
        print TABS * 2 + 'Testing location edit toggle'

        toggle_button = Gtk.ToggleButton()
        location_display = self.dialog.location_entry

        CANCEL_RESPONSE = Gtk.ResponseType.CANCEL
        ACCEPT_RESPONSE = Gtk.ResponseType.ACCEPT

        file_chooser = Gtk.FileChooserDialog('', None, Gtk.FileChooserAction.SAVE)

        file_chooser.was_used = False

        file_paths = [
            path.SYSTEM_DIRECTORY_PATH,
            path.SYSTEM_DATA_PATH,
            path.SYSTEM_LOG_PATH,
            path.SYSTEM_UI_PATH,
            path.SYSTEM_FILE_PATH,
            path.SYSTEM_ORDERS_PATH,
            path.SYSTEM_AUDIT_PATH,
        ]

        DEFAULT_LOCATION = self.dialog.DEFAULT_FILE_PATH

        # Testing cases here will focus on the response
        # from the location display to the toggle button.
        # three possible cases exist here, 2 sets relating
        # to possible responses to the toggle button and
        # the file chooser.
        #
        # Throughout all cases location_display shouldn't ever be
        # sensitive.
        #
        # case 1:
        #   Toggle Button is active, File Chooser response is ACCEPT
        #
        # case 2:
        #   Toggle Button is active, File Chooser response is CANCEL
        #
        # case 3:
        #   Toggle Button is Inactive, File Chooser response is NONE since
        #   it is not activated.

        print TABS * 3 + 'Testing Toggle button and file chooser responses...',

        for file_path in file_paths:

            # Case 1.
            file_chooser.set_current_name(file_path)
            toggle_button.set_active(True)

            self.dialog.location_toggled(toggle_button, file_chooser=file_chooser,
                file_chooser_response=ACCEPT_RESPONSE)

            self.assertEqual(location_display.get_text(), file_path)
            self.assertEqual(toggle_button.get_active(), True)

            # conditional allows staggering to Case 1 and Case 3
            if file_paths.index(file_path) % 2 == 0:
                # case 2:
                self.dialog.location_toggled(toggle_button,file_chooser=file_chooser,
                    file_chooser_response=CANCEL_RESPONSE)

                self.assertEqual(location_display.get_text(), DEFAULT_LOCATION)
                self.assertEqual(toggle_button.get_active(), False)

            # conditional allows staggering to Case 1 and Case 2
            if file_paths.index(file_path) % 3 == 0:
                # case 3
                toggle_button.set_active(False)

                self.dialog.location_toggled(toggle_button)

                self.assertEqual(location_display.get_text(), DEFAULT_LOCATION)
                self.assertEqual(toggle_button.get_active(), False)

        print 'done'
        print TABS * 2 + 'Finished testing location edit toggle'

    def test_audit_dialog_confirmation(self):
        """Tests the confirmation system for the
        audit dialog window.

        @return: None
        """
        print TABS * 2 + 'Testing audit dialog confirmation'
        # Multiple test cases exist here:
        #
        # 1. start_date < end_date
        # 2. start_date = end_date
        # 3. start_date > end_date
        # 4. w/ location
        # 5. w/ name
        # 6. w/ location and name

        domain_values = (1, 250), (0, 0), (-250, -1)

        directory_values = (None, None), (None, 'audit'), ('/home/carl-m', None),\
                           ('/home/carl-m', 'audit')

        print TABS * 3 + 'Testing confirmation function...',
        for x in range(10):

            start_date = generate_random_date()

            for low, high in domain_values:

                time_delta = datetime.timedelta(random.randint(low, high))
                end_date = start_date - time_delta

                for location, name in directory_values:

                    self.dialog.date_bounds[0] = start_date
                    self.start_date = start_date

                    self.dialog.date_bounds[1] = end_date
                    self.end_date = end_date

                    if location:
                        self.dialog.location_entry.set_text(location)
                        self.location = location

                    if name:
                        self.dialog.name_entry.set_text(name)
                        self.name = name

                    self.dialog.confirm_button_clicked()
        print 'done'
        print TABS * 2 + 'Finished testing audit dialog confirmation'


if __name__ == '__main__':
    unittest.main()