import pytest
from pydantic import ValidationError

from src.internal.schemas.definition_schema import DefinitionSchema
from tests import DESCRIPTION, INVALID_STRING_CASES, NAME, TITLE, ErrorItemEnum


class TestDefinitionSchema:
    """Набор тестов для проверки класса DefinitionSchema"""

    def test_valid_entity(self):
        """Проверка создания объекта DefinitionSchema"""
        entity = DefinitionSchema(
            name="ValidName", title="ValidTitle", description="ValidDescription"
        )
        assert entity.name == "ValidName"
        assert entity.title == "ValidTitle"
        assert entity.description == "ValidDescription"

    @pytest.mark.parametrize(
        "test_case",
        INVALID_STRING_CASES,
        ids=[test_case.description for test_case in INVALID_STRING_CASES],
    )
    def test_wrong_name(self, test_case):
        """Проверка указания невалидного имени"""
        with pytest.raises(ValidationError) as ctx:
            DefinitionSchema(
                name=test_case.value, title="ValidTitle", description="ValidDescription"
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (NAME,)

    @pytest.mark.parametrize(
        "test_case",
        INVALID_STRING_CASES,
        ids=[test_case.description for test_case in INVALID_STRING_CASES],
    )
    def test_wrong_title(self, test_case):
        """Проверка указания невалидного заголовка"""
        with pytest.raises(ValidationError) as ctx:
            DefinitionSchema(
                name="ValidName", title=test_case.value, description="ValidDescription"
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (TITLE,)

    @pytest.mark.parametrize(
        "test_case",
        INVALID_STRING_CASES,
        ids=[test_case.description for test_case in INVALID_STRING_CASES],
    )
    def test_wrong_description(self, test_case):
        """Проверка указания невалидного описания"""
        with pytest.raises(ValidationError) as ctx:
            DefinitionSchema(
                name="ValidName", title="ValidTitle", description=test_case.value
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (DESCRIPTION,)


if __name__ == "__main__":
    pytest.main(["-k", "TestDefinitionSchema"])
