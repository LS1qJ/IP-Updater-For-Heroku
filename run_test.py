# -*- coding: utf-8 -*-


import imp
import os
import unittest

if __name__ == "__main__":
    testdir = os.path.curdir + "/test/"
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for filename in os.listdir(testdir):
        if (os.path.isfile(testdir + filename) and
                filename.endswith('_test.py')):
            mod = imp.load_source(filename.split('.')[0], testdir + filename)
            suite.addTest(loader.loadTestsFromModule(mod))
    unittest.TextTestRunner(verbosity=1).run(suite)
