import unittest
from algorithm_collection_tests import AlgorithmCollectionTests
from algorithm_builder_tests import AlgorithmBuilderTest
from algorithm_tests import AlgorithmTests
from data_element_tests import DataElementTests
from data_type_tests import DataTypeTests
from data_shape_tests import DataShapeTests


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(DataShapeTests))
suite.addTest(unittest.makeSuite(DataTypeTests))
suite.addTest(unittest.makeSuite(DataElementTests))
suite.addTest(unittest.makeSuite(AlgorithmTests))
suite.addTest(unittest.makeSuite(AlgorithmBuilderTest))
suite.addTest(unittest.makeSuite(AlgorithmCollectionTests))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
