import os
import unittest

from fastapi.testclient import TestClient

from src import ALGORITHMS_ENDPOINT, IS_TEST_APP
from src.api_models import (
    Algorithms,
    AnswerAlgorithmDefinition,
    AnswerOutputs,
    Data,
    Parameters,
)


class AppTest(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        os.environ[IS_TEST_APP] = str(True)
        if os.path.exists(os.path.basename(__file__)):
            os.chdir("../..")
        from src.main import app

        AppTest.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        os.environ[IS_TEST_APP] = str(False)

    def test_get_algorithms(self):
        response = AppTest.client.get(ALGORITHMS_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Algorithms.model_validate(response.json()))

    def test_get_algorithm(self):
        response = AppTest.client.get(ALGORITHMS_ENDPOINT)
        algs = Algorithms(**(response.json()))
        algorithm_name = algs.algorithms[0].name
        response = self.client.get(ALGORITHMS_ENDPOINT + "/" + algorithm_name)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AnswerAlgorithmDefinition.model_validate(response.json()))

    def test_get_algorithm_result(self):
        response = AppTest.client.get(ALGORITHMS_ENDPOINT)
        algs = Algorithms(**(response.json()))
        algorithm_name = algs.algorithms[0].name

        response = AppTest.client.get(ALGORITHMS_ENDPOINT + "/" + algorithm_name)
        answer = AnswerAlgorithmDefinition(**(response.json()))
        alg_def = answer.result
        params = [
            Data(name=data_def.name, value=data_def.default_value)
            for data_def in alg_def.parameters
        ]
        output_dict = {
            data_def.name: data_def.default_value for data_def in alg_def.outputs
        }
        parameters = Parameters(parameters=params)
        response = AppTest.client.post(
            ALGORITHMS_ENDPOINT + "/" + algorithm_name,
            content=parameters.model_dump_json(),
        )

        self.assertEqual(response.status_code, 200)
        answer = AnswerOutputs(**(response.json()))
        fact_outputs = answer.result
        for fact_output in fact_outputs.outputs:
            self.assertEqual(fact_output.value, output_dict[fact_output.name])


if __name__ == "__main__":
    unittest.main()
