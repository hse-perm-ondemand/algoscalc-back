import json

import pytest

from src.internal.constants import ALGORITHMS_ENDPOINT
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.data_element_schema import DataElementsSchema
from src.internal.schemas.definition_schema import DefinitionSchema
from tests import BOOL_DEF, BOOL_NAME, FIB_DEF, SUM_DEF, SUM_NAME


class TestAlgorithms:
    def test_get_algorithms(self, client):
        response = client.get(ALGORITHMS_ENDPOINT)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 3
        assert DefinitionSchema.model_validate(FIB_DEF).model_dump() in response.json()
        assert DefinitionSchema.model_validate(SUM_DEF).model_dump() in response.json()
        assert DefinitionSchema.model_validate(BOOL_DEF).model_dump() in response.json()

    def test_get_algorithm(self, client):
        response = client.get(f"{ALGORITHMS_ENDPOINT}/{SUM_NAME}")
        assert response.status_code == 200
        assert AlgorithmDefinitionSchema.model_validate(response.json())
        assert response.json() == SUM_DEF

    def test_get_not_existed_algorithm(self, client):
        response = client.get(ALGORITHMS_ENDPOINT + "/not_existed")
        assert response.status_code == 404

    def test_get_algorithm_result(self, client):
        parameters = json.dumps([{"name": "a", "value": 1}, {"name": "b", "value": 2}])
        response = client.post(
            f"{ALGORITHMS_ENDPOINT}/{SUM_NAME}/results", data=parameters
        )
        assert response.status_code == 200
        assert DataElementsSchema.model_validate(response.json())
        assert response.json() == [{"name": "result", "value": 3}]

    def test_get_algorithm_result_bool(self, client):
        parameters = json.dumps([{"name": "x", "value": True}])
        response = client.post(
            f"{ALGORITHMS_ENDPOINT}/{BOOL_NAME}/results", data=parameters
        )
        assert response.status_code == 200
        assert DataElementsSchema.model_validate(response.json())
        assert response.json() == [{"name": "y", "value": True}]

    def test_get_not_existed_algorithm_result(self, client):
        parameters = json.dumps([{"name": "a", "value": 1}, {"name": "b", "value": 2}])
        response = client.post(
            ALGORITHMS_ENDPOINT + "/not_existed/results", data=parameters
        )
        assert response.status_code == 404

    def test_get_algorithm_result_invalid_params(self, client):
        parameters = json.dumps(
            [
                {"invalid_key": "a", "value": 1},
                {"name": "b", "value": 2},
            ]
        )
        response = client.post(
            f"{ALGORITHMS_ENDPOINT}/{SUM_NAME}/results", data=parameters
        )
        assert response.status_code == 422

    def test_get_algorithm_result_missed_param(self, client):
        parameters = json.dumps([{"name": "a", "value": 1}])
        response = client.post(
            f"{ALGORITHMS_ENDPOINT}/{SUM_NAME}/results", data=parameters
        )
        assert response.status_code == 400

    def test_get_algorithm_result_unexpected_param(self, client):
        parameters = json.dumps(
            [
                {"name": "a", "value": 1},
                {"name": "b", "value": 2},
                {"name": "unexpected", "value": 2},
            ]
        )
        response = client.post(
            f"{ALGORITHMS_ENDPOINT}/{SUM_NAME}/results", data=parameters
        )
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main(["-k", "TestAlgorithms"])
