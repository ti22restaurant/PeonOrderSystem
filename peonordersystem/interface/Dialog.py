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

from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport

from abc import ABCMeta, abstractmethod
from copy import copy, deepcopy
import time
import math

from peonordersystem import CheckOperations
from peonordersystem.MenuItem import MenuItem

#========================================================
# This block represents module wide constants that are
# utilized inside and outside of this module to determine
# the text weight and responses of the classes and other
# information.
#========================================================

STANDARD_TEXT_LIGHT = 200
STANDARD_TEXT = 500
STANDARD_TEXT_BOLD = 850

SPLIT_CHECK_DIALOG_RESPONSE = 99

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
            self.dialog.set_default_size(default_size[0],
                                        default_size[1])

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
        """ Abstract Method. Represents the callback
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
        t = time.localtime()
        hour = t[3]

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

        for number in range(hour, 24):
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
        name, number, and time in secs since epoch, respectively.
        """
        name = self.name_entry.get_text()
        number = self.number_entry.get_text()

        hour = int(self.hour_combo_box.get_active_text())

        minute = int(self.min_combo_box.get_active_text())

        t = time.localtime()

        while minute < t[4]:
            minute += 30

        t = time.mktime(t[:3] + (hour, minute, 0) + t[6:])

        return name, number, t

    def confirm_button_clicked(self, *args):
        """Callback method called when the confirm button has been
        clicked.

        @param *args: wildcard that represents a catch all for the
        widget that emitted the call.
        """
        has_hour = self.hour_combo_box.get_active() > -1
        has_min = self.min_combo_box.get_active() > -1

        if has_hour and has_min:
            super(AddReservationsDialog, self).confirm_button_clicked()
            self.confirm_func(self.get_information())

    def cancel_button_clicked(self, *args):
        """Callback method called when the cancel button
        has been clicked.

        @param *args: wildcard catch all that is used to catch
        the widget that emitted this call.
        """
        super(AddReservationsDialog, self).cancel_button_clicked()


class UpdateMenuItemsDialog(Dialog):
    """UpdateMenuItemDialog interacts with the user
    to display information and receive information to
    update the stored menu item data for the PeonOrderSystem
    UI.

    This window expects menu item data to be in a specific
    form. It then operates on that menu item data, finally
    calling the given confirm func upon confirmation from
    the user.

    @group Dialog: This window is a subclass member of the
    Dialog group. Any changes to the Dialog class could effect
    the functionality of this window.

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

    @var item_view: Gtk.TreeView object that is used to
    display the information of the MenuItem objects to
    be selected and editing by the user.
    """

    def __init__(self, parent, menu_item_data, confirm_func,
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

        @param confirm_func: function that is to be called upon
        confirmation.

        @param title: str representing the title to be displayed
        by this dialog window.
        """
        self.menu_item_data = menu_item_data
        self.confirm_func = confirm_func
        self.model_data = None

        self.categories_name_entry = None
        self.item_name_entry = None
        self.price_spin_button = None
        self.stars_spin_button = None

        self.is_editable_switch = None
        self.is_confirmed_switch = None

        self.categories_view = None
        self.item_view = None

        super(UpdateMenuItemsDialog, self).__init__(parent, title,
                                                    default_size=(1100, 600))

    def generate_layout(self):
        """Override Method.

        Generates the layout that is to be
        added to the content area of the main
        dialog window.

        @return: Gtk.Container that holds all
        associated widgets to be displayed in
        the dialog's content area.
        """
        main_box = Gtk.HBox()

        selection_sub_box = Gtk.HBox()
        categories_display = self.generate_categories_display()
        selection_sub_box.pack_start(categories_display, True, True, 5.0)

        item_display = self.generate_item_display()
        selection_sub_box.pack_start(item_display, True, True, 5.0)

        main_box.pack_start(selection_sub_box, True, True, 5.0)

        properties_display = self.generate_properties_display()
        main_box.pack_start(properties_display, True, True, 5.0)

        return main_box

    def generate_properties_display(self):
        """Generates the display associated
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
        adjustment = Gtk.Adjustment(0.0, 0, 100**100, .01, 1, 1)
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
        update_changes_button.connect('clicked', self.update_item)
        update_changes_button.set_size_request(150, 35)
        update_changes_button.set_can_focus(False)
        update_changes_box.pack_end(update_changes_button, False, False, 5.0)
        properties_box.pack_end(update_changes_box, False, False, 5.0)

        properties_frame.add(properties_box)
        options_box.pack_start(properties_frame, False, False, 5.0)

        option_choices_box = Gtk.VBox()

        #TODO add option choices

        options_box.pack_start(option_choices_box, True, True, 5.0)

        return options_box

    def toggle_stars_editable_display(self, switch_widget, *args):
        """Toggles if the stars editable display should become
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

    def generate_item_display(self):
        """Generates the display associated
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
        remove_menu_item_button.connect('clicked', self.remove_selected_item)
        remove_menu_item_button.set_can_focus(False)
        remove_menu_item_button.set_size_request(100, 50)
        menu_items_edit_box.pack_end(remove_menu_item_button, False, False, 5.0)

        menu_items_edit_frame.add(menu_items_edit_box)

        menu_items_display_box.pack_start(menu_items_edit_frame, False, False, 5.0)

        return menu_items_display_box

    def generate_categories_display(self):
        """Generates the display associated
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
        categories_edit_subbox1.pack_start(self.categories_name_entry, False, False, 5.0)
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
        categories_edit_subbox2.pack_start(remove_category_button, False, False, 5.0)

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
        model = self.generate_categories_model()
        tree_view.set_model(model)

        col_list = self.generate_columns(('Category',))

        for col in col_list:
            tree_view.append_column(col)

        selection = tree_view.get_selection()
        selection.set_select_function(self.category_selected, None)

        return tree_view

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

    def generate_item_view(self):
        """Generates the item view to display
        the MenuItem information.

        @return: Gtk.TreeView associated with
        the item view generated.
        """
        tree_view = Gtk.TreeView()
        self.generate_item_model()

        col_list = self.generate_columns(('Menu Item',))

        for col in col_list:
            tree_view.append_column(col)

        selection = tree_view.get_selection()
        selection.set_select_function(self.item_selected, None)

        return tree_view

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
        itr = model.get_iter(path)

        name = model[itr][0]
        price = model[itr][1]
        stars = model[itr][2]
        editable = model[itr][3]
        confirmed = model[itr][4]

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

        return True

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

    def generate_item_model(self):
        """Generates and populates the
        models to display the items
        associated with each category.

        @return: None
        """
        self.model_data = {}

        for category in self.menu_item_data:
            model = Gtk.ListStore(str, float, int, bool, bool)

            for menu_item in self.menu_item_data[category]:

                name = menu_item._name
                price = menu_item._price
                stars = menu_item.stars
                editable = menu_item.editable
                confirmed = menu_item.confirmed

                values = name, price, stars, editable, confirmed

                model.append(values)

            self.model_data[category] = model

    def generate_columns(self, col_names):
        """Generates the Gtk.TreeViewColumns
        to be displayed and returns them as a
        list.

        @param col_names: list of str that represents
        the titles to be have columns generated for.

        @return: list of Gtk.TreeViewColumn that
        represents the columns to be added to
        view for display.
        """
        col_list = []

        for each in col_names:
            rend = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(each, rend, text=0)

        col_list.append(col)

        return col_list

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
        model = self.item_view.get_model()

        model.append(('NEW MENU ITEM', 0.0, 0, False, False))

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
        selection = self.item_view.get_selection()
        model, itr = selection.get_selected()

        if itr:
            model.remove(itr)

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

        if len(text) > 0:
            model = self.categories_view.get_model()
            model.append((text, ))
            new_model = Gtk.ListStore(str, float, int,
                                      bool, bool)
            self.model_data[text] = new_model

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

        response = True

        if len(self.model_data[key]) > 0:
            message_title = 'Removing ' + key + ' will delete all associated Menu Items'
            message = 'If you remove the category ' + key + ' all Menu Items contained' + \
                      ' within this category will also be deleted. ' + \
                      ' This cannot be undone!\n\nDo you want to continue?'
            warning_dialog = Gtk.MessageDialog(self.dialog, 0, Gtk.MessageType.WARNING,
                                               Gtk.ButtonsType.YES_NO, message_title)
            warning_dialog.format_secondary_text(message)
            response = warning_dialog.run() == Gtk.ResponseType.YES
            warning_dialog.destroy()

        if response:
            model.remove(itr)
            del self.model_data[key]

    def update_item(self, *args):
        """Updates the item that has been
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
            model[itr][0] = name.upper()

            model[itr][1] = self.price_spin_button.get_value()
            model[itr][2] = self.stars_spin_button.get_value_as_int()
            model[itr][3] = self.is_editable_switch.get_active()
            model[itr][4] = not self.is_confirmed_switch.get_active()

    def confirm_button_clicked(self, *args):
        """Override Method.

        Called when the confirm button has been
        clicked. This method performs the confirmation
        process by calling the confirm_data method.

        @param args: wildcard catchall to catch the
        Gtk.Widget that called this method.

        @return: None
        """
        super(UpdateMenuItemsDialog, self).confirm_button_clicked()
        self.confirm_data()

    def confirm_data(self):
        """Confirm data method is called
        when the confirm button has been clicked.
        This method calls the confirm_func stored
        in the object with object specific parameters
        passed as arguments.

        @return: dict of str to lists. Each key is a
        str that represents the category, and each
        value is a list of MenuItem objects that represents
        the MenuItem objects associated with that category.
        """
        updated_menu_data = {}

        category_model = self.categories_view.get_model()
        category_itr = category_model.get_iter_first()

        while category_itr:

            item_list = []

            key = category_model[category_itr][0]
            updated_menu_data[key] = item_list
            item_model = self.model_data[key]

            item_itr = item_model.get_iter_first()

            while item_itr:

                name = item_model[item_itr][0]
                price = round(item_model[item_itr][1] * 100) / 100
                stars = item_model[item_itr][2]
                editable = item_model[item_itr][3]
                confirmed = item_model[item_itr][4]

                menu_item = MenuItem(name, price, stars,
                                     editable, confirmed)

                item_list.append(menu_item)

                item_itr = item_model.iter_next(item_itr)

            category_itr = category_model.iter_next(category_itr)

        self.confirm_func(updated_menu_data)

    def cancel_button_clicked(self, *args):
        """Override Method.

        Method called when the cancel button
        has been clicked. This method calls
        the cancel data method.

        @param args: wildcard catchall that
        is used to catch the Gtk.Widget that
        called this method.

        @return: None
        """
        super(UpdateMenuItemsDialog, self).cancel_button_clicked()


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
    
    def set_layout(self, content_boxes):
        """Sets the layout for the OptionsEntryDialog. Each
        content box in the content_area of the dialog window
        is set to store option toggles in groups of three
        distributed among the three given content boxes stored
        in content_boxes.
        
        @param content_boxes: list where each entry represents
        a box in the subdivided content area of the main EntryDialog.
        There are by default three content boxes stored in content_boxes.

        @return: None
        """
        for option in self.menu_item.get_option_choices():
            button_box = content_boxes.pop(0)
            option_toggle = Gtk.ToggleButton(option)
            
            if option in self.menu_item.options:
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
            self.options.append(button.get_label())
        # case 2: Button is inactive (therefore was toggled)
        else:
            self.options.remove(button.get_label())
    
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

                # Get string of options. Slice brackets from front and back
                info = str(menu_item.options)[1:-1], None, STANDARD_TEXT
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
        sub_box = Gtk.HBox()

        button = Gtk.Button("SPLIT CHECK")
        button.set_size_request(200, 20)
        button.connect('clicked', self._split_check_dialog)
        sub_box.pack_start(button, False, False, 0)

        return sub_box

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

    def _split_check_dialog(self, *args):
        """Private Method.

        Called when the split check button has
        been pressed. This method eliminates
        the current dialog and emits the
        appropriate response.

        @param args: wildcard catchall to catch
        the Gtk.Widget that called this method.

        @return: None
        """
        self.dialog.response(SPLIT_CHECK_DIALOG_RESPONSE)
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
                option_dict = menu_item.get_option_choices()
                for key in option_dict:
                    option_price = option_dict[key]
                    model.append(location, (key, str(option_price), True))

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
            for each in self.name_list:
                self.model.append(each)

        return self.model

    def add_new_order(self, *args):
        """Callback Method that is called when
        the add new order button is clicked.

        @param *args: wildcard that represents a
        catch all. The first argument is the
        widget that emitted the signal
        """
        name = self.name_entry.get_text()
        number = self.number_entry.get_text()
        if name is not '' and number is not '':
            t = time.strftime('%X, %A, %m/%y')
            new_order = (name, number, t)

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
            return model.get(itr, 0, 1, 2)

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
        text_view_frame = Gtk.Frame()
        self.message_entry = Gtk.TextView()
        self.message_entry.set_size_request(250, 150)
        self.message_entry.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view_frame.add(self.message_entry)
        discount_message_box.pack_start(text_view_frame, False, False, 0.0)

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

            discount_item = MenuItem(name, -1 * price)
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
    """UpdateTemplateDiscountCheckoutConfirmationDialog is a window that allows the
    user to update the templates stored and accessed by the DiscountCheckoutConfirmationDialog
    window.

    @warning: This class is not intended to be inherited from. This class instantiates
    all of its functionality primarily from its super classes. As well its inheritance
    tree is considered large enough that it would be unwise to continue inheritance.

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
        if len(name) > 0:
            value, is_percentage = self.parse_discount_data()

            value_str = str(value)

            if is_percentage:
                value_str += '%'
            else:
                value_str = '$' + value_str

            data = name, value_str, value, is_percentage

            tree_model = self.tree_view.get_model()
            tree_model.append(data)

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
            model.remove(itr)

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