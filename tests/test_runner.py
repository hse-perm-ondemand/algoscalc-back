from unittest import TestSuite, TestLoader, TextTestRunner

from tests.core_tests.algorithm_collection_tests import AlgorithmCollectionTests
from tests.core_tests.algorithm_builder_tests import AlgorithmBuilderTest
from tests.core_tests.algorithm_tests import AlgorithmTests
from tests.core_tests.data_element_tests import DataElementTests
from tests.core_tests.data_type_tests import DataTypeTests
from tests.core_tests.data_shape_tests import DataShapeTests
from tests.app_tests.app_tests import AppTest


def get_suite():
    """Создает и возвращает набор тестов."""
    suite = TestSuite()
    suite.addTest(TestLoader().loadTestsFromTestCase(DataShapeTests))
    suite.addTest(TestLoader().loadTestsFromTestCase(DataTypeTests))
    suite.addTest(TestLoader().loadTestsFromTestCase(DataElementTests))
    suite.addTest(TestLoader().loadTestsFromTestCase(AlgorithmTests))
    suite.addTest(TestLoader().loadTestsFromTestCase(AlgorithmBuilderTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(AlgorithmCollectionTests))
    suite.addTest(TestLoader().loadTestsFromTestCase(AppTest))
    return suite

def run():
    """Запускает набор тестов."""
    runner = TextTestRunner(verbosity=2)
    runner.run(get_suite())

if __name__ == '__main__':
    run()
