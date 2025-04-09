# Python 3 Migration - Detailed Progress Report

This document contains detailed notes about the progress of the Python 3 migration effort, including what has been completed, current challenges, and next steps. It serves as both a log and a reference in case we need to restart the migration process.

## Current Status (As of Last Update)

The migration is in progress with the following achievements:

### Completed

1. **Core Infrastructure**
   - Created compatibility module (`py_compatibility.py`) for cross-version support
   - Set up fallbacks for Python 2-specific functions and types
   - Fixed imports and exception handling syntax for Python 3
   - Added STRICT_DEPENDENCIES flag to control dependency failures

2. **Core Modules Successfully Migrated**
   - `mcdp.branch_info`
   - `mcdp.logs`
   - `mcdp.constants`
   - `mcdp.dependencies` (with fallbacks for missing dependencies)
   - `mcdp.development` (with fallbacks for contracts module)

3. **Utility Functions**
   - Created `memoize_simple_py3.py` for Python 3 compatible memoization
   - Updated `string_utils.py` to handle bytes vs strings correctly
   - Updated `duration_hum.py` to use f-strings
   - Added `indent_utils.py` to avoid dependency on contracts
   - Updated StringIO, pickle, and iterator handling in `debug_pickler.py`

4. **Testing Infrastructure**
   - Created basic import tests that verify module loading
   - Added targeted unit tests for the updated utility functions
   - Set up test isolation techniques to bypass import chain issues

### Current Challenges

1. **Dependency Issues**
   - PyContracts package is incompatible with Python 3 (uses deprecated `inspect.ArgSpec`)
   - Import chains make isolated testing difficult
   - Some tests need to directly load modules to avoid import errors

2. **Import Structure**
   - Core modules import from many submodules, creating dependency chains
   - Need to create fallbacks for most import paths
   - Module initialization order is critical

3. **String/Bytes Handling**
   - Need to handle conversions between strings and bytes consistently
   - Functions expecting bytes need proper encoding from strings

4. **Iterator/Sequence API Changes**
   - `xrange` vs `range` differences
   - `.next()` vs `__next__()` methods
   - Dictionary views vs lists for keys/values/items

### Migration Strategy

The current strategy involves:

1. **Bottom-up Approach**:
   - Start with core utilities that have minimal dependencies
   - Create compatibility layers as needed
   - Gradually build up to more complex modules

2. **Fallback Implementations**:
   - When dependencies cannot be imported, provide alternative implementations
   - Use conditional imports with exception handling
   - Prioritize functionality over optimization

3. **Incremental Testing**:
   - Test each module in isolation when possible
   - Create minimal test scaffolds to bypass import issues
   - Prioritize basic imports before comprehensive testing

## Current Progress on Specific Files

### Successfully Migrated Files

| File | Status | Notes |
|------|--------|-------|
| `mcdp/py_compatibility.py` | ✅ Created | Provides cross-version compatibility functions |
| `mcdp/branch_info.py` | ✅ Compatible | No changes needed |
| `mcdp/logs.py` | ✅ Compatible | No changes needed |
| `mcdp/constants.py` | ✅ Compatible | No changes needed |
| `mcdp/dependencies.py` | ✅ Updated | Added STRICT_DEPENDENCIES flag and fallbacks |
| `mcdp/development.py` | ✅ Updated | Added fallbacks for contracts and memoize_simple |
| `mcdp_utils_misc/memoize_simple_py3.py` | ✅ Created | Python 3 version of memoize_simple |
| `mcdp_utils_misc/indent_utils.py` | ✅ Created | Replacement for contracts.utils.indent |
| `mcdp_utils_misc/string_repr.py` | ✅ Updated | Fixed imports for Python 3 |
| `mcdp_utils_misc/debug_pickler.py` | ✅ Updated | Fixed StringIO and pickle imports |
| `mcdp_utils_misc/string_utils.py` | ✅ Updated | Fixed bytes handling and formatting |
| `mcdp_utils_misc/duration_hum.py` | ✅ Updated | Updated string formatting to f-strings |

### Files in Progress or Next to Migrate

| File | Status | Notes |
|------|--------|-------|
| `mcdp_utils_misc/__init__.py` | ⚠️ Updated | Added compatibility imports, needs more testing |
| Other `mcdp_utils_misc/*.py` files | 🔄 Pending | Need to review and update one by one |
| `mcdp_lang/utils.py` | ⚠️ Started | Fixed inspect.getargspec usage |
| `mcdp/__init__.py` | ⚠️ Updated | Temporarily modified to allow partial imports |

## Technical Details for Recovery

### Dependency Workarounds

1. **PyContracts**: This causes the most issues. We've added fallbacks:
   ```python
   try:
       from contracts.utils import indent
   except ImportError:
       from .indent_utils import indent
   ```

2. **memoize_simple**: Created a pure Python 3 implementation that doesn't depend on PyContracts:
   ```python
   try:
       from .memoize_simple_imp import *
   except ImportError:
       from .memoize_simple_py3 import *
   ```

3. **StringIO**: Updated imports to work in both Python 2 and 3:
   ```python
   try:
       # Python 2
       from StringIO import StringIO
   except ImportError:
       # Python 3
       from io import StringIO
   ```

### Test Isolation Techniques

1. **Direct module loading** to bypass import chains:
   ```python
   import importlib.util
   module_path = os.path.join(os.path.dirname(__file__), '../src/path/to/module.py')
   spec = importlib.util.spec_from_file_location("module_name", module_path)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)
   ```

2. **Standalone implementations** for testing core functionality:
   ```python
   # Copy the function into a test file directly
   def memoize_simple(obj):
       # Implementation here
       pass
   
   # Then test it independently
   ```

## Next Steps

1. Continue migrating `mcdp_utils_misc` modules one by one:
   - `fileutils.py` - Likely needs updating for file modes ('rb' vs 'r')
   - `natsort.py` - Needs updating for Python 3 sorting
   - `safe_pickling.py` - Needs updating for Python 3 pickle protocol

2. Update import structure in `__init__.py` files to handle import failures gracefully

3. Start migrating core language modules:
   - `mcdp_posets` package
   - `mcdp_lang` package

4. Update the remaining modules with string/bytes handling

5. Create more comprehensive tests for migrated functionality

6. Eventually, enable STRICT_DEPENDENCIES to enforce proper dependency checking

## Commands Used

These commands have been useful during migration:

```bash
# Run specific test file
python tests/test_memoize_test.py

# Run the import tests
python tests/test_imports.py

# Test module loading
python -c "import mcdp.branch_info"

# Debug import chains
python -c "import sys; import mcdp; print(sys.modules.keys())"

# Run string_utils tests
python tests/test_string_utils_minimal.py
```

## State Management

Each step of the migration is committed with a detailed commit message:

1. Migration setup: a0703e2e, aa5326ee
2. Core module updates: d52e7fc0, bd25a65c
3. Utils migration: 77108284, 2c245078, 583f5e8f

If we need to restart, we can:
1. Check out the latest commit
2. Pick up from the next module in the list
3. Reference this document for details on what has been done and what needs attention

The migration approach is modular, so we can resume from any point by focusing on the next utility module or core component to update.