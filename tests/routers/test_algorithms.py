import json

import pytest

from src.internal.constants import ALGORITHMS_ENDPOINT
from src.internal.schemas.definition_schema import DefinitionSchema
from src.routers.schemas import AnswerAlgorithmDefinition, AnswerOutputs
from tests import FIB_DEF, SUM_DEF, SUM_NAME


class TestAlgorithms:
    def test_get_algorithms(self, client):
        response = client.get(ALGORITHMS_ENDPOINT)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 2
        assert DefinitionSchema.model_validate(FIB_DEF).model_dump() in response.json()
        assert DefinitionSchema.model_validate(SUM_DEF).model_dump() in response.json()

    def test_get_algorithm(self, client):
        response = client.get(ALGORITHMS_ENDPOINT + "/" + SUM_NAME)
        assert response.status_code == 200
        assert AnswerAlgorithmDefinition.model_validate(response.json())
        assert response.json()["result"] == SUM_DEF

    def test_get_not_existed_algorithm(self, client):
        response = client.get(ALGORITHMS_ENDPOINT + "/not_existed")
        assert response.status_code == 200
        assert AnswerAlgorithmDefinition.model_validate(response.json())
        assert response.json()["result"] is None
        assert response.json()["errors"] is not None

    def test_get_algorithm_result(self, client):
        parameters = json.dumps(
            {"parameters": [{"name": "a", "value": 1}, {"name": "b", "value": 2}]}
        )
        response = client.post(ALGORITHMS_ENDPOINT + "/" + SUM_NAME, data=parameters)
        assert response.status_code == 200
        assert AnswerOutputs.model_validate(response.json())
        assert response.json()["result"] == {
            "outputs": [{"name": "result", "value": 3}]
        }
        assert response.json()["errors"] is None

    def test_get_not_existed_algorithm_result(self, client):
        parameters = json.dumps(
            {"parameters": [{"name": "a", "value": 1}, {"name": "b", "value": 2}]}
        )
        response = client.post(ALGORITHMS_ENDPOINT + "/not_existed", data=parameters)
        assert response.status_code == 200
        assert AnswerOutputs.model_validate(response.json())
        assert response.json()["result"] is None
        assert response.json()["errors"] is not None

    def test_get_algorithm_result_invalid_params(self, client):
        parameters = json.dumps(
            {
                "parameters": [
                    {"invalid_key": "a", "value": 1},
                    {"name": "b", "value": 2},
                ]
            }
        )
        response = client.post(ALGORITHMS_ENDPOINT + "/not_existed", data=parameters)
        assert response.status_code == 422

    def test_get_algorithm_result_missed_param(self, client):
        parameters = json.dumps({"parameters": [{"name": "a", "value": 1}]})
        response = client.post(ALGORITHMS_ENDPOINT + "/not_existed", data=parameters)
        assert response.status_code == 200
        assert AnswerOutputs.model_validate(response.json())
        assert response.json()["result"] is None
        assert response.json()["errors"] is not None

    def test_get_algorithm_result_unexpected_param(self, client):
        parameters = json.dumps(
            {
                "parameters": [
                    {"name": "a", "value": 1},
                    {"name": "b", "value": 2},
                    {"name": "unexpected", "value": 2},
                ]
            }
        )
        response = client.post(ALGORITHMS_ENDPOINT + "/not_existed", data=parameters)
        assert response.status_code == 200
        assert AnswerOutputs.model_validate(response.json())
        assert response.json()["result"] is None
        assert response.json()["errors"] is not None


if __name__ == "__main__":
    pytest.main(["-k", "TestAlgorithms"])
