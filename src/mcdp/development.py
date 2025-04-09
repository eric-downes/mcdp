# -*- coding: utf-8 -*-
import getpass
import warnings
import functools

# Try to import all_disabled from contracts, fall back to a safe default if not available
try:
    from contracts import all_disabled
except ImportError:
    # If contracts cannot be imported, provide a fallback
    warnings.warn("contracts module not available, using fallback implementation")
    def all_disabled():
        return True

# Try to import memoize_simple, fall back to a simple implementation if not available
try:
    from mcdp_utils_misc import memoize_simple
except ImportError:
    # Fallback implementation of memoize_simple using functools.lru_cache
    warnings.warn("mcdp_utils_misc.memoize_simple not available, using fallback implementation")
    memoize_simple = functools.lru_cache(maxsize=None)


# import warnings
@memoize_simple
def get_user():
    return getpass.getuser()
# class _storage:
#     first = True

def do_extra_checks():
    """ True if we want to do extra paranoid checks for functions. """
    res = not all_disabled()
#     if _storage.first:
#         # logger.info(f'do_extra_checks: {res}')
#         pass
#     _storage.first = False
    return res


def mcdp_dev_warning(s):  # @UnusedVariable
    if get_user() in  ['andrea']:
        #warnings.warn(s)
        pass


