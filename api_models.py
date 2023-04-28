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

    class Config:
        smart_union = True


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

    class Config:
        smart_union = True


class Parameters(BaseModel):
    parameters: list[Data]

    def get_params_to_execute(self):
        return {param.name: param.value for param in self.parameters}


class Outputs(BaseModel):
    outputs: list[Data]


class Answer(BaseModel):
    result: Optional[Any]
    errors: Optional[str]

    class Config:
        @staticmethod
        def schema_extra(schema, model):
            for prop, value in schema.get('properties', {}).items():
                field = [x for x in model.__fields__.values()
                         if x.alias == prop][0]
                if field.allow_none:
                    if 'type' in value:
                        value['anyOf'] = [{'type': value.pop('type')}]
                    elif '$ref' in value:
                        if issubclass(field.type_, BaseModel):
                            value['title'] = field.type_.__config__.title \
                                             or field.type_.__name__
                        value['anyOf'] = [{'$ref': value.pop('$ref')}]
                    value['anyOf'].append({'type': 'null'})


class AnswerOutputs(Answer):
    result: Optional[Outputs]


class AnswerAlgorithmDefinition(Answer):
    result: Optional[AlgorithmDefinition]
