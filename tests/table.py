import unittest

import sys
import os
sys.path.append(os.path.join('..', 'table'))
import table as tbl

class TestTable(unittest.TestCase):
    def setUp(self):
        self.datadir = 'tmp'
        os.makedir(self.datadir)

    def tearDown(self):
        os.removedirs(self.datadir)
        
    def test_init(self, filename):
        pass
