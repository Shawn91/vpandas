import traceback
import types
from functools import wraps

from PyQt5.QtCore import pyqtSlot


def generate_response(result=None, warning=""):
    return locals()


def MyPyQtSlot(*args):
    """A decorator for debugging PyQt slot functions.
    Stolen from https://stackoverflow.com/questions/18740884/preventing-pyqt-to-silence-exceptions-occurring-in-slots/19015654#19015654
    """
    if len(args) == 0 or isinstance(args[0], types.FunctionType):
        args = []
    @pyqtSlot(*args)
    def slotdecorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args)
            except:
                print("Uncaught Exception in slot")
                traceback.print_exc()
        return wrapper

    return slotdecorator


def convert_bytes(n, round=True):
    """Convert n bytes to a more user-friendly number in appropriate units like MB or GB
    Args:
        round: Whether to round the resule number to an integer
    """
    units = ['B','KB', 'MB', 'GB', 'TB']
    unit_index = 0
    if isinstance(n, str) and n.isdigit():
        n = float(n)
    while n >=1024 and unit_index < len(units)-1:
        n /= 1024
        unit_index += 1
    if round:
        return (int(n), units[unit_index])
    else:
        return (n, units[unit_index])