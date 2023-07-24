import pytest
from pydantic import BaseModel

'''
A tempalte for writing tests using pytest.
'''


@pytest.fixture
def config():
    class TestConfig(BaseModel):
        input_value: str = "Input Value"
        output_value: str = "Output Value"

    return TestConfig()


def test_one(request, config):

    assert config.input_value == "Input Value"

    request.config.cache.set('values', {
        'input_value': 'Input Value',
        'output_value': 'Output Value'
    })


def test_two(request, config):

    assert config.output_value == "Output Value"

    values = request.config.cache.get('values', None)
    assert values != None
    data = {
        'input_value': config.input_value,
        'output_value': config.output_value
    }
    assert values == data
