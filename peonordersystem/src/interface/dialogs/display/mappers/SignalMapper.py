"""Defines the SignalMapper class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""


class SignalMapper(object):
    """Maps signals to registered
    functions
    """

    def __init__(self):
        """Initializes the signal mapper"""
        self._signals_to_funcs = {}

    def register_function(self, func, signal):
        """Registers the given function, under
        the given signal

        @param func: function to be registered

        @param signal: int representing the
        signal that the function will be registered
        to

        @return: int representing the signal
        registered
        """
        if signal not in self._signals_to_funcs:
            self._signals_to_funcs[signal] = set()
        self._signals_to_funcs[signal].add(func)

        return signal

    def signal(self, signal, *args, default=True):
        """Signals the mapped functions to be called

        @param signal: int representing the signal
        to be emitted

        @param args: wildcard catchall that passes
         the given arguments to the mapped function

        @keyword default: return value to be given
        if no return value is supplied by the mapping
        function

        @return: bool representing the state of the
        function called
        """
        result = default

        if signal in self._signals_to_funcs:
            result = self._execute_funcs(self._signals_to_funcs[signal], *args)

        return result

    def _execute_funcs(self, funcs, *args):
        """Executes each function contained
        within the given list of functions,
        passing the given arguments.

        @param funcs: iterable of functions

        @param args: wildcard catchall
        representing the arguments to be
        passed to the functions

        @return: bool value representing
        the conjunction of each functions
        result
        """
        result = True
        for func in funcs:
            result &= bool(func(*args))
        return result
