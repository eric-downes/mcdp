#!/usr/bin/env python3
# Test for Python 3 compatibility of mcdp_utils_misc

import os
import sys
import tempfile
import unittest
import gzip

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

class TestUtilsPy3(unittest.TestCase):
    """Tests for Python 3 compatibility of mcdp_utils_misc."""
    
    def test_fileutils(self):
        """Test fileutils functions."""
        from mcdp_utils_misc.fileutils import read_file_encoded_as_utf8, create_tmpdir, tmpdir, tmpfile
        
        # Create a temporary file with UTF-8 content
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write("Test UTF-8 file with unicode: αβγδε")
            temp_file = f.name
        
        try:
            # Test read_file_encoded_as_utf8
            content = read_file_encoded_as_utf8(temp_file)
            self.assertIsInstance(content, bytes)
            self.assertEqual(content.decode('utf-8'), "Test UTF-8 file with unicode: αβγδε")
            
            # Test create_tmpdir
            temp_dir = create_tmpdir(prefix='test_py3_')
            self.assertTrue(os.path.exists(temp_dir))
            os.rmdir(temp_dir)
            
            # Test tmpdir context manager
            with tmpdir(prefix='test_py3_') as d:
                self.assertTrue(os.path.exists(d))
            self.assertFalse(os.path.exists(d))  # Should be cleaned up
            
            # Test tmpfile context manager
            with tmpfile(suffix='.txt') as f:
                self.assertTrue(os.path.exists(f))
            self.assertFalse(os.path.exists(f))  # Should be cleaned up
                
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_safe_write(self):
        """Test safe_write functions."""
        from mcdp_utils_misc.safe_write import safe_write, safe_read
        
        # Test safe_write with text mode and encoding
        test_file = os.path.join(tempfile.gettempdir(), 'test_safe_write.txt')
        if os.path.exists(test_file):
            os.unlink(test_file)
            
        # Write with encoding
        with safe_write(test_file, mode='wt', encoding='utf-8') as f:
            f.write("Test UTF-8 file with unicode: αβγδε")
            
        # Read back with encoding
        with safe_read(test_file, mode='rt', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, "Test UTF-8 file with unicode: αβγδε")
            
        # Test with gzip
        test_gz_file = os.path.join(tempfile.gettempdir(), 'test_safe_write.txt.gz')
        if os.path.exists(test_gz_file):
            os.unlink(test_gz_file)
            
        # Write with gzip
        with safe_write(test_gz_file, mode='wt', encoding='utf-8') as f:
            f.write("Test gzipped UTF-8 file with unicode: αβγδε")
            
        # Read with gzip
        with safe_read(test_gz_file, mode='rt', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, "Test gzipped UTF-8 file with unicode: αβγδε")
            
        # Clean up
        os.unlink(test_file)
        os.unlink(test_gz_file)
    
    def test_yaml(self):
        """Test YAML utilities."""
        from mcdp_utils_misc.my_yaml import yaml_load, yaml_dump
        
        # Test simple data structures
        data = {
            'string': 'test',
            'int': 123,
            'list': [1, 2, 3],
            'dict': {'a': 1, 'b': 2},
            'none': None
        }
        
        # Dump and load
        yaml_str = yaml_dump(data)
        loaded_data = yaml_load(yaml_str)
        
        # Check that it loaded correctly
        self.assertEqual(loaded_data['string'], 'test')
        self.assertEqual(loaded_data['int'], 123)
        self.assertEqual(loaded_data['list'], [1, 2, 3])
        self.assertEqual(loaded_data['dict'], {'a': 1, 'b': 2})
        self.assertIsNone(loaded_data['none'])
    
    def test_natsort(self):
        """Test natural sorting."""
        from mcdp_utils_misc.natsort import natural_sorted
        
        # Test with mixed strings and numbers
        items = ['file10.txt', 'file1.txt', 'file2.txt', 'file20.txt']
        sorted_items = natural_sorted(items)
        
        # Check that it's sorted correctly (1, 2, 10, 20)
        self.assertEqual(sorted_items, ['file1.txt', 'file2.txt', 'file10.txt', 'file20.txt'])
    
    def test_pickling(self):
        """Test pickling utilities."""
        from mcdp_utils_misc.safe_pickling import safe_pickle_dump, safe_pickle_load
        
        # Create a temporary file
        test_pickle = os.path.join(tempfile.gettempdir(), 'test_pickle.pkl')
        if os.path.exists(test_pickle):
            os.unlink(test_pickle)
            
        # Data to pickle
        data = {
            'string': 'test',
            'int': 123,
            'list': [1, 2, 3],
            'dict': {'a': 1, 'b': 2},
            'none': None
        }
        
        # Dump and load
        safe_pickle_dump(data, test_pickle)
        loaded_data = safe_pickle_load(test_pickle)
        
        # Check that it loaded correctly
        self.assertEqual(loaded_data['string'], 'test')
        self.assertEqual(loaded_data['int'], 123)
        self.assertEqual(loaded_data['list'], [1, 2, 3])
        self.assertEqual(loaded_data['dict'], {'a': 1, 'b': 2})
        self.assertIsNone(loaded_data['none'])
        
        # Clean up
        os.unlink(test_pickle)

if __name__ == '__main__':
    unittest.main()