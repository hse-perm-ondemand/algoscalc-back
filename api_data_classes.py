from typing import Union, Optional, Any
from pydantic import BaseModel


class AlgorithmTitle(BaseModel):
    name: str
    title: str


class Algorithms(BaseModel):
    algorithms: Optional[list[AlgorithmTitle]]


class DataDefinition(BaseModel):
    name: str
    title: str
    description: str
    data_type: str
    data_shape: str
    default_value: Union[int, float, str, bool,
                         Optional[list[Union[int, float, str, bool,
                                             Optional[list[
                                                 Union[int, float,
                                                       str, bool]]]]]]]


class AlgorithmDefinition(BaseModel):
    name: str
    title: str
    description: str
    parameters: list[DataDefinition]
    outputs: list[DataDefinition]


class Data(BaseModel):
    name: str
    value: Union[int, float, str, bool,
                 Optional[list[Union[int, float, str, bool,
                                     Optional[list[
                                         Union[int, float, str, bool]]]]]]]


class Parameters(BaseModel):
    parameters: list[Data]

    def get_params_to_execute(self):
        return {param.name: param.value for param in self.parameters}


class Outputs(BaseModel):
    outputs: list[Data]


class Answer(BaseModel):
    result: Optional[Any]
    errors: Optional[str]


class AnswerOutputs(Answer):
    result: Optional[Outputs]


class AnswerAlgorithmDefinition(Answer):
    result: Optional[AlgorithmDefinition]
