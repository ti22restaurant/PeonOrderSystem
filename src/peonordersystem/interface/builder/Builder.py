"""This module provides the Builder
class that is used to create the main
GUI for the user to interact with.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import jsonpickle
jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
from gi.repository import Gtk

from .abc.Builder import AbstractBuilder
from .parsers.DataParser import DataParser
from .connectors.Connector import Connector
from .misc.MenuButton import MenuButton

from .containers.MenuContainer import MenuContainer
from .containers.components.MenuComponent import MenuComponent
from .containers.components.areas.ItemsArea import ItemsArea

from src.peonordersystem.path import MAIN_UI_PATH
from src.peonordersystem.Settings import NUM_OF_TABLES_TO_DISPLAY


class Builder(AbstractBuilder):
    """Creates and connects the main
    GUI to the connected reference.
    Controls the data displayed in
    the main parts of GUI.
    """

    BORDER_SEPARATOR_VALUE = 2.5

    def __init__(self, title):
        """Initializes the Builder"""
        self._title = title
        self._gtk_builder = Gtk.Builder()
        self._gtk_builder.add_from_file(MAIN_UI_PATH)

        self._status_label = None
        self._order_label = None

        self._connector = Connector()
        self._data_parser = DataParser()

        self._menu_notebook = self._set_up_menu_notebook()
        self._set_up()

    def _set_up_menu_notebook(self):
        """Sets up the menu notebook.

        @return: MenuContainer that
        wraps the notebook.
        """
        name = self._data_parser.WIDGET_NAMES['menu_notebook']
        widget = self._get_widget(name)
        return MenuContainer(widget)

    def _get_widget(self, widget_name):
        """Gets the widget associated
        with the name that was generated
        by the xml file.

        @param widget_name: str representing
        the name associated with the generated
        widget.

        @return: Gtk.Widget that was generated
        and matched the given name.
        """
        return self._gtk_builder.get_object(widget_name)

    @property
    def window(self):
        """Gets the widget that
        represents the window.

        @return: Gtk.Widget
        """
        name = self._data_parser.WIDGET_NAMES['main_window']
        return self._get_widget(name)

    @property
    def reservation_window(self):
        """Gets the widget that
        represents the reservation
        window

        @return: Gtk.Widget
        """
        name = self._data_parser.WIDGET_NAMES['reservations_window']
        return self._get_widget(name)

    @property
    def upcoming_orders_window(self):
        """Gets the widget that
        represents the upcoming
        orders window.

        @return: Gtk.Widget
        """
        name = self._data_parser.WIDGET_NAMES['upcoming_orders_window']
        return self._get_widget(name)

    def connect_signals(self, connect_ref):
        """ Connects the signals to the
        given connection reference.

        @param connect_ref: object that
        the signals are expected to be
        connected to.

        @return: None
        """
        self._gtk_builder.connect_signals(connect_ref)
        self._connector.connect(connect_ref)

    def _set_up(self):
        """Sets up the initial data
        to be displayed in the GUI.

        @return: None
        """
        self._create_status_label()
        self._create_order_label()

        self._create_tables()
        self._create_menu_notebook()

        self._set_window_properties()

    def _set_window_properties(self):
        """Sets upt he properties
        of the main window.

        @return: None
        """
        self.window.set_title(self._title)
        self.window.show_all()
        self.window.maximize()
        self.window.connect(self._data_parser.FLAGS['destroy'], Gtk.main_quit)

    def _create_status_label(self):
        """Creates the status label
        area.

        @return: None
        """
        name = self._data_parser.WIDGET_NAMES['status_label']
        self._status_label = self._get_widget(name)

    def _create_order_label(self):
        """Creates the order label
        that displays the selected
        order.

        @return: None
        """
        name = self._data_parser.WIDGET_NAMES['order_label']
        self._order_label = self._get_widget(name)

    def _create_tables(self):
        """Creates the tables that
        are displayed in the GUI

        @return: None
        """
        self._create_tables_buttons()
        self._create_misc_buttons()

    def _create_tables_buttons(self):
        """Creates the table buttons that
        are dispalyed in the GUI.

        @return: None
        """
        table_box = self._get_widget(self._data_parser.WIDGET_NAMES['table_box'])
        for button in self._generate_tables_buttons():
            table_box.pack_start(button, True, True, self.BORDER_SEPARATOR_VALUE)

    def _generate_tables_buttons(self):
        """Generates the table buttons

        @return: Generator object

        @yield: Gtk.Button that represents
        a table.
        """
        for x in range(1, NUM_OF_TABLES_TO_DISPLAY + 1):
            name = 'TABLE ' + str(x)
            button = Gtk.Button(name)
            button.set_focus_on_click(False)
            self._register_table_button(button)
            yield button

    def _register_table_button(self, button):
        """Registers the given button as
        a table button.

        @param button: Gtk.Button that
        represents the table button to
        be registered.

        @return: None
        """
        flag = self._data_parser.FLAGS['button']
        func = self._data_parser.FUNC_NAMES['table_button']
        label = button.get_label()
        self._connector.register(button, flag, func, label)

    def _create_misc_buttons(self):
        """Creates the misc buttons.

        @return: None
        """
        misc_box = self._get_widget(self._data_parser.WIDGET_NAMES['table_box'])

        for button in self._generate_misc_buttons():
            misc_box.pack_start(button, True, True, self.BORDER_SEPARATOR_VALUE)

    def _generate_misc_buttons(self):
        """Generates the misc buttons.

        @return: Generator object

        @yield: Gtk.Button that represents
        the misc buttons being generated.
        """
        button = Gtk.Button('MISC ORDERS')
        button.set_focus_on_click(False)
        self._register_misc_button(button)
        yield button

    def _register_misc_button(self, button):
        """Registers the given buton
        as a misc button.

        @param button: Gtk.Button that
        represents the misc button to be
        registered.

        @return: None
        """
        flag = self._data_parser.FLAGS['button']
        func = self._data_parser.FUNC_NAMES['misc_button']
        self._connector.register(button, flag, func)


    def _create_menu_notebook(self):
        """Creates the notebook that
        displays the menu.

        @return: None
        """
        for label, categories in self._data_parser.categories_data.items():
            component = self._create_menu_notebook_component(label, categories)
            self._menu_notebook.add(component)

    def _create_menu_notebook_component(self, label, categories):
        """Creates the menu notebook component
        associated with the given label and
        categories.

        @param label: str representing the
        label to be associated with the
        component. This will be displayed
        as the tab on the notebook page
        that the component represents.

        @param categories: list of str that
        represents the categories to be associated
        with this component.

        @return: MenuComponent object that represents
        the page associated with these categories.
        """
        component = MenuComponent(label)

        for category in categories:

            category_data = self._data_parser.menu_data[category]
            area = self._create_menu_notebook_areas(category, category_data)
            component.add(area)

        return component

    def _create_menu_notebook_areas(self, category, category_data):
        """Creates the menu notebook area that is
        to be inserted into a component. The area
        is created with the given information.

        @param category: str representing the
        category associated with the area.

        @param category_data: list of MenuItem
        objects that represents the data to be
        displayed in the category area.

        @return: ItemsArea that is used to
        be added to a component.
        """
        data = []

        for item in category_data:
            button = self._create_menu_button(item)
            data.append(button)

        return ItemsArea(data, category)

    def _create_menu_button(self, menu_item):
        """Creates the menu button from a
        given menu item.

        @param menu_item: MenuItem object
        that is to be stored in a MenuButton.

        @return: MenuButton object that
        wraps the given menu item.
        """
        button = MenuButton(menu_item)
        self._register_menu_button(button)
        return button

    def _register_menu_button(self, button):
        """Registers the given button as
        a menu button with the connector.

        @param button: MenuButton object
        that is to be registered.

        @return: None
        """
        flag = self._data_parser.FLAGS['button']
        func = self._data_parser.FUNC_NAMES['menu_button']
        self._connector.register(button, flag, func)

    def set_order_view(self, display_view):
        """Sets the order view to the hold
        the given view.

        @param display_view: Gtk.TreeView
        that is used to display order data.

        @return: None
        """
        order_window = self._get_order_window()

        for widget in order_window.get_children():
            order_window.remove(widget)

        order_window.add(display_view)

    def _get_order_window(self):
        """Gets the order window.

        @return: Gtk.Widget that
        represents the order window.
        """
        name = self._data_parser.WIDGET_NAMES['order_window']
        return self._get_widget(name)

    def set_table_display(self, table_value):
        """Sets the table display to the
        given value.

        @param table_value: str representing
        the value to display in the table
        display.

        @return: None
        """
        self._order_label.set_text(table_value)

    def update_status_display(self, status_msg, styles=[]):
        """Updates the status display with
        the given message and styles.

        @param status_msg: str representing
        the message to display.

        @param styles: list of str representing
        the styles to apply to the display. Accepted
        values are:

            'error' :   Red and bold
            'bold'  :   bold
            'italic':   italic

        @return: None
        """
        parsed_style = self._parse_style(styles)
        msg = parsed_style.format(status_msg)
        self._status_label.set_markup(msg)

    def _parse_style(self, styles):
        """Parses the given styles
        and returns them in a format
        waiting for a message to be
        formatted inside.

        @param styles: list of str
        representing the format
        stlyes to apply.

        @return: str representing
        the style waiting for a
        message to be formatted.
        """
        msg = '{}'
        for style in styles:
            if style == 'error':
                msg = '<span foreground="red">' + msg + '</span>'
                style = 'bold'
            if style == 'bold':
                msg = '<b>' + msg + '</b>'
            if style == 'italic':
                msg = '<i>' + msg + '</i>'
        return msg

    def get_menu_data(self):
        """Gets the stored menu data.

        @return: dict
        """
        return self._data_parser.unpack_menu_data()

    def get_categories_data(self):
        """Gets the stored categories
        data.

        @return: dict
        """
        return self._data_parser.unpack_categories_data()

    def get_options_data(self):
        """Gets the stored options
        data

        @return: dict
        """
        return self._data_parser.unpack_options_data()

    def get_discount_templates_data(self):
        """ Gets the stored discount
        templates data.

        @return: dict
        """
        return self._data_parser.unpack_discount_templates_data()

    def update_menu_data(self, updated_menu_data):
        """Updates the stored menu
        data.

        @param updated_menu_data: dict
        representing the updated menu
        data.

        @return: None
        """
        return self._data_parser.pack_menu_data(updated_menu_data)

    def update_categories_data(self, updated_categories_data):
        """Updates the stored categories
        data.

        @param updated_categories_data: dict
        representing the updated categories
        data.

        @return: None
        """
        return self._data_parser.pack_categories_data(updated_categories_data)

    def update_options_data(self, updated_options_data):
        """Updates the stored options data.

        @param updated_options_data: dict
        representing the stored options
        data.

        @return: None
        """
        return self._data_parser.pack_options_data(updated_options_data)

    def update_discount_templates_data(self, updated_discount_templates):
        """Updates the stored discount templates
        data.

        @param updated_discount_templates: dict
        representing the updated discount templates
        data.

        @return: None
        """
        return self._data_parser.pack_discount_templates_data(updated_discount_templates)