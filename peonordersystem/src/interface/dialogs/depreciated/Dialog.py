"""Dialog module stores the following groups:

@group Dialog: This is the main superclass type of all
classes inside this module. All classes have Dialog as
their Abstract Base Class. Dialog provides the general
functionality of a Gtk.Dialog window

@group EntryDialog: This group represents all subclasses of
the EntryDialogs. These are are all classes that instantiate 
new objects of dialog windows. These differ from other types
are they are used for user interactions of adjustments of 
singular menu items.

@group ConfirmationDialog: This group represents all subclasses
of the ConfirmationDialogs and other confirmation type dialogs.
These are all classes that instantiate new object dialog windows.
These differ from the EntryDialogs as they are simply confirmations
of a current orders list and do not allow for adjustment

@group SelectionDialog: This group represents all subclasses of the
SelectionDialog window. Windows of this type generate three separate
boxes that are editable by the user and must be instantiated. Any
confirmation of these windows calls the confirm function passed in
at instantiation.

@group OrderConfirmationDialog: This group represents all subclasses
of the OrderConfirmationDialog. These are all classes that instantiate
some form of the OrderConfirmationDialog windows. These differ from other
types of dialog windows because they rely on the functionality from the
group OrderConfirmationDialog and all of its sub related groups.

@group CheckoutConfirmationDialog: This group represents all subclasses
of the CheckoutConfirmationDialog. These are all classes that instantiate
some form of the CheckoutConfirmationDialog windows. These differ from other
types of dialog windows because they rely on functionality from the group
CheckoutConfirmationDialog and all of its sub related groups.

@group ReservationsDialog: This group represents all classes
of the ReservationsDialog window. ReservationsDialog group are
subclass members of the Dialog group

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import os
import math
from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport
from datetime import datetime, timedelta, date, time
from copy import copy, deepcopy
from abc import ABCMeta, abstractmethod

from peonordersystem.src import CheckOperations
from peonordersystem.src.standardoperations import tree_view_changed
from peonordersystem.src.MenuItem import MenuItem, DiscountItem
from peonordersystem.src.MenuItem import OptionItem
from peonordersystem.src.interface.Orders import Orders
from peonordersystem.src.Settings import (STANDARD_TEXT,
                                          STANDARD_TEXT_BOLD,
                                          UNDONE_CHECKOUT_SEPARATOR,
                                          CTIME_STR,
                                          DEFAULT_AUDIT_NAME,
                                          AUDIT_FILE_TYPE,
                                          FILE_TYPE_SEPARATOR)
from peonordersystem.SystemPath import SYSTEM_AUDIT_REQUESTS_PATH

#========================================================
# This block represents module wide constants that are
# utilized inside and outside of this module to determine
# the responses of the classes and other information.
#========================================================
SPLIT_CHECK_DIALOG_RESPONSE = 99
PRINT_DIALOG_RESPONSE = SPLIT_CHECK_DIALOG_RESPONSE - 1
COMP_DIALOG_RESPONSE = PRINT_DIALOG_RESPONSE - 1
DISCOUNT_DIALOG_RESPONSE = COMP_DIALOG_RESPONSE - 1
GENERAL_OPTIONS_DIALOG_RESPONSE = DISCOUNT_DIALOG_RESPONSE - 1


#=========================================================
# This block represents windows that form the
# Abstract Base Classes that cannot be instantiated.
#
# Classes contained in this block are represented as
# top level group classes of other windows that can
# be instantiated.
#
# Names follow a certain pattern. You can find out
# which groups are the super classes by checking the
# @group notation in the docstring of the class or
# by their naming convention. Which will be the classes
# name followed by its super classes.
#=========================================================
class Dialog(object):
    """Abstract Base Class. Provides the base functionality
    for a Dialog window.
    
    @group Dialog: This class is the Abstract Base Class for
    all Dialog objects. All members of any subclass or subgroup
    of Dialog objects have this as the main Abstract Base Class.
    
    @var dialog: Gtk.Dialog window representing the dialog on
    which all actions are performed.
    
    @requires: generate_layout method which sets the base layout
    of the content_area in the Gtk.Dialog. This generate layout
    method must return a box representing the top parent component
    to be added to the content_area of the Gtk.Dialog. A call on
    this method via super yields a pass statement
    
    @requires: confirm_button_clicked method which designates the
    method performed when the Gtk.Dialog's Confirm button has been
    clicked. A call on this classes method via super causes the
    appropriate signal to be emitted and the Gtk.Dialog to hide.
    
    @requires: cancel_button_clicked method which designates the
    method performed when the Gtk.Dialog's Cancel button has been
    clicked. A call on this classes method via super causes the
    appropriate signal to be emitted and the Gtk.Dialog to hide
    """
    __metaclass__ = ABCMeta
    
    def __init__(self, parent, title, dialog=None,
                 default_size=(400, 400)):
        """ Initializes the base Gtk.Dialog window
        and creates the functionality of its action
        area by adding confirm and cancel buttons.
        During initialization generate_layout is called.

        @param title: str representing the title to be
        displayed on this Gtk.Dialog window
        
        @param parent: Object representing the object that
        the Gtk.Dialog was called from. Expected Gtk.Window
        """
        # if statement allows for potential change so that
        # given a dialog each dialog window would not be
        # generated, instead only instances would change.
        #
        # Currently this is not fully functional and therefore
        # should not be used
        if dialog is not None:
            dialog.set_title(title)
            self.dialog = dialog
            dialog.set_transient_for(parent)
            content_area = dialog.get_content_area()
            content_area.remove(self.dialog.content_box)
            
        else:
            self.dialog = Gtk.Dialog(title)
            # Any object is acceptable as parent as long as this
            # set_transient_for method operates appropriately
            self.dialog.set_transient_for(parent)
            self.dialog.set_modal(True)
            self.dialog.resize(default_size[0], default_size[1])

            action_area = self.dialog.get_action_area()
            
            cancel_button = Gtk.Button('Cancel')
            cancel_button.set_can_focus(False)
            cancel_button.set_size_request(80, 50)
            confirm_button = Gtk.Button('Confirm')
            confirm_button.set_can_focus(False)
            confirm_button.set_size_request(100, 50)
            
            action_area.set_homogeneous(True)
            
            action_area.pack_start(confirm_button, True, True, 5)
            action_area.pack_start(cancel_button, True, True, 5)
            action_area.show_all()
            
            cancel_button.connect("clicked", self.cancel_button_clicked)
            confirm_button.connect("clicked", self.confirm_button_clicked)
        
        content_area = self.dialog.get_content_area()
        self.dialog.content_box = self.generate_layout()
        content_area.pack_start(self.dialog.content_box, True, True, 5)
        content_area.show_all()
    
    @abstractmethod
    def generate_layout(self):
        """ Abstract Method. Represents the layout
        to be generated on the content_area of the
        Gtk.Dialog.
        
        @return: Gtk.Widget representing the top level
        component to be added directly to the Gtk.Dialog's
        content_area. This widget will be set to fill and
        expand the content area.
        """
        pass
    
    @abstractmethod
    def confirm_button_clicked(self, *args):
        """ Abstract Method. Represents the
        method called when the Gtk.Dialog's confirm
        button is clicked in the action_area.

        @param args: wildcard catchall used to catch
        the widget that activated this method.

        @attention: super calls on this method yield
        the appropriate response to be emitted by the
        Gtk.Dialog window and then the dialog to hide.
        This functionality is utilized by sub classes.

        @return: int representing a Gtk.ResponseType
        that is associated with this dialog windows
        appropriate button.
        """
        self.dialog.response(Gtk.ResponseType.ACCEPT)
        self.dialog.hide()
        return Gtk.ResponseType.ACCEPT

    @abstractmethod
    def cancel_button_clicked(self, *args):
        """ Abstract Method. Represents the callback
        method called when the Gtk.Dialog's cancel
        button is clicked in the action_area.

        @param args: wildcard catchall used to catch
        the widget that activated this method.

        @attention: super calls on this method yield
        the appropriate response to be emitted by the
        Gtk.Dialog window and then the dialog to hide.
        This functionality is utilized by sub classes.

        @return: int representing a Gtk.ResponseType
        that is associated with this dialog windows
        appropriate button.
        """
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()
        return Gtk.ResponseType.CANCEL
    
    def run_dialog(self):
        """Runs the stored dialog window.
        
        @return: int representing the Gtk.ResponseType signal
        emitted
        """
        return self.dialog.run()


class EntryDialog(Dialog):
    """ Abstract class that provides base functionality
    of an EntryDialog
    
    @group Dialog: subclass member of the Dialog group
    
    @group EntryDialog: This is the ABC or Abstract Base Class
    of the EntryDialog group. This class is extended by all
    members of the EntryDialog group. All EntryDialog members
    are also subclass members of the Dialog group
    
    @requires: set_layout method to be overridden. This method is called
    during the initialization phase and is passed in a list of 3 boxes,
    representing the left, center, and right VBoxes of the main content
    area
    
    @requires: confirm_data method to be overridden. This method is called
    whenever the confirmation signal is given.
    
    @requires: cancel_data method to be overridden. This method is called
    whenever the cancel signal is given.
    """
    # for ABC or abstract base class
    __metaclass__ = ABCMeta
    
    def __init__(self, parent, title, dialog=None):
        """Initializes the basic EntryDialog object, and generates
        the base layout for the EntryDialog window.
        
        @param parent: object that is the parent of this EntryDialog.
        Expected Gtk.Window object. 
        
        @param title: str representing the title to be displayed on
        the EntryDialog window.
        
        @keyword dialog: potential dialog to be added. This feature is
        not fully supported
        """
        super(EntryDialog, self).__init__(parent, title, dialog)
    
    def generate_layout(self):
        """Generates the layout for the base EntryDialog window.
        This method generates the content area by creating
        a main box and three subdivided VBoxes to store the
        necessary data. This method also calls the set_layout
        function passing in the three generated VBoxes.
        
        @return: Gtk.Container that holds the basic
        layout that was generated.
        """
        content_area = Gtk.HBox(True, 5)
        content_boxes = []
        
        box1 = Gtk.VBox(True, 5)
        box1.set_homogeneous(True)
        content_area.pack_start(box1, True, True, 5)
        content_boxes.append(box1)
        
        box2 = Gtk.VBox(True, 5)
        box2.set_homogeneous(True)
        content_area.pack_start(box2, True, True, 5)
        content_boxes.append(box2)
        
        box3 = Gtk.VBox(True, 5)
        box3.set_homogeneous(True)
        content_area.pack_start(box3, True, True, 5)
        content_boxes.append(box3)
        
        self.set_layout(content_boxes)
        
        return content_area
        
    @abstractmethod
    def set_layout(self, content_boxes):
        """Abstract Method that sets the layout of the
        given three content boxes.
        
        @param content_boxes: list representing the boxes
        generated in the generate_layout method

        @return: None
        """
        pass
    
    def confirm_button_clicked(self, *args):
        """Callback method that is called when the confirmed
        button is clicked. This method calls the confirm_data
        method and superclass confirm_button_clicked method
        
        @param *args: wildcard catchall that is used to
        catch the widget that called this method.
        """
        self.confirm_data()
        super(EntryDialog, self).confirm_button_clicked()
    
    def cancel_button_clicked(self, *args):
        """Callback method that is called when the cancel
        button is clicked. This method calls the cancel_data
        method and superclass cancel_button_clicked method
        
        @param *args: wildcard catchall that is used to
        catch the Gtk.Widget that called this method.
        """
        self.cancel_data()
        super(EntryDialog, self).cancel_button_clicked(*args)
    
    @abstractmethod
    def confirm_data(self):
        """Abstract Method that is called whenever
        the confirm button has been clicked. After
        completion the window is unaccessible to the
        user

        @return: None
        """
        pass
    
    @abstractmethod
    def cancel_data(self):
        """Abstract Method that is called whenever
        the cancel button has been clicked. After
        completion the window is unaccessible to the
        user.

        @return: None
        """
        pass


class ConfirmationDialog(Dialog):
    """Abstract Base Class. ConfirmationDialog provides
    the base functionality for a ConfirmationDialog window.

    @group Dialog: Subclass member of the Dialog group

    @group ConfirmationDialog: Abstract Base Class of
    the ConfirmationDialog group. This class is a super
    class of all members of the ConfirmationDialog group

    @requires Override generate_columns method that
    returns a list of columns to be added to the
    Gtk.TreeView that will be displayed as part of
    the ConfirmationDialog

    @var confirm_func: Pointer to the callback function
    that is called when the dialog has been confirmed
    """

    __metaclass__ = ABCMeta

    def __init__(self, parent, title, dialog=None,
                 default_size=(600, 700)):
        """Initializes the Abstract Base functionality
        of the ConfirmationDialog.

        @param title: str representing the title to be
        displayed on the dialog window.

        @param parent: Object representing the object
        that the Gtk.Dialog was called on. Expected
        Gtk.Window
        """
        self.tree_view = None
        super(ConfirmationDialog, self).__init__(parent, title,
                                                 dialog, default_size)

    def generate_layout(self):
        """Generates the basic layout of the
        ConfirmationDialog. Generates a basic
        Gtk.TreeView object to be added to
        the main content area of the dialog
        window.

        @return: Gtk.ScrolledWindow representing
        the window that the Gtk.TreeView has been
        added too.
        """
        frame = Gtk.Frame()
        scrolled_window = Gtk.ScrolledWindow()
        model = self.generate_model()

        self.tree_view = Gtk.TreeView(model)
        column_list = self.generate_columns()

        for column in column_list:
            self.tree_view.append_column(column)

        scrolled_window.add(self.tree_view)

        selection = self.tree_view.get_selection()
        selection.set_select_function(self._select_method, None)
        frame.add(scrolled_window)

        return frame

    @abstractmethod
    def generate_columns(self):
        """Abstract Method. Generates
        the columns to be displayed in
        the generated Gtk.TreeView.
        Called in the generate_layout
        method.

        @return: list of Gtk.TreeViewColumn
        to be added to the Gtk.TreeView generated
        in generate_layout.
        """
        pass

    @abstractmethod
    def generate_model(self):
        """Abstract Method. Generates the
        basic model that will store
        the data that the Gtk.TreeView
        will display.

        @return: Gtk.TreeModel representing
        the model that contains the data to
        be displayed on the Gtk.TreeView
        """
        pass

    def confirm_button_clicked(self, *args):
        """Callback Method that is called when
        the confirm button on the dialog window
        is clicked.

        @param *args: Gtk.Widget wildcard representing
        the component or Gtk.Widget that emitted the
        signal and called this method.

        @return: expected int that represents
        Gtk.ResponseType of the dialog
        """
        self.confirm_data()
        return super(ConfirmationDialog, self).confirm_button_clicked()

    def confirm_data(self):
        """Called to confirm the confirmation
        function

        @return: None
        """
        pass

    def cancel_button_clicked(self, *args):
        """Callback Method that is called when
        the cancel button is clicked. This method
        calls on base functionality.

        @param *args: Gtk.Widget wildcard that represents
        the component or Gtk.Widget that emitted
        this signal and called this method.

        @return: expected int that represents t
        he Gtk.ResponseType of the dialog.
        """
        self.cancel_data()
        return super(ConfirmationDialog, self).cancel_button_clicked()

    def cancel_data(self):
        """Called to cancel the data submission.

        @return: None
        """
        pass

    def set_selection_type(self, selection_mode):
        """Sets the selection type of the
        current tree_view.

        @param selection_mode: Gtk.SelectionMode that
        represents the chosen mode for the view

        @return: None
        """
        selection = self.tree_view.get_selection()
        selection.set_mode(selection_mode)

    def get_selected(self):
        """ Gets the currently selected item
        from the tree_view.

        @return: 2-tuple (Gtk.TreeModel, Gtk.TreeIter)
        representing the associated model and an iter
        pointing to the selected row.
        """
        selection = self.tree_view.get_selection()
        return selection.get_selected()

    def _select_method(self, selection, model, path, is_selected, *args):
        """Private Method.

        Callback Method to be called when the an item is
        selected in the self.tree_view object.

        @param selection: Gtk.TreeSelection associated with
        the selection made.

        @param model: Gtk.TreeModel associated with the
        model stored in the self.tree_view object.

        @param path: Gtk.TreePath associated with the
        path selected in the self.tree_view object.

        @param is_selected: bool value representing if the
        selected row is selected.

        @param args: catchall wildcard used to catch the
        object that called this method.

        @return: bool, representing if the given row associated
        with path can be selected. Default of True.
        """
        return True


class SelectionDialog(Dialog):
    """Abstract Base Class. Extends the basic
    functionality from the Dialog window.

    This window builds three containers in
    the content area of the dialog window.

    Upon confirmation this class calls the
    given confirm function.

    @group Dialog: This class is a subclass
    member of the Dialog class. Any changes
    in the parents functionality could effect
    the functionality in this class.

    @var confirm_func: Function that is called
    when the dialog window is confirmed.
    """
    __metaclass__ = ABCMeta

    def __init__(self, parent, title, default_size=(950, 500)):
        """Initializes a new SelectionDialog.

        @param parent: Gtk.Object that this dialog
        is to be called on.



        @param title: str representing the title
        to be displayed of this dialog window.
        """
        super(SelectionDialog, self).__init__(parent, title,
                                              default_size=default_size)

    def generate_layout(self):
        """Override Method.

        Generates the layout of the
        content area to be displayed
        in the dialog box.

        @return: Gtk.Container that
        holds all the widgets to be
        displayed in the content area.
        """
        main_box = Gtk.HBox()

        main_selection_area = self.generate_main_selection_area()
        main_box.pack_start(main_selection_area, True, True, 5.0)

        secondary_selection_area = self.generate_secondary_selection_area()
        main_box.pack_start(secondary_selection_area, True, True, 5.0)

        item_selection_area = self.generate_properties_selection_area()
        main_box.pack_start(item_selection_area, True, True, 5.0)

        return main_box

    @abstractmethod
    def generate_main_selection_area(self):
        """Abstract Method.

        Generates the main selection area
        of the SelectionDialog.

        @return: gtk.Container that holds all
        the widgets for the main selection area.
        """
        pass

    @abstractmethod
    def generate_secondary_selection_area(self):
        """Abstract Method.

        Generates the secondary selection area
        of the SelectionDialog

        @return: gtk.Container that holds all the
        widgets for the secondary selection area.
        """
        pass

    @abstractmethod
    def generate_properties_selection_area(self):
        """Abstract Method.

        Generates the properties selection area
        of the SelectionDialog

        @return: gtk.Container that holds all
        the widgets for the properties selection area.
        """
        pass

    @abstractmethod
    def confirm_data(self, *args):
        """Abstract Method.

        Confirms the data.

        @param args: wildcard catchall
        used to catch the arguments
        passed to this from confirm button
        clicked method.

        @return: None
        """
        pass

    def confirm_button_clicked(self, *args):
        """Override Method.

        Confirms the dialog window, calls the
        confirm data method with the given
        arguments

        @param args: wildcard arguments that are
        passed into the confirm function.

        @return: None
        """
        self.confirm_data(*args)
        super(SelectionDialog, self).confirm_button_clicked()

    def cancel_button_clicked(self, *args):
        """Override Method.

        Cancels the dialog window.

        @param args: wildcard catchall for the widget
        that called this method.

        @return: None
        """
        super(SelectionDialog, self).cancel_button_clicked()


#=========================================================
# This block represents windows that form the specific
# classes that can be instantiated. All classes in this
# block perform operations to obtain a new order.
#
# Upon confirmation each class in this block calls
# a given confirmation function that has been passed
# into the class at instantiation.
#
# Each class in this block belongs to the group of classes
# that are subclasses of the Dialog window. Any changes to
# their respective super classes will effect these classes
# as well.
#=========================================================
class AddReservationsDialog(Dialog):
    """AddReservationsDialog prompts the user with
    a dialog window to insert a new reservation into
    the reservations list.

    @group ReservationsDialog: This class is a member of
    the Reservations Dialog group.

    @var self.name_entry: Gtk.Entry representing the
    area that the user inputs the name associated with
    the new reservation.

    @var self.number_entry: Gtk.Entry representing the
    area that the user inputs the number associated with
    the new reservation

    @var hour_combo_box: Gtk.ComboBox representing an
    integer of hours selection to be made by the user.

    @var min_combo_box: Gtk.ComboBox representing an
    integer of minutes selection to be made by the user.
    """

    def __init__(self, parent, confirm_func, *args):
        """initializes a new AddReservationsDialog that
        the user may interact with to add a new reservation
        to the reservations list.

        @param parent: Gtk.Window that the dialog will be
        a child of

        @param confirm_func: pointer to the function that
        is to be called if the window has been confirmed.

        @param *args: wildcard for unexpected parameters
        """
        self.confirm_func = confirm_func
        self.name_entry = None
        self.number_entry = None
        self.hour_combo_box = None
        self.min_combo_box = None
        super(AddReservationsDialog, self).__init__(parent,
                                                    'Add Reservations Dialog')

    def generate_layout(self):
        """Generates the layout to be added to the
        content area of the dialog window.

        @return: Gtk.VBox that is to be added to the
        content area
        """
        t = datetime.now()

        main_box = Gtk.VBox()

        label = Gtk.Label('Name: ')
        main_box.pack_start(label, False, False, 5)

        self.name_entry = Gtk.Entry()
        main_box.pack_start(self.name_entry, False, False, 5)

        label = Gtk.Label('Number: ')
        main_box.pack_start(label, False, False, 5)

        self.number_entry = Gtk.Entry()
        main_box.pack_start(self.number_entry, False, False, 5)

        inner_box1 = Gtk.VBox()
        label = Gtk.Label('Hour ')
        inner_box1.pack_start(label, True, True, 5)

        self.hour_combo_box = Gtk.ComboBoxText()

        for number in range(t.hour, 24):
            self.hour_combo_box.append_text(str(number))

        inner_box1.pack_start(self.hour_combo_box, True, True, 5)

        inner_box2 = Gtk.VBox()
        label = Gtk.Label('Min ')
        inner_box2.pack_start(label, True, True, 5)

        self.min_combo_box = Gtk.ComboBoxText()

        for number in range(0, 60, 15):
            self.min_combo_box.append_text(str(number))

        inner_box2.pack_start(self.min_combo_box, True, True, 5)

        sub_box = Gtk.HBox()
        sub_box.pack_start(inner_box1, True, True, 5)
        sub_box.pack_start(inner_box2, True, True, 5)

        main_box.pack_start(sub_box, False, False, 5)

        main_box.show_all()

        return main_box

    def get_information(self):
        """Gets the information entered by the
        user and returns.

        @return: 3-tuple of (str, str, float) representing
        name, number, and datetime object, respectively.
        """
        name = self.name_entry.get_text().strip()
        number = self.number_entry.get_text().strip()

        hour = int(self.hour_combo_box.get_active_text())
        minute = int(self.min_combo_box.get_active_text())

        selected_time = datetime.now()
        selected_time = selected_time.replace(hour=hour, minute=minute, second=0,
                                              microsecond=0)

        curr_time = datetime.now()

        while selected_time < curr_time:
            selected_time += timedelta(minutes=10)

        return name, number, selected_time

    def confirm_button_clicked(self, *args):
        """Callback method called when the confirm button has been
        clicked.

        @param *args: wildcard that represents a catch all for the
        widget that emitted the call.
        """
        name, number, selected_time = self.get_information()

        if name and number and selected_time:
            super(AddReservationsDialog, self).confirm_button_clicked()
            self.confirm_func(self.get_information())

    def cancel_button_clicked(self, *args):
        """Callback method called when the cancel button
        has been clicked.

        @param *args: wildcard catch all that is used to catch
        the widget that emitted this call.
        """
        super(AddReservationsDialog, self).cancel_button_clicked()


#=========================================================
# This block represents windows that form the specific
# classes that can be instantiated. All classes in this
# block perform operations on a single MenuItem object.
#
# Upon confirmation each class in this block edits the
# given MenuItem object.
#
# Each class in this block belongs to the group of classes
# that are sub classes of EntryDialog and Dialog. Any
# changes in their respective super classes will effect
# these classes as well.
#=========================================================
class OptionEntryDialog(EntryDialog):
    """ Creates, displays and runs an EntryDialog for editing the given
    MenuItem's selected options. Possible button choices for options are
    generated from the given MenuItem's get_option_choices() method. When
    selected this object updates the given MenuItem's stored options to
    include the user selected buttons from the option choices.
    
    Dialog confirmation stores the selected options as the options for
    the given MenuItem. Dialog cancellation returns to the originally
    selected items that the menu item had.
    
    @group EntryDialog: subclass member of the EntryDialog group
    
    @var options: list representing the currently selected menu_item
    options.
    
    @var menu_item: MenuItem object representing the given MenuItem to
    have the EntryDialog perform actions on it. 
    """
    
    def __init__(self, parent, menu_item, dialog=None,
                 title='Option Dialog'):
        """Initializes a new OptionEntryDialog object.
        This method stores the given menu_item, and
        displays the options choices available to the
        user.
        
        @param parent: Object representing the parent from
        which this object was called. This is expected to
        be a Gtk.Window
        
        @param menu_item: MenuItem object representing the
        MenuItem to have the options selected.
        
        @keyword dialog: Gtk.Dialog object that allows for
        the given dialog to be constructed from another
        dialog window. This feature is not fully supported.
        
        """
        self.options = copy(menu_item.options)
        self.menu_item = menu_item
        super(OptionEntryDialog, self).__init__(parent, title, dialog)

    def generate_layout(self):
        """Override Method

        Generates the layout to be
        displayed in the content area
        of the dialog window.

        @return: Gtk.Container that holds
        the Gtk.Widgets that will be displayed
        in the content area.
        """
        main_box = Gtk.VBox()

        if len(self.menu_item.get_option_choices()) > 0:
            content_area = super(OptionEntryDialog, self).generate_layout()
        else:
            content_area = self.generate_empty_option_choices_area()

        main_box.pack_start(content_area, True, True, 5.0)

        additional_options_area = self.generate_additional_options_area()
        main_box.pack_end(additional_options_area, False, False, 5.0)

        return main_box

    def generate_additional_options_area(self):
        """Generates the additional options
        area for this dialog window. This
        options area holds Gtk.Widgets
        associated with additional options
        beyond the designated storage area
        of the super class.

        @return: Gtk.Container that holds
        the Gtk.Widgets that will be displayed
        in the additional options area.
        """
        main_box = Gtk.HBox()

        general_options_button = Gtk.Button('Open General Options')
        general_options_button.set_can_focus(False)
        general_options_button.set_size_request(200, 50)
        general_options_button.connect('clicked', self.general_option_dialog)
        main_box.pack_start(general_options_button, False, False, 5.0)
        main_box.pack_start(Gtk.Fixed(), True, True, 5.0)

        return main_box

    def generate_empty_option_choices_area(self):
        """Generates the option choices area if the
        given MenuItem had an empty options choices
        stored. This occurs so that the general option
        choices can be instantiated.

        @return: Gtk.Container that holds the Gtk.Widgets
        that will be displayed in the empty option_choices
        area.
        """
        main_box = Gtk.HBox()

        label = Gtk.Label("NO AVAILABLE FREQUENT OPTION CHOICES")
        main_box.pack_start(label, False, False, 5.0)
        main_box.pack_start(Gtk.Fixed(), True, True, 5.0)

        return main_box
    
    def set_layout(self, content_boxes):
        """Override Method.

        Sets the layout for the OptionsEntryDialog. Each
        content box in the content_area of the dialog window
        is set to store option toggles in groups of three
        distributed among the three given content boxes stored
        in content_boxes.
        
        @param content_boxes: list where each entry represents
        a box in the subdivided content area of the main EntryDialog.
        There are by default three content boxes stored in content_boxes.

        @return: None
        """
        for option_item in self.menu_item.get_option_choices():
            button_box = content_boxes.pop(0)

            option_name = option_item.get_option_relation() + ": " + \
                          option_item.get_name()

            option_toggle = Gtk.ToggleButton(option_name)
            option_toggle.option_item = option_item
            
            if option_item in self.menu_item.options:
                option_toggle.set_active(True)
            
            # connect signals to add_option for dynamic adds
            option_toggle.connect("toggled", self.add_option)
            button_box.pack_start(option_toggle, True, True, 5)
            content_boxes.append(button_box)
    
    def add_option(self, button):
        """Adds the selected option to the current
        options for the MenuItem. If the button toggle
        is depressed then it removes it from the list.
        
        @param button: Gtk.Button that represents the button
        toggled.

        @return: None
        """
        # Button has been pressed (therefore is now toggled)
        # case 1: Button is active (therefore was not toggled)
        if button.get_active():
            self.options.append(button.option_item)
        # case 2: Button is inactive (therefore was toggled)
        else:
            self.options.remove(button.option_item)

    def general_option_dialog(self, *args):
        """Cancels the selected options, and
        emits the appropriate response for a
        new ADDITIONAL_OPTOINS_DIALOG to be
        opened.

        @param args: wildcard catchall that is
        used to catch the Gtk.Widget that called
        this method.

        @return: None
        """
        self.dialog.response(GENERAL_OPTIONS_DIALOG_RESPONSE)
        self.dialog.destroy()
    
    def cancel_data(self):
        """Cancel's selected options, and reverts to
        previously selected options set for the stored 
        MenuItem
        
        @return: None
        """
        return super(OptionEntryDialog, self).cancel_data()
    
    def confirm_data(self):
        """Confirms the selected options and stored them
        in the MenuItem's options attribute

        @return: None
        """
        self.menu_item.options = self.options


class NoteEntryDialog(EntryDialog):
    """Creates, displays and runs an EntryDialog that
    takes a given MenuItem and allows the user to alter
    the stored note.
    
    Dialog confirmation stores the new note as the
    MenuItems note. Dialog cancellation restores the
    original note.
    
    @group EntryDialog: subclass member of the EntryDialog
    group
    
    @var menu_item: MenuItem object that represents the
    given MenuItem that this EntryDialog is performing
    on.
    
    @var text_entry: Gtk.Entry representing the text
    entry on the dialog window through which the user
    interacts and alters the text.
    
    @var note_label: Gtk.Label representing the current
    note to be displayed as the MenuItems note.
    """
    
    def __init__(self, parent, menu_item, dialog=None,
                 title='Note Entry'):
        """Initializes a new NoteEntryDialog. This method
        stores the MenuItem given, instantiates all of the
        UI components and runs the dialog.
        
        @param parent: Object representing the parent that
        the EntryDialog will open from. This is expected to
        be a Gtk.Window
        
        @param menu_item: MenuItem object that is the given
        MenuItem that the NoteEntryDialog will be operating
        on.
        """
        self.menu_item = menu_item
        self.text_entry = None
        self.note_label = None
        super(NoteEntryDialog, self).__init__(parent, title, dialog)
        
    def generate_layout(self):
        """Overrides generate_layout. This method generates the
        custom NoteEntryDialog layout and then populates that 
        layout with components via the set_layout method.
        
        @return: Gtk.Container representing the main content area
        through which all content components will be displayed.
        """
        content_area = Gtk.VBox()
        self.set_layout(content_area)
        return content_area
    
    def set_layout(self, content_area):
        """Generates and sets the components in the main content
        area of the EntryDialog window.
        
        @precondition: The content_area is called specifically
        from this methods instance of set_layout and as such
        the content_area is simply one Gtk.VBox that fills the
        entire content area.
        
        @param content_area: Gtk.Container that fills the entire content
        area. Components are added directly to this box
        """
        self.text_entry = Gtk.Entry()
        self.text_entry.connect("changed", self.note_edited)
        self.text_entry.connect("activate",
            super(NoteEntryDialog, self).confirm_button_clicked)
        content_area.pack_end(self.text_entry, False, False, padding=5)
        
        item_label = Gtk.Label()
        item_label.set_markup('<span font="Cambria 18.0">' + "<b>" + 
                              self.menu_item.get_name() + "</b>" + '</span>')
        content_area.pack_start(item_label, False, False, padding=5)
        
        self.note_label = Gtk.Label()
        self.note_label.set_line_wrap(True)
        self.note_label.set_markup('<span font="Sans Italic 15.5">' + 
                                   self.menu_item.notes + "</span>")
        content_area.pack_start(self.note_label, True, True, 5)
        
    def note_edited(self, *args):
        """Callback method called when the text_entry receives
        input. This method automatically updates the stored
        Gtk.Label that represents the note.
        
        @param *args: wildcard representing the Gtk.Entry that called
        this method.
        """
        self.note_label.set_markup('<span font="Sans Italic 15.5">' + 
                                   self.text_entry.get_text() + "</span>")
    
    def confirm_data(self):
        """Confirms the entered note and stores it in
        the given MenuItem's notes.
        """
        self.menu_item.notes = self.text_entry.get_text()
    
    def cancel_data(self):
        """Cancels the selected note from being
        stored in the MenuItem. All changes are
        discarded and the note is reverted back
        to its original
        """
        return super(NoteEntryDialog, self).cancel_data()


class StarEntryDialog(EntryDialog):
    """Creates, displays and runs an EntryDialog that
    takes a MenuItem object and allows the user to
    adjust the MenuItem's stars value.
    
    Dialog confirmation stores the new stars value in
    the MenuItem. Dialog cancellation discards changes
    and reverts to original star value.
    
    @group EntryDialog: subclass member of EntryDialog
    group
    
    @var menu_item: representing the given MenuItem that
    is having its stars value adjusted.
    
    @var stars_value: Value of the MenuItem's stars level
    stored as an attribute
    """
    
    def __init__(self, parent, menu_item, dialog=None,
                 title='Star Dialog'):
        """Initializes a new EntryDialog object. This method
        stores the MenuItem and stars information, generates
        all the components for the dialog window and runs the
        dialog.
        
        @param parent: Object representing the parent that this
        EntryDialog window was called on. This is expected to
        be a Gtk.Window
        
        @param menu_item: MenuItem object that this EntryDialog
        is adjusting the star value of.
        """
        self.menu_item = menu_item
        self.stars_value = menu_item.stars
        self.star_label = None
        super(StarEntryDialog, self).__init__(parent, title, dialog)
    
    def generate_layout(self):
        """Overrides generate_layout. This method creates the
        custom layout for the StarEntryDialog.
        
        @return: VBox representing the box stored in the content
        area of the dialog window
        """
        content_area = super(StarEntryDialog, self).generate_layout()
        top_box = Gtk.VBox()
        
        item_label = Gtk.Label()
        item_label.set_markup('<span font="Cambria 18.0">' + "<b>" + 
                              self.menu_item.get_name() + "</b>" + '</span>')
        
        top_box.pack_start(item_label, False, False, 5)
        top_box.pack_end(content_area, True, True, 5)
        return top_box
    
    def set_layout(self, content_boxes):
        """Generates the components and sets the layout
        to be displayed on the main content area of the
        dialog box. 
        
        @param content_boxes: list of content boxes to that
        will be used to display the information of the stars,
        and controls to adjust them. Here it is assumed that
        there are exactly three content boxes stored in this
        list.
        """
        current_box = content_boxes.pop(0)
        decrease_button = Gtk.Button("<")
        decrease_button.connect('clicked', self.decrease_star_value)
        current_box.pack_start(decrease_button, True, True, 5)
        
        current_box = content_boxes.pop(0)
        self.star_label = Gtk.Label()
        self.update_star_label()
        current_box.pack_start(self.star_label, True, True, 5)
        
        current_box = content_boxes.pop(0)
        increase_button = Gtk.Button(">")
        increase_button.connect('clicked', self.increase_star_value)
        current_box.pack_start(increase_button, True, True, 5)
    
    def update_star_label(self):
        """Updates the displayed star level.
        """
        self.star_label.set_markup('<span font="Sans Italic 15.5">' + 
                                   str(self.stars_value) + "</span>")
    
    def decrease_star_value(self, *args):
        """Callback method when decrease button 
        is clicked. Reduces the temporary star 
        level by one. This value is not stored
        in the star value of the MenuItem object.
        
        @param args: wildcard catchall used to catch
        the Gtk.Widget that called this method.
        """
        self.stars_value -= 1
        self.update_star_label()
        
    def increase_star_value(self, *args):
        """Callback method when the increase button
        is clicked. Increases the temporary star
        level by one. This value is not stored
        in the star value of the MenuItem object.

        @param args: wildcard catchall to catch the
        Gtk.Widget that called this method.
        """
        self.stars_value += 1
        self.update_star_label()
    
    def confirm_data(self):
        """Callback method called when the dialog's
        confirm button is clicked. Stores the star
        value as the MenuItem objects stars.
        """
        self.menu_item.stars = self.stars_value
    
    def cancel_data(self):
        """Callback method called when the dialog's
        cancel button is clicked. Discards changes
        to the MenuItem's stars
        """
        return super(StarEntryDialog, self).cancel_data()


#=========================================================
# This block represents windows that form the specific
# classes that can be instantiated. All classes in this
# block perform operations on an entire order, which is
# expected to be represented as a list of MenuItem objects.
#
# Upon confirmation each class in this block calls a given
# function that is passed into the class at instantiation
# as its "confirm func".
#
# Each class in this block belongs to the group of classes
# that are sub classes of ConfirmationDialog and Dialog.
# Any changes in their respective super classes will
# effect these classes as well.
#=========================================================
class OrderConfirmationDialog(ConfirmationDialog):
    """OrderConfirmationDialog displays a dialog window
    prompting the user to either confirm the other and
    thus initiate the confirmed function that was supplied
    or cancel and thus revert to previous window that
    accessed this dialog.
    
    @group Dialog: subclass member of the Dialog window,
    extends all of its functionality, overriding some.
    
    @group ConfirmationDialog: subclass member of the
    ConfirmationDialog window, extends or overrides
    all/some of its functionality.
    
    @var order_list: list of MenuItem objects representing
    the order list the dialog actions will be performed on
    """

    def __init__(self, parent, confirm_func, order_list, dialog=None,
                 title='Order Confirmation'):
        """Initializes the OrderConfirmationDialog window and
        generates the layout. Builds from superclasses.

        @param parent: Object representing the parent that this
        ConfirmationDialog window was called on. Expected
        Gtk.Window
        
        @param confirm_func: Pointer to external function to be
        called when the ConfirmationDialog has confirmed the
        given order_list
        
        @param order_list: list of MenuItem objects that 
        represents the current order being considered for
        confirmation by the ConfirmationDialog 
        """
        self.order_list = order_list
        self. total_row_reference = None
        self.confirm_func = confirm_func
        super(OrderConfirmationDialog, self).__init__(parent, title, dialog)

    def generate_layout(self):
        """Override Method.

        Generates the layout to be displayed
        in the main content area of the dialog
        window.

        @return: Gtk.Widget representing the object
        to be displayed in the main content area of
        the dialog window.
        """
        main_box = Gtk.VBox()

        scrolled_window = super(OrderConfirmationDialog, self).generate_layout()
        main_box.pack_start(scrolled_window, True, True, 5)

        button_box = Gtk.HBox()
        widgets = self.generate_misc_widgets()

        for widget in widgets:
            button_box.pack_start(widget, False, False, 5)

        main_box.pack_start(button_box, False, False, 5)

        return main_box

    def generate_misc_widgets(self):
        """Generates the misc widgets associated
        with this layout.

        @return: list of Gtk.Widget that are to
        be added to the content area's button
        area.
        """
        widget_list = []

        priority_button = Gtk.Button('Add Priority')
        priority_button.set_size_request(200, 50)
        priority_button.connect('clicked', self._set_selected_priority)

        widget_list.append(priority_button)

        return widget_list

    def generate_columns(self):
        """Generates the columns for the
        OrderConfirmationDialog.
        
        @return: list of Gtk.TreeViewColumn
        objects that are utilized in building
        the layout of the Gtk.TreeView that
        displays the data
        """
        column_list = []
        
        size = self.dialog.get_size()
        horizontal = size[0]
        
        renderer = Gtk.CellRendererText()
        renderer.set_property('weight-set', True)
        renderer.set_property('wrap-width', horizontal)
        col1 = Gtk.TreeViewColumn('Menu Item', renderer,
                                  text=0, weight=2)
        column_list.append(col1)

        col2 = Gtk.TreeViewColumn('Stars', renderer,
                                  text=1, weight=2)
        column_list.append(col2)

        return column_list
    
    def generate_model(self):
        """Generates the Gtk.TreeModel
        to be utilized for displaying
        data. Populates the Gtk.TreeModel
        with the current order_list stored
        in this object
        
        @return: Populated Gtk.TreeModel
        that stores the given data passed
        into this objects constructor
        """
        tree_model = Gtk.TreeStore(str, str, int)
        self.add_items_to_model(tree_model)
        
        return tree_model

    def add_items_to_model(self, tree_model):
        """Add the items associated with the
        order being operated on to the given
        model.

        @param tree_model: Gtk.TreeModel
        representing the model that will
        display the information

        @return: None
        """
        for menu_item in self.order_list:

            name = menu_item.get_name()
            stars = str(menu_item.stars)
            info = name, stars, STANDARD_TEXT

            tree_iter = tree_model.append(None, info)

            if menu_item.has_options():

                for option in menu_item.options:

                    name = option.get_option_relation() + ": " +\
                           option.get_name()
                    info = name, '', STANDARD_TEXT
                    tree_model.append(tree_iter, info)

            if menu_item.has_note():

                info = menu_item.notes, None, STANDARD_TEXT
                tree_model.append(tree_iter, info)

    def confirm_data(self, *args):
        """Override Method.

        Callback Method executed when the confirm
        button is pressed. This method calls the
        confirm_func passed into this object.

        @param args: wildcard catchall used to catch
        the widget that activated this method.

        @return: int as Gtk.ResponseType representing
        which response the dialog logged.
        """
        model = self.tree_view.get_model()

        model_iter = iter(model)

        priority_list = []
        normal_order_list = []

        for item in self.order_list:
            row = model_iter.next()

            priority_value = row[2]

            if priority_value == STANDARD_TEXT:
                normal_order_list.append(item)
            else:
                priority_list.append(item)

        self.confirm_func(priority_list, normal_order_list)

    def _set_selected_priority(self, *args):
        """Private Method.

        Toggles the priority level stored in the
        selected items.

        @param args: wildcard catchall that catches
        the widget that activated this method.

        @return: None
        """
        model, itr = self.get_selected()

        itr = ensure_top_level_item(model, itr)
        priority_value = model[itr][2]

        if priority_value == STANDARD_TEXT:
            model[itr][2] = STANDARD_TEXT_BOLD
        else:
            model[itr][2] = STANDARD_TEXT

    
class CheckoutConfirmationDialog(ConfirmationDialog):
    """CheckoutConfirmationDialog displays a current
    order list for review by the user. Confirmation
    leads to the confirm_func being activated and
    thus the checkout procedure continues. Cancellation
    leads to exiting from the dialog.
    
    @group Dialog: subclass member of Dialog. Extends
    or overrides functionality from superclass Dialog
    
    @group ConfirmationDialog: subclass member of the
    ConfirmationDialog. Extends or overrides functionality
    from the superclass ConfirmationDialog
    
    @var order_list: list of MenuItem object that represents
    the current order being considered for checkout

    @var tree_view: defined in super class. Gtk.TreeView associated
    with the display.

    @var total_row_reference: Gtk.TreeRowReference object that is
    associated with the displayed total for the tree_view.
    """

    def __init__(self, parent, confirm_func, order_list, dialog=None,
                 title='Checkout Confirmation'):
        """Initializes the CheckoutConfirmationDialog window
        and generates the layout for the dialog. Calls super
        class functionality
        
        @param parent: Object that represents the parent from
        which the Dialog window was called. Expected Gtk.Window
        
        @param confirm_func: Pointer to external function that
        is called when confirmation of the dialog occurs
        
        @param order_list: list of MenuItem object that represents
        the current order being considered for checkout
        """
        self.order_list = order_list
        self.tree_view = None
        self.total_row_reference = None
        self.confirm_func = confirm_func
        super(CheckoutConfirmationDialog, self).__init__(parent, title, dialog)

    def generate_layout(self):
        """Override Method.

        Generates the layout to be displayed
        in the main content area of the dialog window.

        @return: Gtk.Container that holds the necessary
        structures that are to be displayed in the content
        area of the dialog window.
        """
        main_box = Gtk.VBox()

        scroll_window = super(CheckoutConfirmationDialog, self).generate_layout()
        main_box.pack_start(scroll_window, True, True, 5)

        sub_box = self.generate_related_area()

        main_box.pack_start(sub_box, False, False, 5)

        return main_box

    def generate_related_area(self):
        """Generates the related buttons to
        be displayed beneath the generated layout
        that are associated with the functionality
        for this dialog window.

        @return: Gtk.Container that holds the
        buttons associated with the functionality
        for this dialog.
        """
        button_box = Gtk.HBox()

        left_side_box = Gtk.VBox()
        button = Gtk.Button("SPLIT CHECK")
        button.set_size_request(200, 35)
        button.connect('clicked', self._emit_dialog_response, SPLIT_CHECK_DIALOG_RESPONSE)
        left_side_box.pack_start(button, False, False, 5.0)

        button = Gtk.Button("COMP ITEM")
        button.set_size_request(200, 35)
        button.connect('clicked', self._emit_dialog_response, COMP_DIALOG_RESPONSE)
        left_side_box.pack_start(button, False, False, 5.0)

        button = Gtk.Button("ADD DISCOUNT")
        button.set_size_request(200, 35)
        button.connect('clicked', self._emit_dialog_response, DISCOUNT_DIALOG_RESPONSE)
        left_side_box.pack_start(button, False, False, 5.0)

        button_box.pack_start(left_side_box, False, False, 5.0)

        right_side_box = Gtk.VBox()

        button = Gtk.Button('Print Check')
        button.set_size_request(200, 35)
        button.connect('clicked', self._emit_dialog_response, PRINT_DIALOG_RESPONSE)
        right_side_box.pack_start(button, False, False, 0)

        button_box.pack_end(right_side_box, False, False, 0.0)

        return button_box

    def generate_columns(self):
        """Generates the columns used to
        establish the format of the display.
        
        @return: list of Gtk.TreeViewColumn
        that will be used to populate a
        Gtk.TreeView and display the 
        appropriate data.
        """
        column_list = []
        
        renderer1 = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn('MenuItem', renderer1,
                                  text=0, sensitive=2)
        column_list.append(col1)
        
        renderer2 = Gtk.CellRendererText()
        col2 = Gtk.TreeViewColumn('Price', renderer2,
                                  text=1, sensitive=2)
        column_list.append(col2)
        
        return column_list

    def generate_model(self):
        """Generates the Gtk.TreeModel
        that will be used to store the
        displayed data. This method further
        populates the Gtk.TreeModel with 
        data from the order_list
        
        @return: Gtk.TreeModel representing
        the data to be displayed
        """
        tree_model = Gtk.TreeStore(str, str, bool)
        self.update_items(self.order_list, model=tree_model)
        return tree_model

    def remove_selected_item(self, *args):
        """Removes the selected MenuItem
        from the display and the list.

        @param args: wildcard catchall that is
        used to catch the Gtk.Widget that called
        this method.

        @return: MenuItem object that was removed.
        """
        model, itr = self.get_selected()
        if itr:
            path = model.get_path(itr)
            index = path.get_indices()[0]
            menu_item = self.order_list[index]

            if not path == self.total_row_reference.get_path() and not menu_item.is_locked():
                model.remove(itr)
                self.order_list.pop(index)
                self._update_check_total(-1 * menu_item.get_price())

    def add_new_menu_item(self, menu_item):
        """Adds the given MenuItem object to
        the stored order_list and the checkout
        display.

        @param menu_item: MenuItem object that
        is to be added to the order and display.

        @return: None
        """
        self.order_list.append(menu_item)

        name = menu_item.get_name()
        price = menu_item.get_price()

        model = self.tree_view.get_model()
        added_itr = model.append(None, (name, str(price), True))
        self._check_row_changed(added_itr)

    def _emit_dialog_response(self, widget, response_type):
        """Private Method.

        Called when a button is pressed that
        causes a new dialog window to be opened.
        This method emits the signal to notify
        whatever program called this dialog that
        it requires a different type of dialog window.

        @param widget: Gtk.Widget that called this
        method.

        @param response_type: int representing
        the associated response type constant that
        is associated with which dialog response
        should be emitted.

        @return: None
        """
        self.dialog.response(response_type)
        self.dialog.destroy()

    def confirm_data(self):
        """Callback Method. Called when confirmation
        occurs

        @return: int representing Gtk.ResponseType
        that was emitted by the closing dialog window.
        """
        self.confirm_func((self.order_list,))
    
    def _check_row_changed(self, added_itr=None):
        """Callback Method. Designed to be called
        when the given Gtk.TreeView has had a row
        change.

        @param added_itr: Gtk.TreeIter pointing to
        the row changed.

        @return: None
        """
        model = self.tree_view.get_model()
        total = CheckOperations.get_order_subtotal(self.order_list)
        
        path = self.total_row_reference.get_path()
        itr = model.get_iter(path)
        
        model[itr][1] = str(total)
        
        if added_itr != None:
            model.swap(added_itr, itr)

    def _update_check_total(self, price):
        """Private Method.

        Updates the total associated with the check.

        @param price: float value to be added to the
        total of the given check.

        @return: Gtk.TreeIter pointing to the location
        of the total.
        """
        model = self.total_row_reference.get_model()
        path = self.total_row_reference.get_path()
        itr = model.get_iter(path)

        previous_total = float(model[itr][1])
        value = previous_total + price

        if int(value * 100) <= 0:
            value = 0.0

        model[itr][1] = str(value)

        return itr

    def get_selected(self):
        """Override Method.

        Gets the selected rows from the main tree view

        @return: 2-tuple (Gtk.TreeModel, list of Gtk.TreePaths)
        where the Gtk.TreeModel is the model associated with
        the tree_view and the Gtk.TreePaths are the paths that
        were selected.
        """

        selection = self.tree_view.get_selection()

        if selection.get_mode() == Gtk.SelectionMode.MULTIPLE:
            model, paths = selection.get_selected_rows()

            total_path = self.total_row_reference.get_path()

            if total_path in paths:
                paths.remove(total_path)

            return model, paths
        else:
            return super(CheckoutConfirmationDialog, self).get_selected()

    def update_items(self, order_list, model=None):
        """Clears and populates the associated model
        with the given order list.

        @param order_list: list of MenuItem objects that
        is to be displayed in the associated model.

        @keyword model: Gtk.TreeModel subclass that represents
        the model that is associated with the self.tree_view
        attribute. This keyword argument exists to allow
        populating a model that isn't associated with the
        the given tree view before it has been created. Whatever
        model is given via this keyword will be the one updated.
        Default updates the currently stored self.tree_view's
        model.

        @return: None
        """
        self.order_list = order_list

        if not model:
            model = self.tree_view.get_model()
            model.clear()

        for menu_item in order_list:
            name = menu_item.get_name()
            price = menu_item.get_price()

            location = model.append(None, (name, str(price), True))

            if menu_item.has_options():
                for option in menu_item.options:
                    option_name = option.get_option_relation() + ": " + \
                                  option.get_name()
                    option_price = option.get_price()
                    data = option_name, str(option_price), True

                    model.append(location, data)

        itr = model.append(None, ('Sub-Total',
                            str(CheckOperations.get_order_subtotal(order_list)), False))
        self.total_row_reference = Gtk.TreeRowReference.new(model, model.get_path(itr))

    def select_all(self, *args):
        """ Selects all items associated with the
        tree_view generated by this object. Adheres
        to selection function requirements.

        @param args: wildcard catchall to catch
        any Gtk.Widget using this as callback.

        @return: None
        """
        selection = self.tree_view.get_selection()
        selection.select_all()


class OrderSelectionConfirmationDialog(ConfirmationDialog):
    """OrderSelectionConfirmation window displays the current
    OrderSelection list for the user. The dialog is displayed
    when the run_dialog method is invoked. This allows
    for the user to select the OrderSelection order to be displayed.

    @var name_list: list of 3-tuples that represents the
    current OrderSelection orders

    @var name_entry: Gtk.Entry that is the area for users
    to input a new name to be added.

    @var number_entry: Gtk.Entry that is the area for users
    to input a new number associated with a name.

    @var model: Gtk.TreeModel that represents the model
    associated with the display.

    @var confirm_func: external function pointer to be
    called at confirmation.

    @var order: The current order to be confirmed or
    submitted.

    @var NUM_OF_EXTERIOR_TABLES: int representing the number
    of tables that are on the exterior, and are to be displayed.

    @var NUM_OF_COUNTER_SPACES: int representing the number of
    spaces that are on the counter, and are to be displayed.
    """
    def __init__(self, parent, confirm_func, name_list,
                 num_of_exterior_tables=4, num_of_counter_spaces=4):
        """Initializes a new OrderSelectionConfirmationDialog window.

        @param parent: subclass of Gtk.Window that the
        Dialog will be a child of.

        @param confirm_func: function pointer that is to be
        called when the dialog window has been confirmed.

        @param name_list: list of 3-tuples representing the
        names on the OrderSelection list. This tuple is of (str, str, str)
        where each entry represents the (name, number, time) that
        the order was placed.

        @keyword num_of_exterior_tables: int representing the number
        of tables in the exterior that are to be accounted for. Default
        value is 4.

        @keyword num_of_counter_spaces: int representing the number
        of counter spaces that are to be accounted for. Default value
        is 4.
        """
        self.NUM_OF_EXTERIOR_TABLES = int(num_of_exterior_tables)
        self.NUM_OF_COUNTER_SPACES = int(num_of_counter_spaces)

        self.order = None

        self.confirm_func = confirm_func
        self.name_list = name_list
        self.name_entry = None
        self.number_entry = None
        self.model = None
        super(OrderSelectionConfirmationDialog, self).__init__(parent,
                                                     'To Go Selection')

    def generate_layout(self):
        """Generates the layout for the dialog window.

        @return: Gtk.VBox representing the box to be
        added to the content area of the dialog window.
        """
        main_box = Gtk.HBox()

        table_box = Gtk.VBox()

        table_sub_box1 = Gtk.VBox()

        for x in range(0, self.NUM_OF_EXTERIOR_TABLES):
            button = Gtk.Button("Ext Table " + str(x + 1))
            button.set_size_request(100, 20)
            button.connect("clicked", self.table_button_clicked,
                            button.get_label())
            button.set_focus_on_click(False)
            button.set_can_focus(False)
            table_sub_box1.pack_start(button, True, True, 0.5)

        table_box.pack_start(table_sub_box1, True, True, 10)

        table_sub_box2 = Gtk.VBox()

        for x in range(0, self.NUM_OF_COUNTER_SPACES):
            button = Gtk.Button("Counter " + str(x + 1))
            button.set_size_request(100, 20)
            button.connect("clicked", self.table_button_clicked,
                           button.get_label())
            button.set_focus_on_click(False)
            button.set_can_focus(False)
            table_sub_box2.pack_start(button, True, True, 0.5)

        table_box.pack_start(table_sub_box2, True, True, 10)

        main_box.pack_start(table_box, False, False, 10)

        right_box = Gtk.VBox()
        scrolled_window = super(OrderSelectionConfirmationDialog,
                                self).generate_layout()
        right_box.pack_start(scrolled_window, True, True, 5)

        name_label = Gtk.Label('NAME: ')
        number_label = Gtk.Label('NUMBER: ')

        sub_box = Gtk.HBox()
        sub_box.set_homogeneous(True)
        sub_box.pack_start(name_label, True, True, 5)
        sub_box.pack_start(number_label, True, True, 5)

        right_box.pack_start(sub_box, False, False, 5)

        self.name_entry = Gtk.Entry()
        self.number_entry = Gtk.Entry()

        sub_box = Gtk.HBox()
        sub_box.set_homogeneous(True)
        sub_box.pack_start(self.name_entry, True, True, 5)
        sub_box.pack_start(self.number_entry, True, True, 5)

        right_box.pack_start(sub_box, False, False, 5)

        add_new_button = Gtk.Button('Add')
        add_new_button.set_size_request(150, 50)
        add_new_button.connect('clicked', self.add_new_order)

        sub_box = Gtk.HBox()
        sub_box.set_homogeneous(True)
        sub_box.pack_start(add_new_button, True, True, 5)
        sub_box.pack_start(Gtk.Fixed(), True, True, 5)
        sub_box.pack_start(Gtk.Fixed(), True, True, 5)

        right_box.pack_start(sub_box, False, False, 5)
        main_box.pack_start(right_box, True, True, 5)

        self.name_entry.grab_focus()

        return main_box

    def generate_columns(self):
        """Generates the columns to be
        displayed in the TreeView displayed in
        the content area.

        @return: list of Gtk.TreeViewColumns that
        represents the columns to be added to the
        TreeView displayed.
        """
        col_list = []

        rend = Gtk.CellRendererText()
        column1 = Gtk.TreeViewColumn('Name: ', rend, text=0)
        col_list.append(column1)

        column2 = Gtk.TreeViewColumn('Number: ', rend, text=1)
        col_list.append(column2)

        column3 = Gtk.TreeViewColumn('Time of Order: ', rend, text=2)
        col_list.append(column3)

        return col_list

    def generate_model(self):
        """Generates the model for the display. The
        model stores 3 strings that are derived from
        each entry in the name_list entries.

        @return: Gtk.TreeModel representing the
        store for the display.
        """
        self.model = Gtk.ListStore(str, str, str)

        if self.name_list is not None:
            for name, number, order_time in self.name_list:
                self.model.append((name, number, order_time.ctime()))

        return self.model

    def add_new_order(self, *args):
        """Callback Method that is called when
        the add new order button is clicked.

        @param *args: wildcard that represents a
        catch all. The first argument is the
        widget that emitted the signal
        """
        name = self.name_entry.get_text().strip()
        number = self.number_entry.get_text().strip()

        non_repeat = True

        itr = self.model.get_iter_first()

        while itr and non_repeat:

            stored_name, stored_number, _ = self.model[itr]
            if stored_name == name and stored_number == number:
                message_title = 'Invalid name and number selected!'
                message = '\nYou have selected an invalid name and number ' \
                          'combination. This current selection is invalid ' \
                          'because there already exists an order under that ' \
                          'exact name and number combination. \n\n To continue ' \
                          'please choose a valid name and number combination!'
                run_warning_dialog(self.dialog, message_title, message)

                non_repeat = False

            itr = self.model.iter_next(itr)

        if len(name) > 0 and len(number) > 0 and non_repeat:
            time = datetime.now().strftime(CTIME_STR)
            time = datetime.strptime(time, CTIME_STR)
            new_order = (name, number, time)

            self.confirm_button_clicked(None, order=new_order)

    def table_button_clicked(self, button, table):
        """Callback Method that is called when
        a table button has been clicked. This
        method closes the dialog

        @param button: Gtk.widget that called this
        method.

        @param table: str representing the table
        representing the button pressed.

        @return: None
        """
        self.confirm_button_clicked(None, order=table)

    def get_selected(self, *args):
        """Gets the selected order in the standard
        3-tuple form.

        @param *args: wildcard that represents the
        widget that called this method.

        @return: 3-tuple of (str, str, str) representing
        the (name, number, and time) of the order.
        """
        tree_selection = self.tree_view.get_selection()
        model, itr = tree_selection.get_selected()

        if itr:
            name, number, display_time = model[itr]
            return name, number, datetime.strptime(display_time, CTIME_STR)

        return None

    def confirm_button_clicked(self, widget, order=None):
        """Override method

        Callback method. Called when Confirm button
        is clicked. This method confirms the
        currently selected order.

        @param args: wildcard catchall used to catch
        the Gtk.Widget that called this method.

        @return: None
        """
        if order:
            self.order = order
        else:
            self.order = self.get_selected()

        if self.order:
            super(OrderSelectionConfirmationDialog, self).confirm_button_clicked()

    def confirm_data(self):
        """Override Method.

        Callback Method that is called when the confirm
        button is clicked.
        """
        self.confirm_func(self.order)


#=========================================================
# This block represents windows that form the specific
# classes that can be instantiated. All classes in this
# block represent selections that can be made.
#
# Upon confirmation each class in this block calls a
# given function that is passed into the class at
# instantiation as its "confirm func".
#
# Each class inherits from the SelectionDialog abstract
# class. SelectionDialog has three main areas, a left most
# box that is the "main_selection_area", a center box that
# is the "secondary_selection_area" and a right most box
# that is the "item_selection_area".
#=========================================================
class UndoCheckoutSelectionDialog(SelectionDialog):
    """UndoCheckoutSelectionDialog window allows for the user to
    access previously checked out orders and return them to the
    main GUI for user interactions.

    @group SelectionDialog: This class is a subclass member of the
    SelectionDialog group. As such it inherits functionality
    from the SelectionDialog super class. Any changes in the
    SelectionDialog class could effect the functionality
    of this class.

    @var name_entry: Gtk.Entry object that allows for entry of
    a name to be displayed when the checked out order is undone.

    @var orders: Orders object that allows for displaying and
    editing the associated MenuItems with an order.

    @var orders_view: Gtk.TreeView object that displays the orders
    that had previously been checked out.

    @var imported_view: Gtk.TreeView object that displays the imported
    orders that will be passed back to the UI for user interaction.

    @var confirm_func: Function that will be called upon confirmation.
    """

    def __init__(self, parent, checkout_information, confirm_func,
                 title='Undo Checkout Dialog Window'):
        """Initializes a new UndoCheckoutDialog window that allows
        the user to retrieve previously checked out orders.

        @param parent: Gtk.Object that this dialog window will be
        called upon. The parent will be frozen and unable to be
        interacted with until this dialog window is confirmed or
        canceled.

        @param checkout_information: dict where each key is a str
        representing an order previously checked out, and each
        value is a list of MenuItem objects that is associated
        with the order that was checked out.

        @param confirm_func: function that is to be called upon
        confirmation of this dialog window.

        @param title: str representing the
        """
        self.checkout_information = checkout_information
        self._prev_imports = {}
        self.orders = Orders(num_of_tables=0)

        self.name_entry = None
        self.orders_view = None
        self.imported_view = None

        self.update_label = None

        self.confirm_func = confirm_func

        super(UndoCheckoutSelectionDialog, self).__init__(parent, title,
                                                          default_size=(950, 800))

    def generate_main_selection_area(self):
        """Override Method.

        Generates the main selection area of
        the SelectionDialog window.

        @return: Gtk.Container holding the widgets
        that are to be displayed.
        """
        frame = Gtk.Frame(label='Order Selection')
        main_box = Gtk.VBox()

        scrolled_window = Gtk.ScrolledWindow()

        self.orders_view = self._generate_orders_view()
        self.orders_view.set_model(self._generate_orders_model())

        scrolled_window.add(self.orders_view)
        main_box.pack_start(scrolled_window, True, True, 5.0)

        frame.add(main_box)
        return frame

    def _generate_orders_view(self, cols=('Order Name:',
                                          'Original Checkout Date/Time')):
        """ Private Method.

        Generates the orders view column to be
        displayed in the main selection area.

        @keyword cols: tuple representing the
        column names that are to be displayed.
        Each name will be expected to have a
        matching data set under the model that
        maps directly to the index of which the
        column is displayed.

        @return: Gtk.TreeView that represents
        the column to be displayed in the main
        selection area.
        """
        orders_view = Gtk.TreeView()

        selection = orders_view.get_selection()
        selection.set_select_function(self._orders_selection_function, None)

        index = 0

        for col in cols:
            rend = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col, rend, text=index)
            orders_view.append_column(column)

            index += 1

        return orders_view

    def _generate_orders_model(self):
        """ Private method.

        Generates the orders view model that will store the
        data for displaying. Populates the model with the
        data from the checkout information.

        @return: Gtk.TreeModel that represents the model
        that will be displaying the data.
        """
        orders_model = Gtk.ListStore(str, str)

        for order_name, order_time in self.checkout_information:
            orders_model.append((order_name, order_time.ctime()))

        return orders_model

    def _orders_selection_function(self, selection, model, path, is_selected,
                                   user_data):
        """ Private Method.

        Method called when an order has been selected.

        @param selection: Gtk.TreeSelection that represents
        the selection that called this method.

        @param model: Gtk.TreeModel that represents the model
        that is displaying the data associated with this
        selection.

        @param path: Gtk.TreePath pointing to the row in the
        view that was selected.

        @param is_selected: Bool value representing if the
        column was selected prior to this current selection
        attempt.

        @param user_data: None by default.

        @return: bool representing if this column is ok to
        be accepted. True if ok, False if not.
        """
        itr = model.get_iter(path)

        name, time_str = model[itr]
        key = name, '', datetime.strptime(time_str, CTIME_STR)

        self.orders.select_togo_order(key)
        return True

    def generate_secondary_selection_area(self):
        """Override Method.

        Generates the secondary selection area.
        By default this area is left blank for
        the UndoCheckoutSelectionDialog.

        @return: Gtk.Container that is empty by
        default.
        """
        return Gtk.VBox()

    def generate_properties_selection_area(self):
        """Override Method.

        Generates the properties selection area
        of the dialog window.

        @return: Gtk.Container that holds the widgets
        that are used to display the properties selection
        area.
        """
        frame = Gtk.Frame(label='Properties Selection Area')
        main_box = Gtk.VBox()

        sub_box = Gtk.VBox()
        sub_box.pack_start(self._generate_items_display_area(), True, True, 5.0)
        main_box.pack_start(sub_box, True, True, 5.0)

        sub_box = Gtk.VBox()
        sub_box.pack_start(self._generate_import_area(), True, True, 5.0)
        main_box.pack_start(sub_box, True, True, 5.0)

        frame.add(main_box)
        return frame

    def _generate_items_display_area(self):
        """Private Method.

        Generates the item displays area. This
        utilizes the previously generated self.orders.

        Populates the orders with every key from
        checkout information that was available. Each
        key is stored in the orders as a togo order with
        the key of (str, '', datetime) representing the
        items name, a blank string and then finally the
        time represented as a datetime object.

        @return: Gtk.Container that holds the display
        view for self.orders widget.
        """
        main_box = Gtk.VBox()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.orders.get_display_view())

        main_box.pack_start(scrolled_window, True, True, 5.0)


        for order_name, order_time in self.checkout_information:
            data = self.checkout_information[order_name, order_time]
            key = (order_name, '', order_time)

            self.orders.load_new_order(key, data)

        return main_box

    def _generate_import_area(self):
        """ Private Method.

        Generates the import area to be displayed.

        @return: Gtk.Container holding all the
        Gtk.Widgets that will be displayed in
        the import area.
        """
        main_box = Gtk.VBox()
        sub_box = Gtk.HBox()
        self.name_entry = Gtk.Entry()
        sub_box.pack_start(self.name_entry, True, True, 5.0)

        import_button = Gtk.Button('Import As')
        import_button.connect('clicked', self._add_import_data)
        sub_box.pack_start(import_button, False, False, 5.0)

        main_box.pack_start(sub_box, False, False, 5.0)

        scrolled_window = Gtk.ScrolledWindow()

        self.imported_view = self._generate_imported_view()
        self.imported_view.set_model(self._generate_imported_model())

        scrolled_window.add(self.imported_view)

        main_box.pack_start(scrolled_window, True, True, 5.0)

        sub_box = Gtk.HBox()
        remove_button = Gtk.Button('Remove Import')
        remove_button.connect('clicked', self._remove_import_data)
        sub_box.pack_start(remove_button, False, False, 5.0)
        sub_box.pack_start(Gtk.Fixed(), True, True, 5.0)

        main_box.pack_start(sub_box, False, False, 5.0)

        return main_box

    def _generate_imported_view(self, cols=('Checkout Name', 'Undo as')):
        """ Private Method.

        Generates the imported view that will be used
        to display which imports will be made.

        @param cols: tuple representing the names that
        the columns should be displayed with. Each column
        will have the index of the tuple used as the index
        through which it will get its data from the model.

        @return: Gtk.TreeView that is used to display the
        imported data.
        """
        imported_view = Gtk.TreeView()

        index = 0

        for col in cols:
            rend = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col, rend, text=index)
            imported_view.append_column(column)

            index += 1

        return imported_view

    def _generate_imported_model(self):
        """Private Method.

        Generates the imported view model that is used
        to store the data to be displayed that represents
        the checkout orders name, the name it will be imported
        as and the time that is associated with it.

        @param types: tuple representing the data types the
        model should display. By default is (str, str, float)
        that represents the original name, the new name and
        the number of seconds since the epoch when it was
        ordered.

        @return: Gtk.TreeModel that stores the data to be
        displayed in the imported view.
        """
        tree_model = Gtk.ListStore(str, str, str)
        return tree_model

    def _add_import_data(self, *args):
        """ Adds the currently selected import from the
        orders view to the imported view under the
        name specified by the name entry.

        @param args: wildcard catchall used to
        catch the Gtk.Widget that called this method.

        @return: None
        """
        selection = self.orders_view.get_selection()
        view, itr = selection.get_selected()

        name = self.name_entry.get_text().strip()
        self.name_entry.set_text('')

        if itr and name and name not in self._prev_imports:
            order_name, order_time_str = view[itr]
            imported_model = self.imported_view.get_model()
            imported_model.append((order_name, name, order_time_str))

            self._prev_imports[name] = order_name, order_time_str

            view.remove(itr)

    def _remove_import_data(self, *args):
        """Removes the currently selected import
        from the imported list.

        @param args: wildcard catchall that catches
        the Gtk.Widget that called this method.

        @return: None
        """
        selection = self.imported_view.get_selection()
        view, itr = selection.get_selected()

        if itr:
            name = view[itr][1]
            view.remove(itr)

            self._update_order(self._prev_imports[name])
            self._clear_prev_import(name)

    def _update_order(self, data):
        model = self.orders_view.get_model()
        model.append(data)

    def _clear_prev_import(self, name):
        del self._prev_imports[name]

    def confirm_data(self, *args):
        """Override Method.

        Confirms the selected data and sends
        it to the confirm function.

        @param args: wildcard catchall that
        represents the Gtk.Widget that called
        this method.

        @return: None
        """
        imported_data = {}
        undone_checkout_keys = []

        for order_name, name, order_time_str in self.imported_view.get_model():
            order_time = datetime.strptime(order_time_str, CTIME_STR)
            order_data = self.checkout_information[order_name, order_time]

            # Normalize the datetime now allow for accuracy between stored
            # datetimes.
            curr_time = datetime.strptime(datetime.now().ctime(), CTIME_STR)

            imported_data[name, UNDONE_CHECKOUT_SEPARATOR, curr_time] = order_data

            undone_checkout_keys.append((order_name, order_time, name))

        self.confirm_func(imported_data, undone_checkout_keys)


class UpdateMenuItemsDialog(SelectionDialog):
    """UpdateMenuItemDialog interacts with the user
    to display information and receive information to
    update the stored menu item data for the PeonOrderSystem
    UI.

    This window expects menu item data to be in a specific
    form. It then operates on that menu item data, finally
    calling the given confirm func upon confirmation from
    the user.

    @group SelectionDialog: This class is a member of the SelectionDialog
    group and as such it inherits its functionality from the SelectionDialog
    class. Any changes to the SelectionDialog class could alter the
    functionality of this class.

    @warning: This dialog window relies on GeneralOptionSelectionDialog
    when editing options. Changes in the functionality of
    GeneralOptionSelectionDialog may effect the functionality in this
    class.

    @var menu_item_data: dict of str key to list of MenuItem object
    values. Each key represents a category and each list is a
    list of MenuItem objects that represents that category.

    @var confirm_func: function that is to be called if or when
    the dialog window has been confirmed by the user.

    @var model_data: dict of str key to list of Gtk.TreeModel
    objects. This represents the associated MenuItems to be
    displayed for any given category. This information will
    be edited throughout the classes function, and if confirmation
    occurs this dict will be changed to MenuItem objects and
    then passed to the confirm_func.

    @var categories_name_entry: Gtk.Entry that represents the
    text entry that is used to add a new category with the
    entered name.

    @var item_name_entry: Gtk.Entry that represents the text
    entry that is used to edit the name associated with
    a specific MenuItem object.

    @var price_spin_button: Gtk.SpinButton that represents
    the edited price associated with a specific MenuItem object.

    @var stars_spin_button: Gtk.SpinButton that represents
    the edited stars associated with a specific MenuItem object.

    @var is_editable_switch: Gtk.Switch that is associated with
    editing the associated MenuItem's editable bool value.

    @var is_confirmed_switch: Gtk.Switch that is associated with
    editing the associated MenuItem's confirmed bool value.

    @var categories_view: Gtk.TreeView object that displays
    the information of the categories to be selected and
    edited by the user.

    @var menu_view: Gtk.TreeView object that is used to
    display the information of the MenuItem objects to
    be selected and editing by the user.
    """

    def __init__(self, parent, menu_item_data, option_item_data, confirm_func,
                 title='Update Menu Items Dialog'):
        """ Initializes a new UpdateMenuItemsDialog window
        that will allow the user to interact with the stored
        menu data and alter it as necessary.

        @param parent: Gtk.Object that represents the parent
        on which this dialog object was called.

        @param menu_item_data: dict of str keys that map to
        list values. Each key is a category that stores a list
        of MenuItem objects associated with menu data that is
        stored.

        @param option_item_data: dict of str keys that represent
        categories that map to list of OptionItems that represent
        the options for those categories.

        @param confirm_func: function that is to be called upon
        confirmation.

        @param title: str representing the title to be displayed
        by this dialog window.
        """
        self.menu_item_data = menu_item_data
        self.option_item_data = option_item_data
        self.confirm_func = confirm_func
        self.model_data = {}

        self.categories_name_entry = None
        self.item_name_entry = None
        self.price_spin_button = None
        self.stars_spin_button = None

        self.is_editable_switch = None
        self.is_confirmed_switch = None

        self.categories_view = None
        self.item_view = None
        self.options_view = None

        super(UpdateMenuItemsDialog, self).__init__(parent, title,
                                                    default_size=(100, 600))

    def generate_main_selection_area(self):
        """Generates the area associated
        with the categories section.

        @return: Gtk.Container that holds all the
        associated Gtk.Widgets that are to be
        displayed.
        """

        # Generate information for displaying
        # and editing categories
        categories_box = Gtk.VBox()

        # Generate categories tree view
        view_frame = Gtk.Frame()
        categories_display_box = Gtk.VBox()
        scroll_window = Gtk.ScrolledWindow()

        self.categories_view = self.generate_categories_view()
        scroll_window.add(self.categories_view)
        categories_display_box.pack_start(scroll_window, True, True, 5.0)

        view_frame.add(categories_display_box)
        categories_box.pack_start(view_frame, True, True, 5.0)

        # Generate categories editing buttons
        categories_frame = Gtk.Frame(label="Category Editor")
        categories_edit_box = Gtk.VBox()

        categories_edit_subbox1 = Gtk.HBox()

        self.categories_name_entry = Gtk.Entry()
        categories_edit_subbox1.pack_start(self.categories_name_entry, False, False,
                                           5.0)
        add_category_button = Gtk.Button("ADD")
        add_category_button.connect('clicked', self.add_new_category)
        add_category_button.set_can_focus(False)
        add_category_button.set_size_request(70, 30)
        categories_edit_subbox1.pack_start(add_category_button, False, False, 5.0)

        categories_edit_box.pack_start(categories_edit_subbox1, False, False, 5.0)

        categories_edit_subbox2 = Gtk.HBox()

        remove_category_button = Gtk.Button("REMOVE SELECTED CATEGORY")
        remove_category_button.connect('clicked', self.remove_selected_category)
        remove_category_button.set_can_focus(False)
        remove_category_button.set_size_request(150, 50)
        categories_edit_subbox2.pack_start(remove_category_button, False, False,
                                           5.0)

        categories_edit_box.pack_start(categories_edit_subbox2, False, False, 5.0)
        categories_frame.add(categories_edit_box)
        categories_box.pack_start(categories_frame, False, False, 5.0)

        return categories_box

    def generate_categories_view(self):
        """Generates the categories view associated
        with displaying the data of categories in
        menu data.

        @return: Gtk.TreeView that represents the
        view that will display the category data.
        """
        tree_view = Gtk.TreeView()

        selection = tree_view.get_selection()
        selection.connect('changed', tree_view_changed, tree_view)

        model = self.generate_categories_model()
        tree_view.set_model(model)

        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Category', rend, text=0)
        tree_view.append_column(col)

        selection = tree_view.get_selection()
        selection.set_select_function(self.category_selected, None)

        return tree_view

    def generate_categories_model(self):
        """Generates and populates the model
        that is associated with displaying the
        categories of the menu data.

        @return: None
        """
        model = Gtk.ListStore(str)

        for category in self.menu_item_data:
            model.append((str(category),))

        return model

    def set_category_selection(self, itr):
        """Sets the current selection displayed
        in the category view to the given iter
        displayed in the category view.

        @param itr: Gtk.TreeIter pointing to a row
        displayed in the categories_view

        @return: None
        """
        if itr:
            selection = self.categories_view.get_selection()
            selection.select_iter(itr)

    def category_selected(self, selection, model, path,
                              is_selected, user_data):
        """Callback Method.

        This method is called when a selection has been
        made in the associated category view. Selections
        made populate the items view with the associated
        model to display MenuItems for selection.

        @param selection: Gtk.Selection that represents
        the selection associated with the treeview

        @param model: Gtk.TreeModel that stores the data
        displayed in the associated treeview

        @param path: Gtk.TreePath pointing to a row in the
        associated treeview

        @param is_selected: bool value that represents if
        the row was selected prior to this current selection.

        @param user_data: user defined arguments passed into
        this selection method. Expected None.

        @return: bool value, default is True
        """
        itr = model.get_iter(path)
        key = model[itr][0]

        category_model = self.model_data[key]

        self.item_view.set_model(category_model)

        self.item_name_entry.set_text('')
        self.item_name_entry.set_sensitive(False)

        self.price_spin_button.set_value(0.0)
        self.price_spin_button.set_sensitive(False)

        self.stars_spin_button.set_value(0)
        self.stars_spin_button.set_sensitive(False)

        self.is_confirmed_switch.set_active(False)
        self.is_confirmed_switch.set_sensitive(False)

        self.is_editable_switch.set_active(False)
        self.is_editable_switch.set_sensitive(False)

        return True

    def get_selected_category(self):
        """Gets the model and itr associated
        with the currently selected row in
        the categories_view

        @return: tuple (Gtk.TreeModel, Gtk.TreeIter)
        representing the model that stores the data
        and an iter point to the current selected row
        respectively.
        """
        selection = self.categories_view.get_selection()
        return selection.get_selected()

    def _get_selected_category_list(self):
        """Private Method.

        Gets the currently selected list
        of MenuItems associated with the
        selected category.

        @return: list of MenuItem objects
        that represent the current category
        list that is being edited.
        """
        model, itr = self.get_selected_category()
        if itr:
            category = model[itr][0]

            return self.menu_item_data[category]

    def add_new_category(self, *args):
        """Adds a new category to the menu data.
        Information for the displayed name of the
        category is pulled from the associated
        text entry.

        @note: If text entry is either empty or
        contains only white space then this method
        doesn't add any new category.

        @param args:wildcard catchall that is used to
        catch the Gtk.Widget that called this method.

        @return: None
        """
        text = self.categories_name_entry.get_text()
        text = text.strip().upper()

        self.categories_name_entry.set_text('')

        if text and text not in self.model_data:
            model = self.categories_view.get_model()

            new_model = Gtk.ListStore(str, float)
            self.model_data[text] = new_model
            self.menu_item_data[text] = []

            new_itr = model.append((text, ))
            self.set_category_selection(new_itr)

    def remove_selected_category(self, *args):
        """Removed the selected category from the
        data.

        @note: If this method is called and the selected
        category has an associated model with a non-zero
        length of MenuItems then this method will initiate
        a warning dialog before deletion.

        @param args: wildcard catchall that is used to
        catch the Gtk.Widget that called this method.

        @return: None
        """
        selection = self.categories_view.get_selection()
        model, itr = selection.get_selected()
        key = model[itr][0]

        if itr:
            response = True

            if len(self.model_data[key]) > 0:
                title = 'Removing ' + key + \
                        ' will delete all associated Menu Items'
                message = 'If you remove the category ' + key + \
                          ' all Menu Items contained' + \
                          ' within this category will also be deleted. ' + \
                          ' This cannot be undone!\n\nDo you want to continue?'
                response = run_warning_dialog(self.dialog, title, message)

            if response:
                model.remove(itr)
                del self.model_data[key]
                del self.menu_item_data[key]

    def generate_secondary_selection_area(self):
        """Generates the area associated
        with the items section.

        @return: Gtk.Container that holds all
        the associated Gtk.Widgets that are
        associated with the items section
        display.
        """
        menu_items_display_box = Gtk.VBox()

        view_frame = Gtk.Frame()
        scroll_window = Gtk.ScrolledWindow()

        self.item_view = self.generate_item_view()

        scroll_window.add(self.item_view)
        view_frame.add(scroll_window)

        menu_items_display_box.pack_start(view_frame, True, True, 5.0)

        menu_items_edit_frame = Gtk.Frame(label='Menu Item Editor')
        menu_items_edit_box = Gtk.HBox()

        add_menu_item_button = Gtk.Button('ADD NEW ITEM')
        add_menu_item_button.connect('clicked', self.add_new_item)
        add_menu_item_button.set_can_focus(False)
        add_menu_item_button.set_size_request(100, 50)
        menu_items_edit_box.pack_start(add_menu_item_button, False, False, 5.0)

        remove_menu_item_button = Gtk.Button('REMOVE ITEM')
        remove_menu_item_button.connect('clicked',
                                        self.remove_selected_item)
        remove_menu_item_button.set_can_focus(False)
        remove_menu_item_button.set_size_request(100, 50)
        menu_items_edit_box.pack_end(remove_menu_item_button, False, False, 5.0)

        menu_items_edit_frame.add(menu_items_edit_box)

        menu_items_display_box.pack_start(menu_items_edit_frame, False, False, 5.0)

        return menu_items_display_box

    def generate_item_view(self):
        """Generates the item view to display
        the MenuItem information.

        @return: Gtk.TreeView associated with
        the item view generated.
        """
        tree_view = Gtk.TreeView()

        selection = tree_view.get_selection()
        selection.connect('changed', tree_view_changed, tree_view)

        self.generate_item_model()

        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Menu Item', rend, text=0)
        tree_view.append_column(col)

        selection = tree_view.get_selection()
        selection.set_select_function(self.item_selected, None)

        return tree_view

    def generate_item_model(self):
        """Generates and populates the
        models to display the items
        associated with each category.

        @return: None
        """
        for category in self.menu_item_data:
            model = Gtk.ListStore(str, float)

            for menu_item in self.menu_item_data[category]:
                name = menu_item._name
                price = menu_item._price

                values = name, price
                model.append(values)

            self.model_data[category] = model

    def set_item_selection(self, itr):
        """Sets the iter pointing to a row
        displayed by the items view.

        @param itr: Gtk.TreeIter pointing
        to a row being displayed by the
        items view.

        @return: None
        """
        if itr:
            selection = self.item_view.get_selection()
            selection.select_iter(itr)

    def item_selected(self, selection, model, path,
                          is_selected, user_data):
        """Callback Method.

        This method is called when the a selection from
        the items_view is selected. This method displays
        the properties of the associated MenuItem in the
        properties area for editing.

        @param selection: Gtk.Selection of the treeview
        that has been selected.

        @param model: Gtk.TreeModel of the treeview that
        has been selected.

        @param path: Gtk.TreePath of the selected row in
        the treeview

        @param is_selected: bool value representing if the
        row was selected, or unselected. This occurs prior
        to selection. So if a row is true, it was previously
        selected and clicked again.

        @param user_data: arguments passed into the selected
        function as designated by the user. Expected value is
        None

        @return: bool value, by default is True
        """
        if not is_selected:
            itr = model.get_iter(path)
            menu_item = self._get_selected_menu_item(item_itr=itr)

            name = menu_item.get_name()
            price = menu_item.get_price()
            stars = menu_item.stars
            editable = menu_item.editable
            confirmed = menu_item.confirmed

            self.item_name_entry.set_text(name)
            self.item_name_entry.set_sensitive(True)

            self.price_spin_button.set_value(price)
            self.price_spin_button.set_sensitive(True)

            self.stars_spin_button.set_value(stars)
            self.stars_spin_button.set_sensitive(editable)

            self.is_editable_switch.set_active(editable)
            self.is_editable_switch.set_sensitive(True)

            self.is_confirmed_switch.set_active(not confirmed)
            self.is_confirmed_switch.set_sensitive(True)

            self.update_options_view(menu_item)

        return True

    def get_selected_item(self, *args):
        """Gets the selected model and iter
        representing the data storage and
        row in storage pointed at by the
        current row selected.

        @param args: wildcard catchall to
        catch the Gtk.Widget that called
        this method.

        @return: tuple (Gtk.TreeModel, Gtk.TreeIter)
        that represent hte stored data model and the
        iter pointing to the row respectively.
        """
        selection = self.item_view.get_selection()
        return selection.get_selected()

    def add_new_item(self, *args):
        """Adds a new MenuItem to the
        menu data. This MenuItem is stored
        with a generic name, and trivial
        properties.

        @param args: wildcard catchall that
        is used to catch the Gtk.Widget that
        called this method.

        @return: None
        """
        item_list = self._get_selected_category_list()

        new_menu_item = MenuItem('NEW MENU ITEM', 0.0, 0, False, False)
        item_list.append(new_menu_item)

        name = new_menu_item.get_name()
        price = new_menu_item.get_price()

        model = self.item_view.get_model()
        data = (name, price)
        new_itr = model.append(data)

        self.set_item_selection(new_itr)

    def remove_selected_item(self, *args):
        """Removes the selected menu item from
        the menu data.

        @param args: wildcard catchall that is
        used to catch the Gtk.Widget that called
        this method.

        @note: This method will only remove a MenuItem,
        if a MenuItem is selected.

        @return: None
        """
        menu_list = self._get_selected_category_list()

        selection = self.item_view.get_selection()
        model, itr = selection.get_selected()

        if itr:
            path = model.get_path(itr)
            index = path.get_indices()[0]

            menu_list.pop(index)
            model.remove(itr)

    def generate_properties_selection_area(self):
        """Generates the area associated
        with the properties editing area.

        @return: Gtk.Container that holds
        all Gtk.Widgets that are associated
        with the properties area display.
        """
        options_box = Gtk.VBox()

        properties_frame = Gtk.Frame(label='Item Properties')
        properties_box = Gtk.VBox()

        name_box = Gtk.HBox()
        name_box.pack_start(Gtk.Label("Name: "), False, False, 5.0)
        self.item_name_entry = Gtk.Entry()
        name_box.pack_start(self.item_name_entry, True, True, 5.0)
        properties_box.pack_start(name_box, False, False, 5.0)

        price_box = Gtk.HBox()
        price_box.pack_start(Gtk.Label("Price: "), False, False, 5.0)
        self.price_spin_button = Gtk.SpinButton()
        self.price_spin_button.set_digits(2)
        adjustment = Gtk.Adjustment(0.0, 0, 100**10, .01, 1, 1)
        self.price_spin_button.set_adjustment(adjustment)
        price_box.pack_start(self.price_spin_button, True, True, 5.0)
        price_box.pack_start(Gtk.Fixed(), True, True, 5.0)
        properties_box.pack_start(price_box, False, False, 5.0)

        stars_box = Gtk.HBox()
        stars_box.pack_start(Gtk.Label("Initial Stars\nValue:"), False, False, 5.0)
        self.stars_spin_button = Gtk.SpinButton()
        adjustment = Gtk.Adjustment(0, -100, 100, 1, 1, 1)
        self.stars_spin_button.set_adjustment(adjustment)
        stars_box.pack_start(self.stars_spin_button, False, False, 5.0)
        properties_box.pack_start(stars_box, False, False, 5.0)

        editable_box = Gtk.HBox()
        editable_box.pack_start(Gtk.Label('Can be\nedited: '), False, False, 5.0)
        self.is_editable_switch = Gtk.Switch()
        self.is_editable_switch.connect('button-press-event', self.toggle_stars_editable_display)
        editable_box.pack_start(Gtk.Fixed(), False, False, 5.0)
        editable_box.pack_start(self.is_editable_switch, False, False, 5.0)
        properties_box.pack_start(editable_box, False, False, 5.0)

        confirmed_box = Gtk.HBox()
        confirmed_box.pack_start(Gtk.Label('Can be sent\nto kitchen: '), False, False, 5.0)
        self.is_confirmed_switch = Gtk.Switch()
        confirmed_box.pack_start(Gtk.Fixed(), False, False, 5.0)
        confirmed_box.pack_start(self.is_confirmed_switch, False, False, 5.0)
        properties_box.pack_start(confirmed_box, False, False, 5.0)

        update_changes_box = Gtk.HBox()
        update_changes_button = Gtk.Button('Update Item')
        update_changes_button.connect('clicked', self.update_item_properties)
        update_changes_button.set_size_request(150, 35)
        update_changes_button.set_can_focus(False)
        update_changes_box.pack_end(update_changes_button, False, False, 5.0)
        properties_box.pack_end(update_changes_box, False, False, 5.0)

        properties_frame.add(properties_box)
        options_box.pack_start(properties_frame, False, False, 5.0)

        option_choices_box = Gtk.VBox()

        option_display = self.generate_options_view()
        option_choices_box.pack_end(option_display, True, True, 5.0)

        options_box.pack_end(option_choices_box, True, True, 5.0)

        return options_box

    def generate_options_view(self):
        """Generates the options view display.

        @return: Gtk.Container that holds the
        options view display and
        """
        options_frame = Gtk.Frame()
        main_box = Gtk.VBox()

        scroll_window = Gtk.ScrolledWindow()

        model = Gtk.ListStore(str, str)
        self.options_view = Gtk.TreeView(model)

        rend = Gtk.CellRendererText()

        col1 = Gtk.TreeViewColumn('Option Name: ', rend, text=0)
        self.options_view.append_column(col1)

        col2 = Gtk.TreeViewColumn('Cost: ', rend, text=1)
        self.options_view.append_column(col2)

        scroll_window.add(self.options_view)
        main_box.pack_start(scroll_window, True, True, 5.0)

        button_box = Gtk.HBox()

        edit_options_button = Gtk.Button('EDIT OPTIONS')
        edit_options_button.set_size_request(150, 35)
        edit_options_button.set_can_focus(False)
        edit_options_button.connect('clicked', self.edit_options)
        button_box.pack_end(edit_options_button, False, False, 5.0)

        main_box.pack_end(button_box, False, False, 5.0)
        options_frame.add(main_box)
        return options_frame

    def edit_options(self, *args):
        """Opens a new dialog window to edit
        the current frequent options associated
        with the selected MenuItem.

        @warning: Opens a new GeneralOptionSelectionDialog
        that allows the user to edit the items associated
        with this order.

        @return: list of OptionItems that has been added
        to the given MenuItem.
        """
        menu_item = self._get_selected_menu_item()
        menu_item.options = menu_item._option_choices
        menu_item._option_choices = []
        new_dialog = GeneralOptionSelectionDialog(self.dialog,
                                                  self.option_item_data,
                                                  menu_item)
        response = new_dialog.run_dialog()
        menu_item._option_choices = list(set(menu_item.options))
        menu_item.options = []

        self.update_options_view(menu_item)

        return menu_item.get_option_choices()

    def update_options_view(self, menu_item):
        """Updates the options view that displays
        the options on a given menu item. This method
        clears the current model and reloads it with
        the given MenuItems possible option choices.

        @param menu_item: MenuItem that is to have
        its option choices displayed in the given
        area.

        @return: return Gtk.TreeModel that was edited.
        """
        if menu_item:
            option_choices = menu_item.get_option_choices()

            model = self.options_view.get_model()
            model.clear()

            for option in option_choices:
                name = option.get_name()
                price = option.get_price()

                data = str(name), str(price)
                model.append(data)

            return model

    def update_item_properties(self, *args):
        """Updates the item properties that has been
        selected by the item view and has had
        its properties edited in the property
        editing area.

        @param args: wildcard catchall that is
        used to catch the Gtk.Widget that called
        this method.

        @return: None
        """
        selection = self.item_view.get_selection()
        model, itr = selection.get_selected()

        name = self.item_name_entry.get_text()
        if len(name) > 0 and self.item_name_entry.is_sensitive():
            name = name.upper()

            price = self.price_spin_button.get_value()
            stars = self.stars_spin_button.get_value_as_int()
            editable = self.is_editable_switch.get_active()
            confirmed = not self.is_confirmed_switch.get_active()

            menu_item = self._get_selected_menu_item(item_itr=itr)

            menu_item._name = name
            model[itr][0] = name

            menu_item._price = price
            model[itr][1] = price

            menu_item.stars = stars
            menu_item._default_stars = stars
            menu_item.editable = editable
            menu_item.confirmed = confirmed

    def _get_selected_menu_item(self, item_itr=None):
        """Private Method.

        Gets the currently selected MenuItem
        that is represented under the category
        and selected by the item view.

        @param args: wildcard catchall that
        catches the Gtk.Widget that called
        this method.

        @return: MenuItem object that is
        referenced by the category and
        item pointed to in the display.
        """
        menu_list = self._get_selected_category_list()

        if item_itr:
            item_model = self.item_view.get_model()
        else:
            item_model, item_itr = self.get_selected_item()

        if item_itr and menu_list:
            path = item_model.get_path(item_itr)
            index = path.get_indices()[0]

            return menu_list[index]

    def toggle_stars_editable_display(self, switch_widget, *args):
        """Toggles if the stars editable area should become
        interactive or not, based on if the editable switch
        has been toggled.

        @param switch_widget: Gtk.Switch that called this
        method.

        @param *args: wildcard catchall used to catch
        any user defined arguments

        @return: None
        """
        # Since this method is called before the action is
        # performed. We have negated the returned boolean.
        switch_will_be_on = not switch_widget.get_active()
        self.stars_spin_button.set_sensitive(switch_will_be_on)

    def confirm_data(self, *args):
        """Confirm data method is called
        when the confirm button has been clicked.
        This method calls the confirm_func stored
        in the object with object specific parameters
        passed as arguments.

        @param args: Wildcard catchall that is used
        to catch the Gtk.Widget that called this method.

        @return: dict of str to lists. Each key is a
        str that represents the category, and each
        value is a list of MenuItem objects that represents
        the MenuItem objects associated with that category.
        """
        self.confirm_func(self.menu_item_data)

        return self.menu_item_data


class GeneralOptionSelectionDialog(SelectionDialog):
    """GeneralOptionSelectionDialog allows the user to
    select from the total list of possible option items
    available and apply them to the order corresponding
    to an "ADD", "SUB", or "NO" relation.

    @group SelectionDialog: This class is a subclass member
    of the SelectionDialog group and as such it inherits
    some of its functionality from SelectionDialog class.
    Any changes in the SelectionDialog class may effect
    the functionality of this class.

    @var menu_item: MenuItem object that is being interacted
    with.

    @var option_data: dict of str keys that represent the
    categories of the options, to list of OptionItem values
    that represent the associated OptionItems with the
    category.

    @var display_data: dict of str keys that represent the
    associated categories mapped to Gtk.ListStore that
    store the represented data in displayable model form.

    @var new_option_list: list of OptionItem objects that
    represents the list associated with the MenuItem.

    @var category_view: Gtk.TreeView that displays the
    categories and allows for user selection.

    @var option_view: Gtk.TreeView that displays the
    OptionItem information and allows for user selection.

    @var item_view: Gtk.TreeView that displays the current
    MenuItems selected OptionItems. Allows for user selection
    and manipulation.
    """

    def __init__(self, parent, option_data, menu_item,
                 title='General Option Selection'):
        """Initializes a new GeneralOptionSelectionDialog.

        @param parent: Gtk.Object that called this Dialog window.

        @param option_data: dict of key strs that represent each
        category. The values are lists of OptionItem objects that
        represent the available options under that category.

        @param menu_item: MenuItem object that is to have the
        dialog called on.

        @keyword title: str representing the title to be used
        on this Dialog window.
        """
        self.menu_item = menu_item
        self.option_data = option_data
        self.display_data = {}
        self.new_option_list = copy(menu_item.options)

        self.category_view = None
        self.option_view = None
        self.item_view = None

        super(GeneralOptionSelectionDialog, self).__init__(parent, title)

    def generate_main_selection_area(self):
        """Override Method.

        Generates the display for the main
        selection area.

        @return: Gtk.Container that displays
        the widgets associated with the main
        selection area.
        """
        main_box = Gtk.VBox()

        category_display = self.generate_category_view()
        main_box.pack_start(category_display, True, True, 5.0)

        return main_box

    def generate_category_view(self):
        """Generates the view to display
        the categories associated with
        the options.

        @return: Gtk.Container that holds
        the view to display the categories.
        """
        category_frame = Gtk.Frame(label='Categories Selection')
        scroll_window = Gtk.ScrolledWindow()

        model = Gtk.ListStore(str)

        for category in self.option_data:
            model.append((category,))

        self.category_view = Gtk.TreeView(model)
        selection = self.category_view.get_selection()
        selection.set_select_function(self.update_category_select, None)
        selection.connect('changed', tree_view_changed, self.category_view)

        rend = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn('Category', rend, text=0)
        self.category_view.append_column(col1)

        scroll_window.add(self.category_view)
        category_frame.add(scroll_window)

        return category_frame

    def get_category_view_selected(self):
        """Gets the selected model and data
        that is selected in the category view.

        @return: tuple (Gtk.TreeModel, Gtk.TreeIter),
        representing the model that stores the data
        and the iter pointing to the row selected.
        """
        selection = self.category_view.get_selection()
        return selection.get_selected()

    def set_category_selection(self, itr):
        """Sets the current selection of the
        category_view to point to the given
        itr.

        @param itr: Gtk.TreeIter pointing
        to a row in the category_view display.

        @return: None
        """
        if itr:
            selection = self.category_view.get_selection()
            selection.select_iter(itr)

    def update_category_select(self, selection, model, path, is_selected,
                               user_data=None):
        """Called when a row on the categories view has
        been selected.

        @param selection: Gtk.Selection that represents
        the selection associated with the categories
        view.

        @param model: Gtk.TreeModel that represents the
        model that stores the data associated with the
        categories view.

        @param path: Gtk.TreePath pointing to the row
        that was selected.

        @param is_selected: bool value that represents
        if the order was selected prior to current
        selection.

        @keyword user_data: Default user data passed
        to this method. By default is None.

        @return: bool value representing if the selection
        can be made. Default True
        """
        if not is_selected:
            itr = model.get_iter(path)
            key = model[itr][0]

            option_model = self.display_data[key]
            self.option_view.set_model(option_model)

        return True

    def generate_secondary_selection_area(self):
        """Override Method.

        Generates the display for the secondary
        selection area.

        @return: Gtk.Container that displays the
        widgets associated with the secondary
        selection area.
        """
        main_box = Gtk.VBox()

        option_display = self.generate_option_view()
        main_box.pack_start(option_display, True, True, 5.0)

        return main_box

    def generate_option_view(self):
        """Generates the view to display
        the selectable options.

        @return: Gtk.Container that holds
        the view to display the options.
        """
        option_frame = Gtk.Frame(label='Options Selection')
        scroll_window = Gtk.ScrolledWindow()

        for category in self.option_data:
            options_list = self.option_data[category]
            model = Gtk.ListStore(str, str)

            for option in options_list:
                name = option._name
                price = option.get_price()

                option_data = name, str(price)
                model.append(option_data)

            self.display_data[category] = model

        self.option_view = Gtk.TreeView()
        selection = self.option_view.get_selection()
        selection.connect('changed', tree_view_changed, self.option_view)

        rend = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn('Option Name', rend, text=0)
        self.option_view.append_column(col1)

        col2 = Gtk.TreeViewColumn('Add Cost', rend, text=1)
        self.option_view.append_column(col2)

        scroll_window.add(self.option_view)
        option_frame.add(scroll_window)

        return option_frame

    def get_option_view_selected(self):
        """Gets the selected model and data
        that is selected in the option view.

        @return: tuple (Gtk.TreeModel, Gtk.TreeIter),
        representing the model that stores the data
        and the iter pointing to the row selected.
        """
        selection = self.option_view.get_selection()
        return selection.get_selected()

    def set_option_selection(self, itr):
        """Sets the row selected in the
        options_view to the row pointed to
        by the given itr.

        @param itr: Gtk.TreeIter pointing to
        a row displayed in the options_view.

        @return: None
        """
        if itr:
            selection = self.option_view.get_selection()
            selection.select_iter(itr)

    def generate_properties_selection_area(self):
        """Override Method.

        Generates the display for the properties
        selection area.

        @return: Gtk.Container that displays
        the widgets associated with the properties
        selection area.
        """
        main_box = Gtk.VBox()

        item_display = self.generate_item_view()
        main_box.pack_start(item_display, True, True, 0.0)

        button_box = Gtk.HBox()

        add_box = Gtk.VBox()

        sub_box = Gtk.HBox()
        add_button = Gtk.Button('ADD OPTION')
        add_button.set_can_focus(False)
        add_button.set_size_request(150, 50)
        add_button.connect('clicked', self.add_new_option, 1.0)
        sub_box.pack_start(add_button, False, False, 5.0)
        add_box.pack_start(sub_box, False, False, 5.0)

        sub_box = Gtk.HBox()
        sub_button = Gtk.Button('SUB OPTION')
        sub_button.set_can_focus(False)
        sub_button.set_size_request(150, 50)
        sub_button.connect('clicked', self.add_new_option, -1.0)
        sub_box.pack_start(sub_button, False, False, 5.0)
        add_box.pack_start(sub_box, False, False, 5.0)

        sub_box = Gtk.HBox()
        no_button = Gtk.Button('NO OPTION')
        no_button.set_can_focus(False)
        no_button.set_size_request(150, 50)
        no_button.connect('clicked', self.add_new_option, 0.0)
        sub_box.pack_start(no_button, False, False, 5.0)
        add_box.pack_start(sub_box, False, False, 5.0)

        button_box.pack_start(add_box, False, False, 5.0)

        remove_button_box = Gtk.VBox()

        remove_button = Gtk.Button('REMOVE OPTION')
        remove_button.connect('clicked', self.remove_selected_option)
        remove_button.set_can_focus(False)
        remove_button.set_size_request(150, 50)
        remove_button_box.pack_start(remove_button, False, False, 5.0)

        button_box.pack_end(remove_button_box, False, False, 5.0)

        main_box.pack_start(button_box, False, False, 5.0)

        return main_box

    def generate_item_view(self):
        """Generates the display view
        that displays the items associated
        with the current

        @return:
        """
        item_frame = Gtk.Frame()
        scroll_window = Gtk.ScrolledWindow()

        model = Gtk.ListStore(str, str, str)

        for option in self.new_option_list:
            relation = option.get_option_relation()
            name = option.get_name()
            price = option.get_price()

            option_data = relation, name, str(price)
            model.append(option_data)

        self.item_view = Gtk.TreeView(model)

        rend = Gtk.CellRendererText()
        col0 = Gtk.TreeViewColumn('Relation', rend, text=0)
        self.item_view.append_column(col0)

        col1 = Gtk.TreeViewColumn('Option Name', rend, text=1)
        self.item_view.append_column(col1)

        col2 = Gtk.TreeViewColumn('Price', rend, text=2)
        self.item_view.append_column(col2)

        scroll_window.add(self.item_view)

        item_frame.add(scroll_window)
        return item_frame

    def get_item_view_selected(self):
        """Gets the selected model and data
        that is selected in the item view.

        @return: tuple (Gtk.TreeModel, Gtk.TreeIter),
        representing the model that stores the data
        and the iter pointing to the row selected.
        """
        selection = self.item_view.get_selection()
        return selection.get_selected()

    def add_new_option(self, widget, option_relation):
        """Adds a new option to the MenuItem area,
        with the given relation.

        @param widget: Gtk.Widget that called this
        method.

        @param option_relation: str representing the
        relation that this option will share with the
        MenuItem.

        @return: None
        """
        option_model, itr = self.get_option_view_selected()
        category_model, category_itr = self.get_category_view_selected()
        category = category_model[category_itr][0]

        if itr:
            item_model = self.item_view.get_model()

            name = option_model[itr][0]
            if option_relation == 1:
                price = option_model[itr][1]
            else:
                price = str(0.0)

            option_list = self.option_data[category]
            path = option_model.get_path(itr)
            index = path.get_indices()[0]

            option_item = copy(option_list[index])
            option_item.set_option_relation(option_relation)

            self.new_option_list.append(option_item)

            relation = option_item.get_option_relation()

            option_data = relation, name, price
            item_model.append(option_data)

    def remove_selected_option(self, *args):
        """Removes the currently selected item
        in the

        @param args: wildcard catchall that is
        used to catch the Gtk.Widget that called
        this method.

        @return: None
        """
        item_model, itr = self.get_item_view_selected()

        if itr:
            path = item_model.get_path(itr)
            index = path.get_indices()[0]

            item_model.remove(itr)
            self.new_option_list.pop(index)

    def confirm_data(self, *args):
        """Override Method.

        Confirms the data stored as
        the new_option_list by inserting
        it in to the given MenuItem object.

        @param args: wildcard catchall that is
        used to catch the Gtk.Widget that called
        this method.

        @return: None
        """
        self.menu_item.options = self.new_option_list


class AuditDataSelectionDialog(SelectionDialog):
    """AuditDisplaySelectionDialog allows the user to
    select a date range to run an audit over of all files
    that fall within the associated date range. The dialog
    also allows the user to select a location that the
    file will be saved to.

    @group SelectionDialog: This class is a subclass member
    of the SelectionDialog group and as such it inherits
    some of its functionality from SelectionDialog class.
    Any changes in the SelectionDialog class may effect
    the functionality of this class.

    @cvar DEFAULT_FILE_PATH: str representing the default
    file path that will be displayed as a place holder to
    notify the user that the file path selected is currently
    the default.

    @cvar DEFAULT_FILE_NAME: str representing the default
    file name that the audit will be saved under.

    @var confirm_func: Function that is to be called upon
    confirmation of the dialog window.

    @var selection_calendar: Gtk.Calendar that is to be
    interacted with by the user to select a dates.

    @var location_entry: Gtk.Entry that represents a str
    associated with the file path that the audit
    will be saved at.

    @var name_entry: Gtk.Entry that represents a str associated
    with the file name that the audit will be saved as.

    @var from_date_display: Gtk.Entry that represents a str
    associated with the start date for the audit.

    @var until_date_display: Gtk.Entry that represents a str
    associated with the end date for the audit.

    @var warning_label: Gtk.Label that is used to display
    warning messages to the user.

    @var date_bounds: list of expected length 2 that stores
    the start date at the first index [0] and the end date
    as the last index[1].
    """

    DEFAULT_FILE_PATH = SYSTEM_AUDIT_REQUESTS_PATH
    DEFAULT_FILE_NAME = DEFAULT_AUDIT_NAME

    def __init__(self, parent, confirm_func, title='Data Auditor'):
        """Initializes a new AuditDataSelectionDialog window.

        @param parent: Gtk.Object that this dialog window was
        called on.

        @param confirm_func: function that is to be called when
        the dialog window is confirmed.

        @param title: str representing the title associated with
        this dialog window.
        """
        self.confirm_func = confirm_func

        self.location_entry = Gtk.Entry()
        self.name_entry = Gtk.Entry()

        self.selection_calendar = Gtk.Calendar()

        self.from_date_display = Gtk.Entry()
        self.until_date_display = Gtk.Entry()

        self.warning_label = Gtk.Label()

        self.date_bounds = [0.0, 0.0]

        super(AuditDataSelectionDialog, self).__init__(parent, title)

        buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN,
                   Gtk.ResponseType.ACCEPT)

        self.file_chooser = Gtk.FileChooserDialog('Save Audit As', self.dialog,
                              Gtk.FileChooserAction.SELECT_FOLDER,buttons)

    def generate_main_selection_area(self):
        """Generates the main selection area for the
        SelectionDialog.

        @return: Gtk.Container that holds all the associated
        widgets to be displayed in the main selection area.
        """
        frame = Gtk.Frame(label='Storage Selection Area')
        main_box = Gtk.VBox()

        sub_box = Gtk.HBox()
        sub_box.pack_start(Gtk.Label('File Save Location:'), False, False, 5.0)
        main_box.pack_start(sub_box, False, False, 5.0)

        sub_box = Gtk.HBox()
        sub_box.pack_start(self.location_entry, True, True, 5.0)
        sub_box.pack_start(Gtk.Fixed(), True, True, 5.0)
        self.location_entry.set_text(self.DEFAULT_FILE_PATH)
        self.location_entry.set_sensitive(False)

        main_box.pack_start(sub_box, False, False, 5.0)
        select_location = Gtk.ToggleButton('Edit Save as Location')
        select_location.set_can_focus(False)

        sub_box = Gtk.HBox()
        sub_box.pack_start(select_location, False, False, 5.0)
        select_location.connect('toggled', self.location_toggled)
        select_location.set_size_request(200, 50)

        main_box.pack_start(sub_box, False, False, 5.0)

        sub_box = Gtk.HBox()
        sub_box.pack_start(Gtk.Label('File Save as Name:'), False, False, 5.0)
        main_box.pack_start(sub_box, False, False, 5.0)

        sub_box = Gtk.HBox()
        sub_box.pack_start(self.name_entry, True, True, 5.0)
        self.name_entry.set_text(self.DEFAULT_FILE_NAME)
        self.name_entry.set_sensitive(False)

        sub_box.pack_start(Gtk.Label('.xlsx'), False, False, 5.0)

        main_box.pack_start(sub_box, False, False, 5.0)
        sub_box = Gtk.HBox()
        select_name = Gtk.ToggleButton('Edit Save as Name')
        select_name.set_can_focus(False)

        sub_box.pack_start(select_name, False, False, 5.0)
        select_name.connect('toggled', self.name_toggled)
        select_name.set_size_request(200, 50)

        main_box.pack_start(sub_box, False, False, 5.0)

        frame.add(main_box)
        return frame

    def generate_secondary_selection_area(self):
        """Generates the secondary selection area for
        the SelectionDialog.

        @return: Gtk.Container that holds all the widgets
        to be displayed in the secondary selection area.
        """
        frame = Gtk.Frame(label='Date Selection Area')
        main_box = Gtk.VBox()

        sub_box = Gtk.HBox()
        calendar_frame = Gtk.Frame()
        calendar_frame.add(self.selection_calendar)

        sub_box.pack_start(calendar_frame, False, False, 5.0)
        main_box.pack_start(sub_box, True, True, 5.0)

        main_box.pack_start(Gtk.Fixed(), True, True, 5.0)

        sub_box = Gtk.HBox()
        sub_box.pack_start(Gtk.Label('Start Date:'), False, False, 5.0)
        main_box.pack_start(sub_box, False, False, 5.0)

        sub_box = Gtk.HBox()
        sub_box.pack_start(self.from_date_display, True, True, 5.0)
        self.from_date_display.set_sensitive(False)

        set_start_date_button = Gtk.Button('set Start Date')
        sub_box.pack_start(set_start_date_button, True, True, 5.0)
        set_start_date_button.connect('clicked', self.set_start_date)

        sub_box.pack_start(Gtk.Fixed(), True, True, 5.0)
        main_box.pack_start(sub_box, True, True, 5.0)

        sub_box = Gtk.HBox()
        sub_box.pack_start(Gtk.Label('Until Date:'), False, False, 5.0)
        main_box.pack_start(sub_box, False, False, 5.0)

        sub_box = Gtk.HBox()
        sub_box.pack_start(self.until_date_display, True, True, 5.0)
        self.until_date_display.set_sensitive(False)

        set_end_date_button = Gtk.Button('set Until Date')
        sub_box.pack_start(set_end_date_button, True, True, 5.0)
        set_end_date_button.connect('clicked', self.set_end_date)
        set_end_date_button.set_size_request(100, 15)

        sub_box.pack_start(Gtk.Fixed(), True, True, 5.0)
        main_box.pack_start(sub_box, True, True, 5.0)

        main_box.pack_start(self.warning_label, True, True, 5.0)

        frame.add(main_box)
        return frame

    def generate_properties_selection_area(self):
        """Generates the properties selection area to
        be displayed in the selectionDialog.

        @return: Gtk.Container that holds all the
        widgets associated with the properties
        selection area.
        """
        return Gtk.HBox()

    def location_toggled(self, toggle_button, **kwargs):
        """Toggles the location area to allow the
        user to edit the location that the generated
        audit file will be saved to.

        Allows the user to toggle between the default
        or a selected directory.

        @param toggle_button: Gtk.ToggleButton that
        called this method.

        @param kwargs: dict wildcard catchall that is
        used to catch keyword parameters that will be
        used for testing purposes. All keyword parameters
        will be passed to secondary called methods.

        @return: None
        """
        self.set_warning_message('')
        if toggle_button.get_active():
            file_path = self.choose_location(**kwargs)

            if file_path == self.DEFAULT_FILE_PATH:
                toggle_button.set_active(False)

            self.location_entry.set_text(file_path)

        else:
            self.location_entry.set_text(self.DEFAULT_FILE_PATH)

    def choose_location(self, *args, **kwargs):
        """Opens and controls a new dialog window
        that allows the user to select a new path
        for the file to be saved to.

        @param args: wildcard catchall used to catch
        the Gtk.Widget that called this method.

        @param kwargs: dict wildcard catchall used to catch
        test information passed into this method. The
        current test parameters are as such:

            1. 'file_chooser' = Gtk.FileChooserDialog that
            is to have information pulled from it.

            2. 'file_chooser_response' = Gtk.ResponseType
            to be simulated as emitted from the file_chooser.

        @return: str representing the directory selected
        by the user. If no choice was made by the user
        then the default file path is returned.
        """
        self.set_warning_message('')

        file_chooser = self.file_chooser
        response = False

        # Test case. Allows for dummy file chooser.
        if 'file_chooser' in kwargs:
            file_chooser = kwargs['file_chooser']

        # Test case. Allows for dummy response.
        if 'file_chooser_response' in kwargs:
            response = kwargs['file_chooser_response']
        else:
            response = file_chooser.run()

        file_path = file_chooser.get_filename()
        file_chooser.hide()

        if response == Gtk.ResponseType.ACCEPT:

            return file_path

        else:
            return self.DEFAULT_FILE_PATH

    def name_toggled(self, toggle_button):
        """Toggles the name area to be editable
        by the user.

        @param toggle_button. Gtk.ToggleButton that
        called this method.

        @return: None
        """
        self.set_warning_message('')
        if toggle_button.get_active():
            name_sensitive = True
            name_text = ''
        else:
            name_sensitive = False
            name_text = self.DEFAULT_FILE_NAME

        self.name_entry.set_sensitive(name_sensitive)
        self.name_entry.set_text(name_text)

    def set_start_date(self, *args):
        """Sets the currently selected date in the
        calendar area as the currently selected start
        date for the audit. Updates the start date display
        area to notify the user.

        @param args: wildcard catchall that is used
        to catch the Gtk.Widget that called this method.

        @return: None
        """
        self.set_warning_message('')
        text = self.from_date_display.get_text()
        text = text.strip()

        year, month, day = self.selection_calendar.get_date()

        start_date = date(year, month + 1, day)

        self.from_date_display.set_text(self._get_date_str(start_date))
        self.date_bounds[0] = datetime.combine(start_date, time.min)

    def set_end_date(self, *args):
        """Sets the currently selected date in the
        calendar area as the currently selected end
        date for the audit. Updates the end date display
        area to notify the user.

        @param args: wildcard catchall that is used to
        catch the Gtk.Widget that called this method.

        @return: None
        """
        self.set_warning_message('')
        text = self.until_date_display.get_text()
        text = text.strip()

        year, month, day = self.selection_calendar.get_date()

        end_date = date(year, month + 1, day)
        self.until_date_display.set_text(self._get_date_str(end_date))
        self.date_bounds[1] = datetime.combine(end_date, time.max)

    def _get_date_str(self, date):
        """Gets the str associated with the
        given date, in the mm/dd/yyyy format.

        @param date: datetime.date object that
        represents the date to be transfered to
        a str.

        @return: str representing the date in
        standard mm/dd/yyyy format.
        """
        return '{}/{}/{}'.format(date.month, date.day, date.year)

    def set_warning_message(self, message):
        """

        @param message:
        @return:
        """
        markup = '<span foreground="red" weight="bold">' + message + '</span>'
        self.warning_label.set_markup(markup)

    def confirm_button_clicked(self, *args):
        """Confirms the selected dialog window. This
        method checks if the selected information is
        able to be confirmed, if so then the dialog
        window is confirmed. If not then a warning
        message is displayed in the dialog window
        prompting the user.

        @param args: wildcard catchall that is used
        to catch the Gtk.Widget that called this method.

        @return: None
        """
        self.set_warning_message('')
        name = self.name_entry.get_text()
        name = name.strip()

        if '.' in name:
            name = ''

        location = self.location_entry.get_text()
        location = location.strip()

        start_date = self.date_bounds[0]
        end_date = self.date_bounds[1]

        if not (start_date and end_date) or (end_date < start_date):
            self.set_warning_message('Invalid dates selected!')
        elif not name and location:
            self.set_warning_message('Invalid save name or location')
        else:
            self.set_warning_message('Please wait while the data is compiled')
            super(AuditDataSelectionDialog, self).confirm_button_clicked(
                start_date, end_date, location, name)

    def confirm_data(self, start_date, end_date, location, name):
        """Confirms the data by calling the confirm function
        associated with this dialog window with data regarding
        the start date, end date of the audit as well as the
        location and name associated with where the file should
        be saved.

        @param start_date: datetime.date object that represents
        the start date of the audit.

        @param end_date: datetime.date object that represents the
        end date of the audit.

        @param location: str representing the directory location
        where the file is to be saved.

        @param name: str representing the name that the file
        will be saved as under the directory location.

        @return: None
        """
        name += FILE_TYPE_SEPARATOR + AUDIT_FILE_TYPE
        kwargs = {'file_path': os.path.join(location, name)}
        self.confirm_func(start_date, end_date, **kwargs)


#==========================================================
# This block represents windows that form the specific
# classes that can be instantiated. All classes in this
# block perform operations on an entire order, but are
# considered more complex operations that the simple
# operations performed in the previous block.
#
# Upon confirmation each class in this block mimics the
# previous block and calls a given function that is
# passed into the class at instantiation as its
# "confirm func"
#
# Each class in this block belongs to the group that relies
# on the instantiable CheckoutConfirmationDialog or
# OrderConfirmationDialog. Any changes in their respective
# super classes will change the functionality of these
# classes.
#==========================================================
class SplitCheckConfirmationDialog(CheckoutConfirmationDialog):
    """SplitCheckConfirmationDialog object displays the given
    information allowing the user to split any MenuItem object
    into separate checks. Confirmation leads to the confirm function
    given to be called. Cancellation leads to exiting the dialog.

    @group Dialog: subclass member of Dialog. Extends
    or overrides functionality from superclass Dialog

    @group ConfirmationDialog: subclass member of the
    ConfirmationDialog. Extends or overrides functionality
    from the superclass ConfirmationDialog

    @group CheckoutConfirmationDialog: subclass member of the
    CheckoutConfirmationDialog. Extends or overrides functionality
    from the superclass CheckoutConfirmationDialog.

    @var check_dict: dict representing the checks as keys and lists
    of MenuItems that are stored in the checks.

    @var checks_view: Gtk.TreeView associated with the checks to be
    displayed.

    @var _original_order_list: list of MenuItem objects that represents
    the pre-edited/copied order_list
    """

    def __init__(self, parent, confirm_func, order_list, dialog=None,
                 title='Split Check'):
        """Initializes the SplitCheckConfirmationDialog.


        @param parent: Gtk.Container that will hold the
        dialog window.

        @param confirm_func: function that is to be called
        upon confirmation of the dialog window.

        @param order_list: list of MenuItem objects that
        represents the current order being considered.

        @keyword dialog: Dialog window to be passed to superclass,
        Default=None. This feature hasn't been fully implemented yet

        @keyword title: str representing the title to be displayed
        on the dialog window

        @return: None
        """
        self.check_dict = {}
        self._original_order_list = order_list
        order_copy = []
        for menu_item in order_list:
            menu_item = copy(menu_item)
            menu_item._hash = hash(menu_item)
            order_copy.append(menu_item)

        self.checks_view = None
        self.confirm_func = confirm_func

        super(SplitCheckConfirmationDialog, self).__init__(parent, confirm_func, order_copy,
                                                           dialog=dialog, title=title)
        
        self.dialog.set_default_size(1100, 700)
        self.set_selection_type(Gtk.SelectionMode.MULTIPLE)
    
    def generate_layout(self):
        """Override Method.

        Generates the basic layout of the
        SplitCheckConfirmationDialog. Generates
        the necessary widgets to create functionality
        for a SplitCheckConfirmationDialog.

        @return: Gtk.Container that holds all the
        associated widgets. This is expected to be
        added directly to the dialog's content area.
        """
        main_box = Gtk.VBox()

        center_sub_box = Gtk.HBox()
        
        items_box = super(SplitCheckConfirmationDialog, self).generate_layout()

        center_sub_box.pack_start(items_box, True, True, 5)
        
        center_column_box = Gtk.VBox()
        center_column_box.set_homogeneous(True)
        
        center_column_box.pack_start(Gtk.Fixed(), True, True, 5)
        
        push_button = Gtk.Button('>')
        push_button.connect('clicked', self.push_items)
        push_button.set_size_request(100, 100)
        center_column_box.pack_start(push_button, True, True, 5)
        
        center_column_box.pack_start(Gtk.Fixed(), True, True, 5)
        
        pull_button = Gtk.Button('<')
        pull_button.connect('clicked', self.pull_items)
        pull_button.set_size_request(100, 100)
        center_column_box.pack_start(pull_button, True, True, 5)
        
        center_column_box.pack_start(Gtk.Fixed(), True, True, 5)
        
        center_sub_box.pack_start(center_column_box, False, False, 5)
        
        checks_box = self.generate_check_treeview()

        center_sub_box.pack_start(checks_box, True, True, 5)
        
        main_box.pack_end(center_sub_box, True, True, 5)
        
        top_sub_box = Gtk.HBox()
        
        item_label = Gtk.Label('ITEMS')
        top_sub_box.pack_start(item_label, False, False, 5)
        check_label = Gtk.Label('CHECKS')
        top_sub_box.pack_end(check_label, False, False, 5)
        
        main_box.pack_end(top_sub_box, False, False, 5)
        
        main_box.show_all()
        
        return main_box

    def generate_related_area(self):
        """Override Method.

        Generates the buttons associated
        with this dialog windows functionality.

        @return: Gtk.Container that holds the
        generated buttons.
        """
        sub_box = Gtk.HBox()

        button = Gtk.Button("SELECT ALL")
        button.connect('clicked', super(SplitCheckConfirmationDialog, self).select_all)
        button.set_size_request(175, 25)
        sub_box.pack_start(button, False, False, 5)

        return sub_box

    def generate_check_treeview(self):
        """Generates the Gtk.TreeView

        @return: Gtk.ScrollWindow object that holds
        the generated view.
        """
        main_box = Gtk.VBox()

        scroll_window = Gtk.ScrolledWindow()
        self.checks_view = Gtk.TreeView()
        
        self.checks_view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        col_list = self.generate_check_columns()
        
        for column in col_list:
            self.checks_view.append_column(column)
        
        model = self.generate_check_model()
        self.checks_view.set_model(model)
        
        scroll_window.add(self.checks_view)

        selection = self.checks_view.get_selection()
        selection.set_select_function(self._select_method, None)
        
        main_box.pack_start(scroll_window, True, True, 5)

        related_buttons = self.generate_check_related_buttons()

        main_box.pack_start(related_buttons, False, False, 5)

        return main_box
    
    def generate_check_columns(self):
        """Generates the columns associated with
        the check tree view.

        @return: list of Gtk.TreeViewColumns that
        are to be added to the check treeview.
        """
        col_list = []
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Items', rend, text=0)
        col_list.append(col)
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Price', rend, text=1)
        col_list.append(col)
        
        return col_list

    def generate_check_related_buttons(self):
        """Generates the buttons associated with
        the check tree view functionality.

        @return: Gtk.Container that holds the
        related buttons.
        """
        sub_box = Gtk.VBox()

        lower_sub_box1 = Gtk.HBox()
        lower_sub_box2 = Gtk.HBox()

        select_all_button2 = Gtk.Button('SELECT ALL')
        select_all_button2.set_size_request(175, 30)
        select_all_button2.connect('clicked', self.select_all)
        lower_sub_box1.pack_end(select_all_button2, False, False, 5)

        remove_check_button = Gtk.Button('REMOVE CHECK')
        remove_check_button.connect('clicked', self.remove_selected_check)
        remove_check_button.set_size_request(175, 30)
        lower_sub_box2.pack_end(remove_check_button, False, False, 5)

        add_check_button = Gtk.Button("ADD CHECK")
        add_check_button.connect('clicked', self.add_new_check)
        add_check_button.set_size_request(175, 30)
        lower_sub_box2.pack_end(add_check_button, False, False, 5)

        sub_box.pack_end(lower_sub_box2, True, True, 5)
        sub_box.pack_end(lower_sub_box1, True, True, 5)

        return sub_box

    def get_selected(self):
        """Override Method.

        Gets the selected rows from the check view
        associated with this object.

        @return: 2-tuple, first index is the model
        associated with the check_view, the second
        is a n-tuple of Gtk.TreePath type that points
        to each of the n selected rows.
        """
        return self._check_get_selected()

    def generate_check_model(self):
        """Generates the model associated
        with the check_view. This model
        holds a 2-tuple of (str, str) that
        represent the name and price for the
        associated menu item.

        @return: Gtk.TreeModel object that is
        to be added to the generated check_view
        """
        tree_model = Gtk.TreeStore(str, str)
        return tree_model

    def _check_get_selected(self):
        """ Private Method.

        Gets the selected rows from the check view
        associated with this object.

        @return: 2-tuple, first index is the model
        associated with the check_view, the second
        is an n-tuple of Gtk.TreePath type that points
        to each of the n selected rows.
        """
        selection = self.checks_view.get_selection()
        return selection.get_selected_rows()

    def _item_get_selected(self):
        """Private Method.

        Gets the selected rows from the item view
        associated with this object.

        item_view object is generated and stored in
        the super class CheckoutConfirmationDialog

        @return: 2-tuple, first index is the model
        associated with the item view, the second
        is an n-tuple of Gtk.TreePath type that points
        to each of the n selected rows.
        """
        return super(SplitCheckConfirmationDialog, self).get_selected()
    
    def add_new_check(self, *args):
        """Callback Method.

        Adds a new check to the object. This check
        will be generated as the (n + 1)th check if there
        exists checks 1-n. Under some circumstances it
        may generate a lower ordered check (pth) if the
        pth check doesn't exist.

        @param args: wildcard catchall to catch the Gtk.Widget
        that called this method.

        @return: None
        """
        model = self.checks_view.get_model()
        key = 'Check ' + str(len(self.check_dict) + 1)

        counter = 1

        while key in self.check_dict:
            key = 'Check ' + str(counter)
            counter = counter + 1
        
        self.check_dict[key] = []
        itr = model.append(None, (key, '0.0'))

    def remove_selected_check(self, *args):
        """Callback Method

        Removes the selected checks from
        consideration. All items in these
        checks are pushed back into the items.

        @param args: wildcard catchall for the widget
        that called this method.

        @return: None
        """
        model, paths = self._check_get_selected()
        self.pull_items()

        row_refs = get_row_refs(model, paths)

        for row_ref in row_refs:
            path = row_ref.get_path()
            itr = model.get_iter(path)
            itr = ensure_top_level_item(model, itr)
            key = model[itr][0]
            model.remove(itr)
            del self.check_dict[key]

    def select_all(self, *args):
        """ Override Method.

        selects all the selectable checks that are
        available in the check_view associated with
        this object. Adheres to the selection function
        requirements.

        @param args: wildcard catchall used to catch any
        Gtk.Widget using this as callback method.

        @return: None
        """
        selection = self.checks_view.get_selection()
        selection.select_all()

    def push_items(self, *args):
        """Push the items selected in the item_view
        into the checks selected in the check_view. If
        multiple checks are selected each menu_item is
        subdivided to be shared equally between each
        selected check.

        @param args: wildcard catchall for the Gtk.Widget
        that called this method.

        @return: None
        """
        item_model, item_paths = self._item_get_selected()
        check_model, check_paths = self._check_get_selected()

        if len(item_paths) > 0 and len(check_paths) > 0:

            item_refs = get_row_refs(item_model, item_paths)

            denominator = len(check_paths)

            items_subtracted_total = 0.0

            for item_ref in item_refs:
                item_path = item_ref.get_path()
                item_itr = item_model.get_iter(item_path)
                index = item_path.get_indices()[0]

                item_itr = ensure_top_level_item(item_model, item_itr)

                item_model.remove(item_itr)
                menu_item = self.order_list.pop(index)
                items_subtracted_total = items_subtracted_total + menu_item.get_price()
                cost = math.ceil(menu_item.get_price() * 100 / denominator) / 100
                name = menu_item.get_name()

                for check_path in check_paths:
                    new_menu_item = deepcopy(menu_item)
                    new_menu_item.edit_price(cost)

                    check_itr = check_model.get_iter(check_path)
                    check_itr = ensure_top_level_item(check_model, check_itr)

                    key = check_model[check_itr][0]

                    check_order = self.check_dict[key]
                    check_order.append(new_menu_item)
                    check_model.append(check_itr, (name, str(new_menu_item.get_price())))

                    self._update_check_total(check_model, check_itr, new_menu_item.get_price())

            super(SplitCheckConfirmationDialog, self)._update_check_total(-1 * items_subtracted_total)

    def _update_check_total(self, model, itr, price):
        """Updates the total associated with
        the selected check information passed in.
        The total is then modified by adding the price
        to the total.

        @param model: Gtk.TreeModel that stores the
        selected check's information.

        @param itr: Gtk.TreeIter that points to the
        selected check.

        @param price: float value that will be added
        to the total of the check, pointed to by the
        itr parameter. This value should be negative if
        it is to be subtracted.

        @return: Gtk.TreeIter pointing to the updated
        check.
        """
        total = float(model[itr][1])
        model[itr][1] = str(total + price)
        return itr

    def pull_items(self, *args):
        """ Pull the items selected in the check_view
        back to the items_view. Any previously split
        items will be merged back together if possible.

        If an entire check is selected in the check_view
        all menu items that are associated with it are
        pulled back. If a single item is selected from
        any check then that single menu_item will be
        pulled back.

        Selecting entire checks and sub menu_items are
        mutually exclusive and as such cannot occur at
        the same time.

        @param args: wildcard catchall used to catch the
        Gtk.Widget that called this method.

        @return: None
        """
        check_model, check_paths = self._check_get_selected()

        if len(check_paths) > 0:
            row_refs = get_row_refs(check_model, check_paths)

            menu_items = self.order_list[:]

            for row_ref in row_refs:
                path = row_ref.get_path()
                itr = check_model.get_iter(path)

                # If an entire check is selected
                if check_model.iter_has_child(itr):
                    key = check_model[itr][0]
                    current_check = self.check_dict[key]
                    menu_items = menu_items + current_check
                    check_model.insert_after(None, itr, (key, '0.0'))
                    check_model.remove(itr)
                    self.check_dict[key] = []

                # If a single menu item is selected
                elif check_model.iter_parent(itr):
                    index = path.get_indices()[1]
                    parent_itr = check_model.iter_parent(itr)

                    key = check_model[parent_itr][0]

                    current_check = self.check_dict[key]
                    curr_menu_item = current_check.pop(index)

                    menu_items.append(curr_menu_item)
                    check_model.remove(itr)

                    price = curr_menu_item.get_price()

                    self._update_check_total(check_model, parent_itr, -1*price)

            menu_items = self._sort_and_merge_items(menu_items)

            self.update_items(menu_items)

    def _sort_and_merge_items(self, curr_list):
        """ Private Method.

        Sorts a list of MenuItem objects by their
        stored hash values.

        @param curr_list: list of MenuItem objects that
        all contain values for MenuItem._hash

        @return: list of MenuItem objects that have been
        sorted according to their MenuItem._hash values.
        If two items shared the same MenuItem._hash value
        then they are combined. Increasing the price of
        that MenuItem by adding the two prices together.
        """
        if len(curr_list) < 2:
            return curr_list
        else:
            list_one = self._sort_and_merge_items(curr_list[len(curr_list) / 2:])
            list_two = self._sort_and_merge_items(curr_list[:len(curr_list) / 2])

            return self._merge(list_one, list_two)

    def _merge(self, list_one, list_two):
        """ Private Method.

        Merge procedure of the mergesort utilized by
        self._sort_and_merge_items. This merge procedure
        compares the menu items and sorts two of the lists
        into one list.

        In the equality case it merges the two MenuItems that
        are being compared together by combining their prices.

        @param list_one: list of MenuItem objects that is to be
        sorted.

        @param list_two: list of MenuItem objects that is to be
        sorted.

        @return: list of MenuItem objects that is the sorted
        list of both lists passed in as parameters.
        """
        result = []
        first_index = 0
        second_index = 0

        while first_index + second_index < (len(list_one) + len(list_two)):

            if len(list_one) <= first_index or len(list_two) <= second_index:

                if len(list_two) <= second_index:
                    result += list_one[first_index:]
                else:
                    result += list_two[second_index:]

                return result
            else:

                first_item = list_one[first_index]
                second_item = list_two[second_index]

                if first_item._hash == second_item._hash:
                    first_item.edit_price(first_item.get_price() + second_item.get_price())
                    result.append(first_item)
                    first_index += 1
                    second_index += 1
                else:

                    if first_item._hash < second_item._hash:
                        result.append(first_item)
                        first_index += 1
                    else:
                        result.append(second_item)
                        second_index += 1
        return result

    def _select_method(self, selection, model, path, is_selected, *args):
        """ Override, Private, Callback Method.

        Provides the behavior for the the Gtk.TreeSelection
        associated with the tree_view. This method is called
        whenever a participating Gtk.TreeSelection has an item
        selected.

        This method is called prior to selecting of the row.

        @param selection: Gtk.TreeSelection associated with the
        selection made.

        @param model: Gtk.TreeModel the model associated with the
        stored data.

        @param path: Gtk.TreePath pointing to the selected row.

        @param is_selected: bool value representing if the selected
        row was selected prior to the current selection.

        @param args: wildcard catchall

        @return: bool representing if the given row is selectable
        or not.
        """
        itr = model.get_iter(path)
        itr_parent = model.iter_parent(itr)

        if itr_parent:
            selection.unselect_iter(itr_parent)

        elif model.iter_has_child(itr):
            itr_child = model.iter_children(itr)

            while itr_child:
                selection.unselect_iter(itr_child)
                itr_child = model.iter_next(itr_child)

        return True

    def confirm_button_clicked(self, *args):
        """ Override, Callback Method.

        Confirms the dialog window. Makes
        calls to super classes overriden
        method.

        @param args: wildcard catchall used to
        catch the Gtk.Widget that called this
        method.

        @return: None if the confirmation isn't
        valid, int representing Gtk.ResponseType
        otherwise.
        """

        if len(self.order_list) == 0 and len(self.tree_view) <= 1:
            return super(SplitCheckConfirmationDialog, self).confirm_button_clicked(args)

        return None

    def confirm_data(self):
        """Override Method.

        Confirms the checks that
        have been subdivided, and calls
        the confirm function given in the
        constructor.

        @return: None
        """
        curr_order = []

        for key in self.check_dict:
            curr_order.append(self.check_dict[key])

        self.confirm_func(tuple(curr_order))


class CompItemsOrderConfirmationDialog(OrderConfirmationDialog):
    """CompItemsConfirmationDialog window allows the user to
    set the comp setting for any menu item in the given order
    list. Confirmation leads to these changes being confirmed
    and the confirmation function being called.

    @group Dialog: subclass member of Dialog. Extends
    or overrides functionality from superclass Dialog

    @group ConfirmationDialog: subclass member of the
    ConfirmationDialog. Extends or overrides functionality
    from the superclass ConfirmationDialog

    @group OrderConfirmationDialog: subclass member of the
    OrderConfirmationDialog. Extends or overrides functionality
    from the superclass OrderConfirmationDialog.

    @var message_entry: Gtk.TextView that represents the area
    that users enter messages to to added to comped items.

    """

    def __init__(self, parent, confirm_func, order_list, dialog=None,
                 title='Comp Dialog Window'):
        """Initializes the new CompItemsConfirmationDialog
        window that can be interacted with by the user to
        change the comp status of menu items.

        @param parent: Gtk.Container that represents the parent
        that called this dialog.

        @param confirm_func: function pointer that is to be called
        if/when this dialog window has been confirmed.

        @param order_list: List of MenuItem objects that represent
        the order being operated on.

        @keyword dialog: Dialog window to be passed to superclass,
        Default=None. This feature hasn't been fully implemented yet

        @keyword title: Title of the dialog window that will be displayed.
        Default = 'Comp Dialog Window'
        """
        self.message_entry = None
        super(CompItemsOrderConfirmationDialog, self).__init__(parent, confirm_func,
                                                               order_list, title=title)

    def generate_misc_widgets(self):
        """Override Method.

        Generates the widgets associated
        with this layout.

        @return: list of Gtk.Widget objects
        that represent the buttons associated
        with the given layout.
        """
        widget_list = []

        main_box = Gtk.VBox()
        main_box.pack_start(Gtk.Label('Message: '), True, True, 5.0)

        sub_box = Gtk.HBox()

        message_box = self.generate_message_entry()
        sub_box.pack_start(message_box, True, True, 5)

        main_box.pack_start(sub_box, True, True, 5.0)

        button_sub_box = Gtk.HBox()

        button = Gtk.Button('Toggle COMP w/ message')
        button.connect('clicked', self.comp_selected_item)
        button.set_size_request(200, 50)
        button_sub_box.pack_start(button, True, True, 5.0)

        for x in range(2):
            sub_box.pack_end(Gtk.Fixed(), True, True, 5)
            button_sub_box.pack_start(Gtk.Fixed(), True, True, 5.0)

        main_box.pack_start(button_sub_box, False, False, 5.0)

        widget_list.append(main_box)

        return widget_list

    def generate_message_entry(self):
        """Generates the message entry
        associated with this window.

        @return: Gtk.Container that
        holds the Gtk.TextView to be
        displayed.
        """
        frame = Gtk.Frame()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_size_request(400, 150)

        self.message_entry = Gtk.TextView()
        self.message_entry.set_justification(Gtk.Justification.LEFT)
        self.message_entry.set_wrap_mode(Gtk.WrapMode.WORD)

        scrolled_window.add(self.message_entry)
        frame.add(scrolled_window)

        return frame

    def generate_model(self):
        """Override Method.

        Generates the model that will
        store the information to be
        displayed to your user.

        @return: Gtk.TreeModel that
        stores the data for displaying.
        """
        tree_model = Gtk.TreeStore(str, str, int, bool)
        self.add_items_to_model(tree_model)

        return tree_model

    def add_items_to_model(self, tree_model):
        """Override Method.

        Adds items to the tree_model that
        will be displaying information about
        each menu item.

        @param tree_model: Gtk.TreeModel that
        represents the data to be displayed

        @return: None
        """
        for menu_item in self.order_list:

            name = menu_item.get_name()
            stars = str(menu_item.stars)

            if menu_item.is_comped():
                name = '( ' + name + ' )'
                stars = ''
                info = name, stars, STANDARD_TEXT, True

                itr = tree_model.append(None, info)

                row = (menu_item.get_comp_message(),) + info[1:]

                tree_model.append(itr, row)
            else:
                info = name, stars, STANDARD_TEXT, False

                itr = tree_model.append(None, info)

                if menu_item.has_options():
                    options = str(menu_item.options)[1:-1]

                    row = (options, ) + info[1:]
                    tree_model.append(itr, row)

                if menu_item.has_note():
                    note = menu_item.notes

                    row = (note, ) + info[1:]
                    tree_model.append(itr, row)

    def comp_selected_item(self, *args):
        """Comps the selected menu item in the
        order list. This removes all associated
        cost from it.

        @return:
        """
        text_buf = self.message_entry.get_buffer()
        start_itr = text_buf.get_start_iter()
        end_itr = text_buf.get_end_iter()
        message = text_buf.get_text(start_itr, end_itr, False)
        text_buf.delete(start_itr, end_itr)

        if message and len(message) > 0:
            model, itr = self.get_selected()

            itr = ensure_top_level_item(model, itr)

            row = model[itr]
            path = model.get_path(itr)
            index = path.get_indices()[0]

            child_itr = model.iter_children(itr)
            result = (child_itr != None)

            while child_itr and result:
                result = model.remove(child_itr)

            if row[3]:
                menu_item = self.order_list[index]

                row[0] = row[0][1:-1]
                row[1] = str(menu_item.stars)
                row[3] = False

                if menu_item.has_options():
                    options = str(menu_item.options)[1:-1]
                    model.append(itr, (options, '', STANDARD_TEXT, False))

                if menu_item.has_note():
                    note = menu_item.notes
                    model.append(itr, (note, '', STANDARD_TEXT, False))

            else:
                row[0] = '( ' + row[0] + ' )'
                row[1] = ''
                row[3] = True

                model.append(itr, (message, '', STANDARD_TEXT, True))

    def confirm_data(self):
        """Override Method.

        Confirms the comped menu items

        @return: None
        """
        model = self.tree_view.get_model()
        index = 0
        for row in model:

            is_comp = row[3]

            menu_item = self.order_list[index]

            child_itr = row.iterchildren()

            if is_comp:
                row_child = child_itr.next()
                message = row_child[0]
                menu_item.comp(True, message)
                self.order_list[index] = menu_item

            elif menu_item.is_comped():
                menu_item.comp(False, '')

            index += 1

        self.confirm_func(self.order_list)


class DiscountCheckoutConfirmationDialog(CheckoutConfirmationDialog):
    """DiscountCheckoutConfirmationDialog window is utilized by
    the user to display and edit discounts associated with a given
    order. This window instantiates a new dialog window and upon
    confirmation calls the confirm_func that will adjust the order
    so that the associated discount is added to the associated order.

    @group CheckoutConfirmationDialog: This class is a subclass member
    of the CheckoutConfirmationDialog group, and as such it inherits
    functionality from its superclass. Any changes to the superclass
    could change the functionality for this class.

    @var discount_button_group: tuple of Gtk.RadioButtons that represents
    the toggle group. This allows for access to the associated radio buttons
    at any time.

    @var discount_input_areas: list of Gtk.Widgets that represent the respective
    input areas for discount information.

    @var message_entry: Gtk.TextView object that is used to display and edit the
    message that will be associated with a specific discount.

    @var discount_view: Gtk.TreeView for displaying a list of template discounts
    that the user may choose from the apply standard often used discounts.
    """

    def __init__(self, parent, confirm_func, order_list, discount_templates,
                 dialog=None,title='Add Discount Dialog Window'):
        """ Initializes a new DiscountCheckoutConfirmationDialog window.

        @param parent: Gtk.Object that will be used as the parent of this
        dialog window. All interactions with the parent object will be
        frozen until this dialog is confirmed.

        @param confirm_func: function that will be called upon confirmation
        of this dialog.

        @param order_list: list of MenuItem objects that represents the
        current order to have a discount added to it.

        @param discount_templates: list of tuples that represents the
        discount template data.

        @param dialog: Unused argument. Leave as default.

        @param title: str representing the title to be displayed by the
        dialog window.
        """
        self.discount_templates = discount_templates
        self.discount_button_group = None
        self.discount_input_areas = []
        self.message_entry = None
        self.discount_view = None
        super(DiscountCheckoutConfirmationDialog, self).__init__(parent, confirm_func,
                                                                 order_list, title=title)

    def generate_layout(self):
        """Override Method.

        Generates the layout for the
        DiscountOrderConfirmationDialog
        this method relies heavily on super
        class generate_layouts before it.

        @return: Gtk.Container that holds
        the widgets to be displayed.
        """
        main_box = Gtk.HBox()

        view_display_box = Gtk.VBox()
        checkout_order_box = super(DiscountCheckoutConfirmationDialog,
                                   self).generate_layout()
        view_display_box.pack_start(checkout_order_box, True, True, 5.0)
        button_box = Gtk.HBox()
        remove_button = Gtk.Button('Remove Item')
        remove_button.connect('clicked', self.remove_selected_item)
        remove_button.set_size_request(200, 50)
        remove_button.set_can_focus(False)
        button_box.pack_start(remove_button, False, False, 0.0)

        view_display_box.pack_start(button_box, False, False, 0.0)
        main_box.pack_start(view_display_box, True, True, 5.0)

        discount_properties_box = self.generate_properties_panel()
        main_box.pack_start(discount_properties_box, False, False, 5.0)

        return main_box

    def generate_properties_panel(self):
        """Generates the properties panel
        area which lies to the right of
        the tree view and is used to display
        and edit property information associated
        with the discount properties of this
        class.

        @return: Gtk.Container that holds
        the widgets to be displayed.
        """
        main_box = Gtk.VBox()

        properties_selection_area = self.generate_properties_selection_area()
        main_box.pack_start(properties_selection_area, True, True, 5.0)

        confirmation_selection_area = self.generate_confirmation_selection_area()

        main_box.pack_start(confirmation_selection_area, False, False, 5.0)

        return main_box

    def generate_confirmation_selection_area(self):
        """Generate the confirmation selection area.
        This area will display widgets that are to
        be added to the bottom right hand side, which
        is designated at the confirmation selection
        area. This area provides the widgets that
        allow the user to add new discounts to the
        order.

        @return: Gtk.Container that holds all the
        necessary widgets that will display the
        information for the area.
        """
        border = Gtk.Frame(label='Confirm Discount Properties')

        discount_message_box = Gtk.VBox()

        discount_message_box.pack_start(Gtk.Label('Message: '), False, False, 0.0)

        scrolled_window = Gtk.ScrolledWindow()

        text_view_frame = Gtk.Frame()
        self.message_entry = Gtk.TextView()
        self.message_entry.set_size_request(250, 150)
        self.message_entry.set_wrap_mode(Gtk.WrapMode.WORD)

        scrolled_window.add(self.message_entry)
        text_view_frame.add(scrolled_window)
        discount_message_box.pack_start(text_view_frame, False, False, 5.0)

        add_discount_button = Gtk.Button('Add Discount To Order')
        add_discount_button.set_size_request(200, 50)
        add_discount_button.connect('clicked', self.add_discount_to_order)
        add_discount_button.set_can_focus(False)
        discount_message_box.pack_start(add_discount_button, False, False, 5.0)

        border.add(discount_message_box)

        return border

    def generate_properties_selection_area(self):
        """Generates the properties selection area.
        This area contains all widgets that are used
        to edit specific properties associated with
        the discount. This is where the user may
        edit properties of a discount, or select
        the necessary information that will allow
        for a new discount to be placed on the order.

        @return: Gtk.Container that holds all the
        widgets that will be displayed for editing
        properties of discounts.
        """
        border = Gtk.Frame(label='Discount Properties')

        sub_box1 = Gtk.VBox()

        #Generate items to be displayed
        adjustment = Gtk.Adjustment(0.00, -100.00 * 1000.00, 1000.00 * 100.00, 0.01, 1.00, 0)
        discount_select_dollars = Gtk.SpinButton(adjustment=adjustment)
        discount_select_dollars.is_percentage = False
        discount_select_dollars.set_digits(2)

        discount_by_number_button = Gtk.RadioButton.new_with_label_from_widget(None, 'By Dollar Amount')
        discount_by_number_button.connect('toggled', self.update_property_display, discount_select_dollars)

        #generate containers and layout for items.
        discount_by_number_box = Gtk.VBox()
        discount_by_number_box.pack_start(discount_by_number_button, False, False, 0.0)
        discount_by_number_edit_box = Gtk.HBox()
        discount_by_number_edit_box.pack_start(Gtk.Label('Discount Total:     $'), False, False, 0.0)

        discount_by_number_edit_box.pack_start(discount_select_dollars, False, False, 0.0)
        self.discount_input_areas.append(discount_select_dollars)

        discount_by_number_box.pack_start(discount_by_number_edit_box, True, True, 5.0)

        sub_box1.pack_start(discount_by_number_box, False, False, 5.0)

        #generate items to be displayed
        adjustment = Gtk.Adjustment(0.00, -100.00, 100.00, 0.01, 1.00, 0)
        discount_from_total = Gtk.SpinButton(adjustment=adjustment)
        discount_from_total.is_percentage = True
        discount_from_total.set_digits(2)
        discount_from_total.set_sensitive(False)
        self.discount_input_areas.append(discount_from_total)

        discount_by_total_button = Gtk.RadioButton.new_with_label_from_widget(discount_by_number_button,
                                                                              'By Order Total')
        discount_by_total_button.connect('toggled', self.update_property_display, discount_from_total)
        discount_by_total_button.set_active(False)
        self.discount_button_group = discount_by_total_button.get_group()

        discount_display = self.generate_template_view()
        self.discount_view.set_sensitive(False)

        #generate containers and layout for items
        discount_by_total_box = Gtk.VBox()
        discount_by_total_box.pack_start(discount_by_total_button, False, False, 0.0)

        discount_by_total_edit_box = Gtk.HBox()
        discount_by_total_edit_box.pack_start(Gtk.Label('Discount Total:   '), False, False, 0.0)
        discount_by_total_edit_box.pack_start(discount_from_total, False, False, 0.0)
        discount_by_total_edit_box.pack_start(Gtk.Label(' %'), False, False, 0.0)
        discount_by_total_box.pack_start(discount_by_total_edit_box, False, False, 0.0)
        sub_box1.pack_start(discount_by_total_box, False, False, 5.0)

        sub_box1.pack_start(discount_display, True, True, 5.0)

        border.add(sub_box1)

        return border

    def generate_template_view(self):
        """Generates the treeview to display
        and select discount templates.

        @return: Gtk.TreeView that has been
        generated by this method.
        """
        main_box = Gtk.VBox()

        self.discount_view = Gtk.TreeView()

        add_from_templates_button = Gtk.RadioButton.new_with_label_from_widget(self.discount_button_group[0],
                                                                               'Discount From Template')
        add_from_templates_button.connect('toggled', self.update_property_display, self.discount_view)

        main_box.pack_start(add_from_templates_button, False, False, 5.0)

        scroll_window = Gtk.ScrolledWindow()

        rend = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn('Discount Name', rend, text=0)
        self.discount_view.append_column(col1)

        col2 = Gtk.TreeViewColumn('Price', rend, text=1)
        self.discount_view.append_column(col2)

        model = Gtk.ListStore(str, str, float, bool)

        for row in self.discount_templates:
            model.append(row)

        self.discount_view.set_model(model)
        scroll_window.add(self.discount_view)

        main_box.pack_start(scroll_window, True, True, 5.0)

        return main_box

    def update_property_display(self, widget, *args):
        """Updates the displayed property
        information.

        @param widget: Gtk.ToggleButton that called
        this method.

        @param args: list of Gtk.Widget objects that
        are to be set to sensitive dependent on the
        toggled state of the widget passed in.

        @return: None
        """

        set_sensitive = widget.get_active()

        for items in args:
            items.set_sensitive(set_sensitive)

    def add_discount_to_order(self, *args):
        """Adds the selected discount to the
        order.

        @param args: wildcard catchall to catch
        the Gtk.Widget that called this method.

        @return:None
        """
        msg_buffer = self.message_entry.get_buffer()
        start = msg_buffer.get_start_iter()
        end = msg_buffer.get_end_iter()
        message = msg_buffer.get_text(start, end, True)
        message = message.strip()

        msg_buffer.set_text('')

        if len(message) > 0:
            name = 'Discount '

            data, is_percentage = self.parse_discount_data()

            if is_percentage:
                price = round(CheckOperations.get_order_subtotal(self.order_list) * data / 100, 2)

                name += str(data) + '%'
            else:
                price = data
                name += '$' + str(price)

            discount_item = DiscountItem(name, -1 * price, message)
            discount_item.editable = False
            discount_item.confirmed = True
            discount_item.notes = message

            self.add_new_menu_item(discount_item)

    def parse_discount_data(self):
        """Parses the discount data
        that was selected by the user.

        @return: 2 tuple representing the
        value selected by the user and if
        that value should be interpreted as
        a percentage.
        """
        data = None
        is_percentage = None

        if self.discount_view.is_sensitive():
            selection = self.discount_view.get_selection()

            model, itr = selection.get_selected()

            row = model[itr]

            name = row[0] + ' '
            data = round(row[2], 2)
            is_percentage = row[3]

        else:
            counter = 0
            while not data and counter < len(self.discount_input_areas):
                display = self.discount_input_areas[counter]
                if display.is_sensitive():

                    data = round(display.get_value(), 2)
                    is_percentage = display.is_percentage
                counter += 1

        return data, is_percentage

    def generate_related_area(self):
        """Override Method.

        Generates the related area to be
        displayed underneath the the main
        view for displaying the order.

        @note: This class is overwritten
        so that the related area buttons
        are not populated. As such this
        method is simply an override.

        This is to prevent the Checkout
        confirmation dialog from
        displaying the split check button
        which is not helpful here.

        @return: Gtk.Container that is
        empty.
        """
        return Gtk.VBox()

    def confirm_data(self):
        """Override Method.

        Confirms the updated order list that
        has has discount MenuItems added or
        removed.

        @return: None
        """
        self.confirm_func(self.order_list)


#==========================================================
# This block represents windows that have used inheritance
# through multiple classes. All classes in this block have
# highly specific purposes that rely heavily on multiple
# classes from other groups. As such it is not recommended
# to inherit from these classes, as their inheritance tree
# could cause eventual problems by being excessively robust.
#==========================================================
class UpdateTemplateDiscountCheckoutConfirmationDialog(DiscountCheckoutConfirmationDialog):
    """UpdateTemplateDiscountCheckoutConfirmationDialog is a window
    that allows the user to update the templates stored and accessed by the
    DiscountCheckoutConfirmationDialog
    window.

    @warning: This class is not intended to be inherited from.
    This class instantiates all of its functionality primarily
    from its super classes. As well its inheritance tree is
    considered large enough that it would be unwise to continue
    inheritance.

    @var name_entry: Gtk.Entry that represents the area where the name
    if the new discount template will be stored.
    """
    def __init__(self, parent, confirm_func, discount_templates,
                 dialog=None, title='Discount Template Editor dialog'):
        """Initializes a new UpdateTemplateDiscountCheckoutConfirmationDialog
        window.

        @param parent: Gtk.Object that this dialog window will be called on.
        The parent will be unable to function until this dialog window closes.

        @param confirm_func: function that will be called upon confirmation
        of the dialog window.

        @keyword dialog: unimplemented keyword parameter. Usage has no effect,
        default is None.

        @param title: str representing the title that will be displayed on the
        dialog window.
        """
        self.name_entry = None
        self._discount_name_set = {name for name, _, _, _ in discount_templates}
        super(UpdateTemplateDiscountCheckoutConfirmationDialog, self).__init__(parent, confirm_func,
                                                                               [], discount_templates)
        self.tree_view.set_model(self.discount_view.get_model())

    def generate_columns(self):
        """Override Method

        Generates the columns
        to be displayed in the given
        order list.

        @return: list of Gtk.TreeViewColumn
        objects that are used to display the
        information in the associated view.
        """
        col_list = []

        rend = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn('Template Name', rend,
                                  text=0)
        col_list.append(col1)

        rend = Gtk.CellRendererText()
        col2 = Gtk.TreeViewColumn('Discount', rend,
                                  text=1)
        col_list.append(col2)

        return col_list

    def generate_model(self):
        """Override Method.

        Generates the model that will
        be used to store and display the
        information.

        @note: This method is used to
        eliminate the model display,
        which will be added after the
        discount view's model has been
        adjusted.

        @return: None
        """
        return None

    def generate_confirmation_selection_area(self):
        """Override Method.

        Generates the selection confirmation area that
        can be interacted with by the user to confirm
        a new template.

        @return: Gtk.Container that holds the widgets
        for confirmation window.
        """
        border = Gtk.Frame(label='Confirmation Area')
        main_box = Gtk.VBox()

        label_box = Gtk.HBox()
        label_box.pack_start(Gtk.Label('Name: '), False, False, 0.0)

        main_box.pack_start(label_box, False, False, 0.0)

        self.name_entry = Gtk.Entry()
        main_box.pack_start(self.name_entry, False, False, 5.0)

        add_discount_button = Gtk.Button('Add Discount Template')
        add_discount_button.connect('clicked', self.add_discount_to_order,
                                    self.tree_view.get_model())
        add_discount_button.set_size_request(150, 50)
        main_box.pack_start(add_discount_button, False, False, 0.0)

        border.add(main_box)
        return border

    def add_discount_to_order(self, *args):
        """Override Method

        Adds the selected discount information
        to the templates list.

        @param args: wildcard catchall that is
        used to catch the Gtk.Widget that called
        this method.

        @return: None
        """
        name = self.name_entry.get_text()
        name = name.strip()

        self.name_entry.set_text('')
        if name and name not in self._discount_name_set:
            value, is_percentage = self.parse_discount_data()

            value_str = str(value)

            if is_percentage:
                value_str += '%'
            else:
                value_str = '$' + value_str

            data = name, value_str, value, is_percentage

            tree_model = self.tree_view.get_model()
            tree_model.append(data)
            self._discount_name_set.add(name)

    def remove_selected_item(self, *args):
        """Override Method.

        Removes the selected discount template
        from the stored discount template information.

        @param args: wildcard catchall that is used
        to catch the Gtk.Widget that called this method.

        @return: None
        """
        model, itr = self.get_selected()

        if itr:
            name = model[itr][0]
            model.remove(itr)
            self._discount_name_set.remove(name)

    def confirm_data(self):
        """Override Method.

        Confirms the updated discount
        templates and calls the confirm
        func field.

        information is generated directly
        from the stored model in the discount
        template display.

        @return: None
        """
        discount_templates = []
        model = self.tree_view.get_model()
        for row in model:
            discount_templates.append(tuple(row))

        self.confirm_func(discount_templates)


class UpdateGeneralOptionSelectionDialog(GeneralOptionSelectionDialog):
    """UpdateGeneralOptionSelectionDialog allows the user to interact
    with the stored OptionItems data that may be accessed through
    the GeneralOptionSelectionDialog. This includes adding/editing
    OptionItems and categories.

    @warning: This class is not intended to be inherited from.
    This class instantiates all of its functionality primarily
    from its super classes. As well its inheritance tree is
    considered large enough that it would be unwise to continue
    inheritance.

    @var confirm_func: Function that is to be called upon
    confirmation of the data.

    @var category_entry: Gtk.Entry that allows the user to
    input a new category name when adding a category.

    @var name_entry: Gtk.Entry that allows the user to input
    a new option name when editing option properties.

    @var price_display: Gtk.SpinButton that allows the user
    to edit price data associated with an option.

    """

    def __init__(self, parent, confirm_func, option_data,
                 title='Update Options Dialog'):
        """Initializes a new UpdateGeneleratOptionSelectionDialog

        @param parent: Gtk.Object that represent the parent that
        this dialog window will be called on.

        @param confirm_func: Function that is to be called upon
        confirmation of the data.

        @param option_data: dict of str keys that represent the
        category, mapped to value list of OptionItems that
        represents the associated OptionItems.

        @keyword title: str representing the title to be displayed.
        Default 'Update Options Dialog'
        """
        self.confirm_func = confirm_func

        self.category_entry = None
        self.name_entry = None
        self.price_display = None

        menu_item = MenuItem('', 0.0)
        super(UpdateGeneralOptionSelectionDialog, self).__init__(parent,
                                                                 option_data,
                                                                 menu_item,
                                                                 title=title)

    def generate_main_selection_area(self):
        """Override Method

        Generates the main selection area
        to be displayed.

        @return: Gtk.Container that holds all
        the widgets to be displayed in the
        main selection area.
        """
        main_box = Gtk.VBox()

        category_display = super(UpdateGeneralOptionSelectionDialog,
                                 self).generate_main_selection_area()
        main_box.pack_start(category_display, True, True, 5.0)

        add_button_box = Gtk.HBox()

        self.category_entry = Gtk.Entry()
        add_button_box.pack_start(self.category_entry, False, False, 5.0)

        add_button = Gtk.Button('ADD CATEGORY')
        add_button.set_can_focus(False)
        add_button.connect('clicked', self.add_category)
        add_button.set_size_request(150, 30)
        add_button_box.pack_end(add_button, False, False, 5.0)

        main_box.pack_start(add_button_box, False, False, 5.0)

        remove_button_box = Gtk.HBox()

        remove_button = Gtk.Button('REMOVE CATEGORY')
        remove_button.set_can_focus(False)
        remove_button.connect('clicked', self.remove_category)
        remove_button.set_size_request(150, 30)
        remove_button_box.pack_end(remove_button, False, False, 5.0)

        main_box.pack_start(remove_button_box, False, False, 5.0)

        return main_box

    def generate_secondary_selection_area(self):
        """Override Method.

        Generates all the widgets to be displayed
        in the secondary selection area.

        @return: Gtk.Container that holds all
        widgets that are to be displayed in the
        secondary select area.
        """
        main_box = Gtk.VBox()

        option_display = super(UpdateGeneralOptionSelectionDialog,
                               self).generate_secondary_selection_area()
        main_box.pack_start(option_display, True, True, 5.0)

        selection = self.option_view.get_selection()
        selection.set_select_function(self.update_option_selection, None)

        add_button_box = Gtk.HBox()

        add_button = Gtk.Button('ADD NEW OPTION')
        add_button.set_can_focus(False)
        add_button.connect('clicked', self.add_new_option)
        add_button.set_size_request(150, 30)
        add_button_box.pack_start(add_button, False, False, 5.0)

        main_box.pack_start(add_button_box, False, False, 5.0)

        remove_button_box = Gtk.HBox()

        remove_button = Gtk.Button('REMOVE OPTION')
        remove_button.set_can_focus(False)
        remove_button.connect('clicked', self.remove_selected_option)
        remove_button.set_size_request(150, 30)
        remove_button_box.pack_start(remove_button, False, False, 5.0)

        main_box.pack_start(remove_button_box, False, False, 5.0)

        return main_box

    def generate_properties_selection_area(self):
        """Override Method.

        Generates the widgets to be displayed
        in the item selection area.

        @return: Gtk.Container that holds all
        widgets to be displayed in the item
        selection area.
        """
        frame = Gtk.Frame(label='Properties')
        main_box = Gtk.VBox()

        properties_box = Gtk.VBox()

        name_entry_box = Gtk.HBox()
        name_entry_box.pack_start(Gtk.Label('Name: '), False, False, 5.0)

        self.name_entry = Gtk.Entry()
        name_entry_box.pack_start(self.name_entry, True, True, 5.0)

        properties_box.pack_start(name_entry_box, False, False, 5.0)

        price_entry_box = Gtk.HBox()
        price_entry_box.pack_start(Gtk.Label('Add Price: '), False, False, 5.0)

        self.price_display = Gtk.SpinButton()
        adjustment = Gtk.Adjustment(0.0, -1 * 100 * 100.0, 100 * 100.0,
                                    0.01, 1, 0)
        self.price_display.set_adjustment(adjustment)
        self.price_display.set_digits(2)

        price_entry_box.pack_start(self.price_display, False, False, 5.0)
        price_entry_box.pack_start(Gtk.Fixed(), False, False, 5.0)

        properties_box.pack_start(price_entry_box, False, False, 5.0)
        main_box.pack_start(properties_box, False, False, 5.0)

        update_button_box = Gtk.HBox()

        update_button = Gtk.Button('UPDATE OPTION')
        update_button.set_can_focus(False)
        update_button.connect('clicked', self.update_option)
        update_button.set_size_request(150, 30)

        update_button_box.pack_end(update_button, False, False, 5.0)
        update_button_box.pack_start(Gtk.Fixed(), False, False, 5.0)
        main_box.pack_start(update_button_box, False, False, 5.0)

        main_box.pack_start(Gtk.Fixed(), False, False, 5.0)

        frame.add(main_box)

        return frame

    def update_category_select(self, selection, model, path, is_selected,
                               user_data=None):
        """Override Method

        Called when a row on the categories view has
        been selected.

        @param selection: Gtk.Selection that represents
        the selection associated with the categories
        view.

        @param model: Gtk.TreeModel that represents the
        model that stores the data associated with the
        categories view.

        @param path: Gtk.TreePath pointing to the row
        that was selected.

        @param is_selected: bool value that represents
        if the order was selected prior to current
        selection.

        @keyword user_data: Default user data passed
        to this method. By default is None.

        @return: bool value representing if the selection
        can be made. Default True
        """
        self.clear_entries()
        return super(UpdateGeneralOptionSelectionDialog,
                     self).update_category_select(selection, model, path,
                                                  is_selected, user_data=user_data)

    def update_option_selection(self, selection, model, path, is_selected,
                                user_data=None):
        """Method called when the option selection area
        has had a selection made. Updates the name and
        price displays for editing.

        @param selection: Gtk.Selection that represents
        the selection associated with the display.

        @param model: Gtk.TreeModel that represents the
        data storage associated with the display

        @param path: Gtk.TreePath pointing to the row
        that was selected.

        @param is_selected: bool value representing if
        the row was selected prior to this current
        selection check.

        @keyword user_data: User data passed to this
        method. Default is None.

        @return: bool value representing if the current
        row can be selected. By default True.
        """
        if not is_selected:
            itr = model.get_iter(path)

            name = model[itr][0]
            price = float(model[itr][1])

            self.name_entry.set_text(name)
            self.price_display.set_value(price)

        return True

    def get_selected_category(self):
        """Get the currently selected category.

        @return: str representing the category
        that has been selected.
        """
        model, itr = self.get_category_view_selected()
        category = model[itr][0]
        return category

    def add_category(self, *args):
        """Adds a new category by with
        the name stored in the category
        entry area.

        @return: str representing the
        category added.
        """
        name = self.category_entry.get_text()
        self.clear_entries()
        name = name.strip().upper()

        if len(name) > 0 and not name in self.option_data:
            self.option_data[name] = []
            self.display_data[name] = Gtk.ListStore(str, str)

            model = self.category_view.get_model()
            itr = model.append((name,))

            self.set_category_selection(itr)

            return name

        return None

    def remove_category(self, *args):
        """Removes the selected category
        from the category list.

        @return: str representing the
        category removed.
        """
        model, itr = self.get_category_view_selected()

        if itr:
            key = model[itr][0]
            option_data = self.option_data[key]

            response = True

            if len(option_data) > 0:
                title = 'Delete ' + key + ' Confirmation?'
                message = 'Deleting ' + key + ' will also remove all' + \
                          ' associated Option Items. Do you want to continue?'
                response = run_warning_dialog(self.dialog, title, message)

            if response:
                del self.option_data[key]
                del self.display_data[key]

                model.remove(itr)

            return key

        return None

    def add_new_option(self, *args):
        """Adds a new option to the
        option data with the generated
        title "NEW OPTION'.

        @return: Gtk.TreeIter pointing to
        the option that was added.
        """
        key = self.get_selected_category()
        option_list = self.option_data[key]

        option_model = self.option_view.get_model()
        itr = option_model.append(('NEW OPTION', str(0.0)))

        option_item = OptionItem('NEW OPTION', key, 0.0)
        option_list.append(option_item)

        self.set_option_selection(itr)
        return itr

    def remove_selected_option(self, *args):
        """Removes the selected option from the
        option data.

        @return: OptionItem that represents
        the selected, removed OptionItem
        """
        key = self.get_selected_category()
        option_list = self.option_data[key]

        model, itr = self.get_option_view_selected()
        if itr:
            path = model.get_path(itr)
            index = path.get_indices()[0]

            model.remove(itr)
            return option_list.pop(index)

        return None

    def update_option(self, *args):
        """Updates the selected option to
        the adjusted name and adjusted price
        generated from the respective entries.

        @return: OptionItem that has been
        updated.
        """
        name = self.name_entry.get_text()
        name = name.strip().upper()

        price = self.price_display.get_value()
        price = float(price)

        model, itr = self.get_option_view_selected()

        self.clear_entries()

        if itr and len(name) > 0:
            key = self.get_selected_category()

            option_list = self.option_data[key]

            path = model.get_path(itr)
            index = path.get_indices()[0]

            option_item = option_list[index]

            option_item._name = name
            option_item._price = price

            model[itr][0] = option_item._name
            model[itr][1] = str(option_item._price)

            return option_item

        return None

    def clear_entries(self):
        """Clears the current text
        displayed in all entries.

        @return: None
        """
        if self.category_view and self.name_entry and self.price_display:
            self.category_entry.set_text('')
            self.name_entry.set_text('')
            self.price_display.set_value(0.0)

    def confirm_data(self, *args):
        """Override Method

        Confirms the updated data
        by calling the given
        confirm func.

        @param args: wildcard catchall
        that is used to catch the
        parameters given to this method.

        @return: None
        """
        self.confirm_func(self.option_data)


#===========================================================
# This block represents module wide functions that are
# utilized in classes throughout this module to perform
# general operations that are useful.
#===========================================================
def get_row_refs(model, paths):
    """Gets a list of Gtk.TreeRowReferences
    associated with the given paths.
    These Gtk.TreeRowReferences are
    independent of changes made in the
    model or treeview.

    @param model: Gtk.TreeModel associated
    with the stored data in the Gtk.TreeView that
    the paths were generated from.

    @param paths: list of Gtk.TreePaths where each
    entry is pointing to an associated data row of
    data in the given model.

    @return: list of Gtk.TreeRowReference objects that
    point to each of the rows in the paths given.
    """
    row_refs = []

    for path in paths:
        row_ref = Gtk.TreeRowReference.new(model, path)
        row_refs.append(row_ref)

    return row_refs


def ensure_top_level_item(model, tree_iter):
    """Ensures that the given iter is a valid iter on the
    given model, and that the iter points to the parent
    most item, that represents the menu item stored in
    the model.

    @param model: Gtk.TreeModel object, that stores the
    given tree_iter.

    @param tree_iter: Gtk.TreeIter object, that represents
    a row in the given model.

    @return: tree_iter pointing to the top_most parent
    of the selected row, or None if the given iter is
    not a row present in the model.
    """

    parent_iter = model.iter_parent(tree_iter)

    if parent_iter:
        return ensure_top_level_item(model, parent_iter)
    return tree_iter


def run_warning_dialog(parent, title, message):
    """Runs a warning dialog window on the given
    parent, with the given title and the given
    message. This warning dialog window allows
    for two possible selections, Yes or No.

    @param parent: Gtk.Object that this warning
    window is being called on.

    @param title: str representing the title to
    be displayed. This title should be a brief
    informative description of the error.

    @param message: str representing the message
    to be displayed warning the user.

    @return: bool value representing True if the
    Yes response was given from the dialog, or
    False if the No response was given.
    """

    buttons = Gtk.ButtonsType.YES_NO
    message_type = Gtk.MessageType.WARNING

    warning_dialog = Gtk.MessageDialog(parent, 0, message_type, buttons, title)
    warning_dialog.format_secondary_text(message)

    response = warning_dialog.run()
    warning_dialog.destroy()

    return response == Gtk.ResponseType.YES