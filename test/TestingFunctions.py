"""TestingFunctions module supplies functions that are
useful in testing.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
import os
import string
import jsonpickle
from random import randint, random, sample
from datetime import date, datetime, time, timedelta

from src.peonordersystem.MenuItem import MenuItem, DiscountItem
from src.peonordersystem.interface.Reservations import Reserver
from src.peonordersystem.Settings import (MAX_DATETIME,
                                          MIN_DATETIME,
                                          TOGO_SEPARATOR,
                                          TYPE_SUFFIX_STANDARD_ORDER,
                                          SQLITE_DATE_TIME_FORMAT_STR,
                                          SQLITE_DATE_FORMAT_STR,
                                          FILENAME_BLACKLIST_CHARS)

from test.Settings import (POSSIBLE_CHARS,
                           GENERATOR_MAX,
                           NUM_OF_CHARS)


#====================================================================================
# This block represents utility functions.
#====================================================================================
def save_data_to_file(order_data, file_path):
    """Adds the given data to the given file path
    overwriting any data the currently exists.

    The given data will be written by utilizing
    jsonpickle to serialize the data.

    @param order_data: data to be serialized.

    @param file_path: str representing the path
    of the file to be saved to.

    @return: data that was saved to the file,
    as it would return from decoding it from
    the file.
    """
    data = jsonpickle.encode(order_data)
    with open(file_path, 'w') as f:
        f.write(data)

    return jsonpickle.decode(data)


def get_data_from_file(file_path):
    """Gets the data from the file and decodes
    it using jsonpickle.

    The given file path will be read and any
    data contained will be decoded and returned.

    @param file_path: file path of file that
    stores serialized json data.

    @return: decoded data that was stored
    in the object.
    """
    with open(file_path, 'r') as f:
        return jsonpickle.decode(f.read())


#====================================================================================
# This block represents functions that are used to generate data. All functions
# here utilize generators and yield to return an data.
#====================================================================================
def generate_random_names(n=GENERATOR_MAX,
                          from_chars=(POSSIBLE_CHARS + TOGO_SEPARATOR * 6),
                           num_of_chars=NUM_OF_CHARS):
    """Creates generator that returns an arbitrary number of
    randomly generated names.

    @keyword n: the number of names to generate through
    the generator. This is to assure that a indefinite
    loop will not occur.

    @keyword from_chars: str representing the characters
    to be chosen from. Default POSSIBLE_CHARS

    @keyword num_of_chars: int representing the number of
    characters each name should be in length. Default 100

    @return: generator object.

    @yield: str representing a name generated.
    """
    counter = 0
    while counter < n:
        name = ''.join(sample(from_chars, num_of_chars))
        yield name

        counter += 1


def generate_random_times(from_time=MIN_DATETIME, until_time=MAX_DATETIME,
                                   n=GENERATOR_MAX):
    """Generates random times within the given time frame.

    @param from_time: datetime object that represents
    the starting time, inclusive.

    @param until_time: datetime object that represents
    the ending time, inclusive.

    @keyword n: number of times to generate. This is to
    assure that the loop is not triggered accidentally.

    @return: generator that yields random times within
    the given range.

    @yield: datetime.datetime object generated from within
    the given range.
    """
    max_time_delta = until_time - from_time
    max_time_seconds = int(max_time_delta.total_seconds())

    counter = 0
    while counter < n:
        time_data = {'seconds': randint(1, max(1, max_time_seconds)),
                     'microseconds': 0}

        time_delta = timedelta(**time_data)

        yield from_time + time_delta

        counter += 1


def generate_random_menu_items(n=GENERATOR_MAX, is_notification=0.5):
    """Generates a list of menu items that would
    represent a single order. With the
    given number of items generated.

    @keyword n: int representing number of random
    MenuItems to be associated with this order.

    @keyword has_notification: float representing
    the probability that the generated MenuItems
    are notification items.

    @return: list of MenuItem objects generated.
    """
    counter = 0
    rand_name = generate_random_names(n=n*2)

    while counter < n:
        price = randint(1, 100)
        item = MenuItem(rand_name.next(), price)

        if random() <= is_notification:
            message = rand_name.next()
            item.comp(True, message)

        yield item
        counter += 1


def generate_random_reservations(from_time=None, until_time=MAX_DATETIME,
                                 n=GENERATOR_MAX):
    """Generates a Reserver object with a random
    time within the given time frame.

    @param from_time: datetime.datetime object
    that represents the starting date for the Reserver
    object date range. Default is None and therefore
    datetime.now() is used.

    @param until_time: datetime.datetime object
    that represents the ending date for the Reserver
    object date range, Inclusive. Default is MAX_DATETIME.

    @param n: int representing number of random
    Reserver items to be generated. This is utilized
    to prevent possible indefinite loops, Inclusive.
    Default is GENERATOR_MAX

    @return: generator object that is used to generate
    random Reserver values within the specified
    ranges.

    @yield: Reserver object with randomized name, number,
    and arrival time within the given arrival range.
    """
    if not from_time or from_time < datetime.now():
        from_time = datetime.now()
    rand_name = generate_random_names(n=n*2)
    rand_time = generate_random_times(from_time, until_time)

    counter = 0

    while counter < n:
        td = datetime.now() - from_time + timedelta(seconds=1)
        rsvr = Reserver(rand_name.next(),
                        rand_name.next(),
                        rand_time.next() + td)

        yield rsvr

        if datetime.now() == until_time:
            counter = n
        counter += 1
