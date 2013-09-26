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
This differ from the EntryDialogs as they are simply confirmations
of a current orders list and do not allow for adjustment

@group ReservationsDialog: This group represents all classes
of the ReservationsDialog window. ReservationsDialog group are
subclass members of the Dialog group

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport

from abc import ABCMeta, abstractmethod

from collections import deque

from copy import copy

import time


STANDARD_TEXT = 100
STANDARD_TEXT_BOLD = 700


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
            cancel_button.set_size_request(80, 50)
            confirm_button = Gtk.Button('Confirm')
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
        
        @return: widget representing the top level
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
        
        @return: HBox representing the
        content area of the window dialog. 
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
        """
        pass
    
    def confirm_button_clicked(self, *args):
        """Callback method that is called when the confirmed
        button is clicked. This method calls the confirm_data
        method and superclass confirm_button_clicked method
        
        @param *args: wildcard that represents the confirmed
        button widget
        """
        self.confirm_data()
        super(EntryDialog, self).confirm_button_clicked(*args)
    
    def cancel_button_clicked(self, *args):
        """Callback method that is called when the cancel
        button is clicked. This method calls the cancel_data
        method and superclass cancel_button_clicked method
        
        @param *args: wildcard that represents the cancel
        button widget
        """
        self.cancel_data()
        super(EntryDialog, self).cancel_button_clicked(*args)
    
    @abstractmethod
    def confirm_data(self):
        """Abstract Method that is called whenever
        the confirm button has been clicked. After
        completion the window is unaccessible to the
        user
        
        """
        pass
    
    @abstractmethod
    def cancel_data(self):
        """Abstract Method that is called whenever
        the cancel button has been clicked. After
        completion the window is unaccessible to the
        user.
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
        super(OptionEntryDialog, self).__init__(parent, title,
                                                dialog)
    
    def set_layout(self, content_boxes):
        """Sets the layout for the OptionsEntryDialog. Each
        content box in the content_area of the dialog window
        is set to store option toggles in groups of three
        distributed among the three given content boxes stored
        in content_boxes.
        
        @param content_boxes: list where each entry represents
        a box in the subdivided content area of the main EntryDialog.
        There are by default three content boxes stored in content_boxes.
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
        
        @param button: widget that represents the button
        toggled.
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
        
        @return: 
        """
        return super(OptionEntryDialog, self).cancel_data()
    
    def confirm_data(self):
        """Confirms the selected options and stored them
        in the MenuItem's options attribute
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
        super(NoteEntryDialog, self).__init__(parent, title,
                                              dialog)
        
    def generate_layout(self):
        """Overrides generate_layout. This method generates the
        custom NoteEntryDialog layout and then populates that 
        layout with components via the set_layout method.
        
        @return: Gtk.VBox representing the main content area
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
        
        @param content_area: Gtk.VBox that fills the entire content
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
        super(StarEntryDialog, self).__init__(parent, title,
                                              dialog)
    
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
    
    def decrease_star_value(self, widget):
        """Callback method when decrease button 
        is clicked. Reduces the temporary star 
        level by one. This value is not stored
        in the star value of the MenuItem object.
        
        @param widget: Gtk.Button representing the
        given widget that called this method.
        """
        self.stars_value = self.stars_value - 1
        self.update_star_label()
        
        
    def increase_star_value(self, widget):
        """Callback method when the increase button
        is clicked. Increases the temporary star
        level by one. This value is not stored
        in the star value of the MenuItem object.
        """
        self.stars_value = 1 + self.stars_value
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
    
    def __init__(self, parent, title, confirm_func, dialog=None,
                 default_size=(600, 700)):
        """Initializes the Abstract Base functionality
        of the ConfirmationDialog.
        
        @param title: str representing the title to be
        displayed on the dialog window.
        
        @param parent: Object representing the object
        that the Gtk.Dialog was called on. Expected 
        Gtk.Window
        
        @param confirm_func: Pointer to callback function
        called when the dialog has been confirmed.
        """
        self.confirm_func = confirm_func
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
        
        self.tree_view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        for column in column_list:
            self.tree_view.append_column(column)

        scrolled_window.add(self.tree_view)

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
        is clicked. Calls base functionality and
        confirm_func passed in as a parameter in
        the constructor
        
        @param *args: Gtk.Widget wildcard representing
        the component or Gtk.Widget that emitted the
        signal and called this method.
        
        @attention: Calls function external to object.
        Possible unintended consequences based on value
        passed in.

        @return: expected int that represents
        Gtk.ResponseType of the dialog
        """
        return super(ConfirmationDialog, self).confirm_button_clicked()
    
    def cancel_button_clicked(self, *args):
        """Callback Method that is called when
        the cancel button is clicked. This method
        calls on base functionality.
        
        @param *args: Gtk.Widget wildcard that represents
        the component or Gtk.Widget that emitted
        this signal and called this method.

        @return: expected int that represents t
        he Gtk.ResponseTypeof the dialog.
        """
        return super(ConfirmationDialog, self).cancel_button_clicked()

    def get_selected(self):
        """ Gets the currently selected item
        from the tree_view.

        @return: 2-tuple (Gtk.TreeModel, Gtk.TreeIter)
        representing the associated model and an iter
        pointing to the selected row.
        """
        selection = self.tree_view.get_selection()
        return selection.get_selected()

    def _ensure_top_level_item(self, model, tree_iter):
        """ Private Method.

        Ensures that the given iter is a valid iter on the
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
        if model.iter_is_valid(tree_iter):
            parent_iter = model.iter_parent(tree_iter)

            if parent_iter != None:
                return self._ensure_top_level_item(model, parent_iter)
            return tree_iter

        return None


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
        def is_confirmed(menu_item):
            return not menu_item.confirmed
        self. total_row_reference = None
        self.order_list = filter(is_confirmed, order_list)
        super(OrderConfirmationDialog, self).__init__(parent, title,
                                                      confirm_func, dialog)

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

    def confirm_button_clicked(self, *args):
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

        return super(OrderConfirmationDialog, self).confirm_button_clicked(args)

    def _set_selected_priority(self, *args):
        """Private Method.

        Toggles the priority level stored in the
        selected items.

        @param args: wildcard catchall that catches
        the widget that activated this method.

        @return: None
        """
        model, itr = self.get_selected()

        itr = self._ensure_top_level_item(model, itr)
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
        super(CheckoutConfirmationDialog, self).__init__(parent, title,
                                                         confirm_func,
                                                         dialog)
    
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
        col1 = Gtk.TreeViewColumn('MenuItem',
                                  renderer1, text=0)
        column_list.append(col1)
        
        renderer2 = Gtk.CellRendererText()
        col2 = Gtk.TreeViewColumn('Price',
                                  renderer2, text=1)
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
        
        tree_model = Gtk.TreeStore(str, str)
        
        total = 0
        
        for menu_item in self.order_list:
            name = menu_item.get_name()
            price = menu_item.get_price()
            total = total + price
            treeiter = tree_model.append(None,
                                         (name, str(price)))
            if menu_item.has_options():
                option_dict = menu_item.get_option_choices()
                for option in menu_item.options:
                    option_price = option_dict[option]
                    total = total + option_price
                    tree_model.append(treeiter, (option,
                                                 str(option_price)))
                    
        total = CheckOperations.get_total(self.order_list)
        itr = tree_model.append(None, ('Total', str(total)))
        self.total_row_reference = Gtk.TreeRowReference.new(tree_model,
                                                            tree_model.get_path(itr))
        
        return tree_model

    def confirm_button_clicked(self, *args):
        super(CheckoutConfirmationDialog, self).confirm_button_clicked()
        self.confirm_func()


    
    def _check_row_changed(self, added_itr=None):
        
        model = self.tree_view.get_model()
        total = CheckOperations.get_total(self.order_list)
        
        path = self.total_row_reference.get_path()
        itr = model.get_iter(path)
        
        model[itr][1] = str(total)
        
        if added_itr != None:
            model.swap(added_itr, itr)
    
class SplitCheckConfirmationDialog(CheckoutConfirmationDialog):
    
    def __init__(self, parent, confirm_func, order_list, dialog=None,
                 title='Split Check'):
        self.check_dict = {}
        self.checks_view = None
        self.items_view = None
        
        super(SplitCheckConfirmationDialog, self).__init__(parent,
            confirm_func, order_list, dialog=dialog, title=title)
        
        self.dialog.set_default_size(1100, 700)
        self.items_view = self.tree_view
    
    def generate_layout(self):
        main_box = Gtk.VBox()
        
        lower_sub_box1 = Gtk.HBox()
        lower_sub_box2 = Gtk.HBox()
        
        select_all_button1 = Gtk.Button('SELECT ALL')
        select_all_button1.connect('clicked', self.items_select_all)
        select_all_button1.set_size_request(200, 40)
        lower_sub_box1.pack_start(select_all_button1, False, False, 5)
        
        select_all_button2 = Gtk.Button('SELECT ALL')
        select_all_button2.set_size_request(200, 40)
        select_all_button2.connect('clicked', self.checks_select_all)
        lower_sub_box1.pack_end(select_all_button2, False, False, 5)
        
        remove_check_button = Gtk.Button('REMOVE CHECK')
        remove_check_button.connect('clicked', self.remove_selected_check)
        remove_check_button.set_size_request(200, 40)
        lower_sub_box2.pack_end(remove_check_button, False, False, 5)
        
        add_check_button = Gtk.Button("ADD CHECK")
        add_check_button.connect('clicked', self.add_new_check)
        add_check_button.set_size_request(200, 40)
        lower_sub_box2.pack_end(add_check_button, False, False, 5)
        
        main_box.pack_end(lower_sub_box2, False, False, 5)
        main_box.pack_end(lower_sub_box1, False, False, 5)
        
        
        center_sub_box = Gtk.HBox()
        
        items_scroll_window = super(SplitCheckConfirmationDialog,
                                    self).generate_layout()
        center_sub_box.pack_start(items_scroll_window, True, True, 5)
        
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
        
        checks_scroll_window = self.generate_check_treeview()
        center_sub_box.pack_start(checks_scroll_window, True, True, 5)
        
        main_box.pack_end(center_sub_box, True, True, 5)
        
        top_sub_box = Gtk.HBox()
        
        item_label = Gtk.Label('ITEMS')
        top_sub_box.pack_start(item_label, False, False, 5)
        check_label = Gtk.Label('CHECKS')
        top_sub_box.pack_end(check_label, False, False, 5)
        
        main_box.pack_end(top_sub_box, False, False, 5)
        
        main_box.show_all()
        
        return main_box
    
    def generate_check_treeview(self):
        scroll_window = Gtk.ScrolledWindow()
        self.checks_view = Gtk.TreeView()
        
        self.checks_view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        col_list = self.generate_check_columns()
        
        for column in col_list:
            self.checks_view.append_column(column)
        
        model = self.generate_check_model()
        self.checks_view.set_model(model)
        
        scroll_window.add(self.checks_view)
        
        return scroll_window
    
    def generate_check_columns(self):
        col_list = []
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Items', rend, text=0)
        col_list.append(col)
        
        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Price', rend, text=1)
        col_list.append(col)
        
        return col_list
    
    def generate_check_model(self):
        tree_model = Gtk.TreeStore(str, str)
        return tree_model
    
    def _get_check_selected(self, *args):
        selection = self.checks_view.get_selection()
        return selection.get_selected_rows()
    
    def checks_select_all(self, *args):
        pass
    
    def items_select_all(self, *args):
        self.tree_view.get_selection().select_all()
    
    def add_new_check(self, *args):
        model = self.checks_view.get_model()
        key = 'Check ' + str(len(self.check_dict) + 1)
        
        self.check_dict[key] = deque()
        itr = model.append(None, (key, '0.0'))
    
    def remove_selected_check(self, *args):
        model, paths = self._get_check_selected()
        rows = []
        for path in paths:
            rows.append(Gtk.TreeRowReference.new(model, path))
        
        for row in rows:
            path = row.get_path()
            itr = model.get_iter(path)
            itr = self._ensure_top_level(model, itr)
            
            key = model[itr][0]
            
            if key in self.check_dict:
                self.pull_items()
                model.remove(itr)
                del self.check_dict[key]
                
    def _get_item_at_index(self, key, index):
        current_order = self.check_dict[key]
        current_order.rotate(-index)
        menu_item = current_order.popleft()
        current_order.rotate(index)
        return menu_item
        
    
    def push_items(self, *args):
        item_model, item_paths = self._get_items_selected()
        check_model, check_paths = self._get_check_selected()
        
        if len(item_paths) > 0 and len(check_paths) > 0:
            
            rows = []
            for item_path in item_paths:
                row_ref = Gtk.TreeRowReference.new(item_model, item_path)
                rows.append(row_ref)
                
            for row_ref in rows:
                item_path = row_ref.get_path()
                item_iter = item_model.get_iter(item_path)
                index = item_path.get_indices()[0]
                
                item_model.remove(item_iter)
                menu_item = self.order_list.pop(index)
                
                name = menu_item.get_name()
                price = menu_item.get_price()
                price = math.ceil(price / len(check_paths) * 100) / 100
                
                menu_item.edit_price(price)
                
                for check_path in check_paths:
                    check_iter = check_model.get_iter(check_path)
                    check_iter = self._ensure_top_level(check_model, check_iter)
                    
                    key = check_model[check_iter][0]
                    check_list = self.check_dict[key]
                    check_list.appendleft(menu_item)
                    
                    check_model.prepend(check_iter,
                                       (name, str(price)))
                    
                    self._check_row_changed(check_model, check_iter)
                    super(SplitCheckConfirmationDialog, self)._check_row_changed()
        
    
    def pull_items(self, *args):
        model, paths = self._get_check_selected()
        
        if len(paths) > 0:
            parent_iter = None
            rows = []
            
            for path in paths:
                
                itr = model.get_iter(path)
                
                if model.iter_has_child(itr):
                    parent_iter = itr
                    key = model[itr][0]
                    itr = model.iter_children(itr)
                    
                    while itr != None:
                        path = model.get_path(itr)
                        index = path.get_indices()[1]
                        row_ref = Gtk.TreeRowReference.new(model, path)
                        rows.append((key, index, row_ref))
                        itr = model.iter_next(itr)
                
                else:
                    parent_iter = model.iter_parent(itr)
                    key = model[parent_iter][0]
                    
                    path = model.get_path(itr)
                    index = path.get_indices()[1]
                    row_ref = Gtk.TreeRowReference.new(model, path)
                    rows.append((key, index, row_ref))
            
            for row in rows:
                key = row[0]
                index = row[1]
                row_ref = row[2]
                
                path = row_ref.get_path()
                itr = model.get_iter(path)
                
                model.remove(itr)
                
                menu_item = self._get_item_at_index(key, index)
                name = menu_item.get_name()
                price = menu_item.get_price()
                
                
                self.order_list.append(menu_item)
                
                item_model = self.tree_view.get_model()
                added_itr = item_model.append(None, (name, str(price)))
                
                self._check_row_changed(model, parent_iter)
                super(SplitCheckConfirmationDialog, self)._check_row_changed(added_itr)
        
    
    def _check_row_changed(self, tree_model, itr, *args):
        if itr != None and tree_model.iter_is_valid(itr):
            
            parent_iter = tree_model.iter_parent(itr)
            
            if parent_iter == None:
                parent_iter = itr
            
            if tree_model.iter_has_child(parent_iter):
                check_name = tree_model[parent_iter][0]
                
                current_order = self.check_dict[check_name]
                
            tree_model[parent_iter][1] = str(CheckOperations.get_total(current_order))
            
    
    def _ensure_top_level(self, model, itr):
        
        parent_iter = model.iter_parent(itr)
        
        if parent_iter != None:
            return parent_iter
        
        return itr
    
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
    """
    def __init__(self, parent, confirm_func, name_list):
        """Initializes a new OrderSelectionConfirmationDialog window.
        
        @param parent: subclass of Gtk.Window that the 
        Dialog will be a child of.
        
        @param confirm_func: function pointer that is to be
        called when the dialog window has been confirmed.
        
        @param name_list: list of 3-tuples representing the
        names on the OrderSelection list. This tuple is of (str, str, str)
        where each entry represents the (name, number, time) that
        the order was placed.
        
        """
        self.name_list = name_list
        self.name_entry = None
        self.number_entry = None
        self.model = None
        super(OrderSelectionConfirmationDialog, self).__init__(parent,
                                                     'To Go Selection',
                                                     confirm_func)
    
    def generate_layout(self):
        """Generates the layout for the dialog window.
        
        @return: Gtk.VBox representing the box to be
        added to the content area of the dialog window.
        """
        main_box = Gtk.VBox()
        scrolled_window = super(OrderSelectionConfirmationDialog,
                                self).generate_layout()
        main_box.pack_start(scrolled_window, True, True, 5)
        
        name_label = Gtk.Label('NAME: ')
        number_label = Gtk.Label('NUMBER: ')
        
        sub_box = Gtk.HBox()
        sub_box.set_homogeneous(True)
        sub_box.pack_start(name_label, True, True, 5)
        sub_box.pack_start(number_label, True, True, 5)
        
        main_box.pack_start(sub_box, False, False, 5)
        
        self.name_entry = Gtk.Entry()
        self.number_entry = Gtk.Entry()
        
        sub_box = Gtk.HBox()
        sub_box.set_homogeneous(True)
        sub_box.pack_start(self.name_entry, True, True, 5)
        sub_box.pack_start(self.number_entry, True, True, 5)
        
        main_box.pack_start(sub_box, False, False, 5)
        
        add_new_button = Gtk.Button('Add')
        add_new_button.set_size_request(150, 50)
        add_new_button.connect('clicked', self.add_new_order)
        
        sub_box = Gtk.HBox()
        sub_box.set_homogeneous(True)
        sub_box.pack_start(add_new_button, True, True, 5)
        sub_box.pack_start(Gtk.Fixed(), True, True, 5)
        sub_box.pack_start(Gtk.Fixed(), True, True, 5)
        
        main_box.pack_start(sub_box, False, False, 5)
        
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
            self.confirm_button_clicked(args[0], order=new_order)
    
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
        return model.get(itr, 0, 1, 2)
    
    def confirm_button_clicked(self, widget, order=None):
        """Callback Method that is called when the confirm
        button is clicked. 
        
        @param widget: Gtk.Button that emitted the signal and
        called this method
        
        @keyword order: Default None. Expected 3-tuple that
        represents the (str, str, str) of the given order.
        """
        if order is None:
            order = self.get_selected()
        self.confirm_func(order)
        super(OrderSelectionConfirmationDialog, self).confirm_button_clicked()

    
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
    
    def __init__(self, parent, *args):
        """initializes a new AddReservationsDialog that
        the user may interact with to add a new reservation
        to the reservations list.
        
        @param parent: Gtk.Window that the dialog will be
        a child of
        
        @param *args: wildcard for unexpected parameters
        """
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
            minute = minute + 30
        
        t = time.mktime(t[:3] + (hour, minute, 0) + t[6:])
        
        return name, number, t
    
    def confirm_button_clicked(self, *args):
        """Callback method called when the confirm button has been
        clicked.
        
        @param *args: wildcard that represents a catch all for the
        widget that emitted the call.
        """
        super(AddReservationsDialog, self).confirm_button_clicked()
        
    def cancel_button_clicked(self, *args):
        """Callback method called when the cancel button
        has been clicked.
        
        @param *args: wildcard catch all that is used to catch
        the widget that emitted this call.
        """
        super(AddReservationsDialog, self).cancel_button_clicked()
    
    def run_dialog(self):
        """Runs the current dialog window
        
        @attention: returns an empty 3-tuple if the signal
        emitted was a cancellation of the dialog window.
        
        @return: 3-tuple representing the newly added reservation
        in the (str, str, float) form representing name, number, 
        and secs from the epoch respectively.
        """
        signal = super(AddReservationsDialog, self).run_dialog()
        if signal is int(Gtk.ResponseType.ACCEPT):
            return self.get_information()
        return None, None, None

if __name__ == '__main__':
    
    def boom(*args):
        print 'Confirmed!'
    
    from peonordersystem.MenuItem import MenuItem
    
    order = []
    
    for _ in range(3):
        order.append(MenuItem('Carls Item', 10.0))
        order.append(MenuItem('Loras Item', 10.0))
        order.append(MenuItem('Bobs Item', 10.23))
    
    
    dialog = SplitCheckConfirmationDialog(None, boom, order)
    dialog.run_dialog()
                                          
