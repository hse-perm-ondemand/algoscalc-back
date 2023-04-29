import unittest
from core_tests.algorithm_collection_tests import AlgorithmCollectionTests
from core_tests.algorithm_builder_tests import AlgorithmBuilderTest
from core_tests.algorithm_tests import AlgorithmTests
from core_tests.data_element_tests import DataElementTests
from core_tests.data_type_tests import DataTypeTests
from core_tests.data_shape_tests import DataShapeTests
from app_tests.app_tests import AppTest

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DataShapeTests))
    suite.addTest(unittest.makeSuite(DataTypeTests))
    suite.addTest(unittest.makeSuite(DataElementTests))
    suite.addTest(unittest.makeSuite(AlgorithmTests))
    suite.addTest(unittest.makeSuite(AlgorithmBuilderTest))
    suite.addTest(unittest.makeSuite(AlgorithmCollectionTests))
    suite.addTest(unittest.makeSuite(AppTest))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
