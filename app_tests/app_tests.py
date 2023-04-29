import os
import unittest
import jsonschema
from fastapi.testclient import TestClient

from api_models import Algorithms, AnswerAlgorithmDefinition, Data, \
    Parameters, AnswerOutputs
from constants import IS_TEST_APP


class AppTest(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        os.environ[IS_TEST_APP] = str(True)
        if os.path.exists(os.path.basename(__file__)):
            os.chdir('..')
        from main import app
        AppTest.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        os.environ[IS_TEST_APP] = str(False)

    def test_get_algorithms(self):
        response = AppTest.client.get('/api/algorithms')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(jsonschema.validate(response.json(),
                                              Algorithms().schema()))

    def test_get_algorithm(self):
        response = AppTest.client.get('/api/algorithms')
        algs = Algorithms().parse_obj(response.json())
        algorithm_name = algs.algorithms[0].name
        response = self.client.get('/api/algorithms/' + algorithm_name)
        self.assertEqual(response.status_code, 200)
        schema = AnswerAlgorithmDefinition().schema()
        self.assertIsNone(jsonschema.validate(response.json(), schema))

    def test_get_algorithm_result(self):
        response = AppTest.client.get('/api/algorithms')
        algs = Algorithms().parse_obj(response.json())
        algorithm_name = algs.algorithms[0].name

        response = AppTest.client.get('/api/algorithms/' + algorithm_name)
        answer = AnswerAlgorithmDefinition().parse_obj(response.json())
        alg_def = answer.result
        params = [Data(name=data_def.name, value=data_def.default_value)
                  for data_def in alg_def.parameters]
        output_dict = {data_def.name: data_def.default_value
                       for data_def in alg_def.outputs}
        parameters = Parameters(parameters=params)
        response = AppTest.client.post('/api/algorithms/' + algorithm_name,
                                       content=parameters.json())

        self.assertEqual(response.status_code, 200)
        answer = AnswerOutputs().parse_obj(response.json())
        fact_outputs = answer.result
        for fact_output in fact_outputs.outputs:
            self.assertEqual(fact_output.value, output_dict[fact_output.name])


if __name__ == '__main__':
    unittest.main()
