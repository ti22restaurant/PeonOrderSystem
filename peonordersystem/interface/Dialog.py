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

@group CheckoutConfirmationDialog: This group represents all subclasses
of the CheckoutConfirmationDialog. These are all classes that instantiate
some form of the CheckoutConfirmationDialog windows. These differ from other
types of dialog windows because they rely on functionality from the group
CheckoutConfirmationDialog.

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
from peonordersystem.CustomExceptions import InvalidOrderError

STANDARD_TEXT = 500
STANDARD_TEXT_BOLD = 850

SPLIT_CHECK_DIALOG_RESPONSE = 99


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
        scrolled_window = Gtk.ScrolledWindow()
        model = self.generate_model()
        
        self.tree_view = Gtk.TreeView(model)
        column_list = self.generate_columns()
        
        for column in column_list:
            self.tree_view.append_column(column)

        scrolled_window.add(self.tree_view)

        selection = self.tree_view.get_selection()
        selection.set_select_function(self._select_method, None)

        return scrolled_window
    
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

    @abstractmethod
    def confirm_data(self):
        """Abstract Method. Called to confirm the confirmation
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
        return super(ConfirmationDialog, self).cancel_button_clicked()

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
        priority_button = Gtk.Button('Add Priority')
        priority_button.set_size_request(200, 50)
        priority_button.connect('clicked', self._set_selected_priority)
        button_box.pack_start(priority_button, False, False, 5)

        main_box.pack_start(button_box, False, False, 5)

        return main_box

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
        # Contingency: Absurdly long notes stored in a
        # MenuItem object. Solution: wrap text
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

        for menu_item in self.order_list:

            info = menu_item.get_name(), str(menu_item.stars), STANDARD_TEXT
            treeiter = tree_model.append(None, info)

            if menu_item.has_options():

                # Get string of options. Slice brackets from front and back
                info = str(menu_item.options)[1:-1], None, STANDARD_TEXT
                tree_model.append(treeiter, info)

            if menu_item.has_note():

                info = menu_item.notes, None, STANDARD_TEXT
                tree_model.append(treeiter, info)
        
        return tree_model

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

        sub_box = self.generate_related_buttons()

        main_box.pack_start(sub_box, False, False, 5)

        return main_box

    def generate_related_buttons(self):
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
        total = CheckOperations.get_total(self.order_list)
        
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
        model, paths = selection.get_selected_rows()

        total_path = self.total_row_reference.get_path()

        if total_path in paths:
            paths.remove(total_path)

        return model, paths

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
            menu_item.hash = hash(menu_item)
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

    def generate_related_buttons(self):
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
                    print curr_menu_item

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
        all contain values for MenuItem.hash

        @return: list of MenuItem objects that have been
        sorted according to their MenuItem.hash values.
        If two items shared the same MenuItem.hash value
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

                if first_item.hash == second_item.hash:
                    first_item.edit_price(first_item.get_price() + second_item.get_price())
                    result.append(first_item)
                    first_index += 1
                    second_index += 1
                else:

                    if first_item.hash < second_item.hash:
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

    
class AddReservationsDialog(Dialog):
    """AddResdervationsDialog prompts the user with
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