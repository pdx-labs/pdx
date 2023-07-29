import pytest
from pydantic import BaseModel
from pdx.cache.in_memory_cache import InMemoryCache
from pdx.agent.metadata import AgentResponse


# @pytest.fixture
def config():
    class TestConfig(BaseModel):
        test_data: dict = {'data': 'What do you call a dog that does magic tricks? A labracadabrador!',
                           'metadata': {'custom': {},
                                        'pdx': {'version': '0.5.0'},
                                        'request': {'agent_id': {'agent_name': 'agent',
                                                                 'git_branch': 'add-caching',
                                                                 'git_hash': 'e549a8020c00ff110a080397bfed10295212ae5e',
                                                                 'unique_id': '4a01e244-043b-4a76-a2e6-7370a66afbca'},
                                                    'prompt': [{'content': 'Tell me a joke about dogs.',
                                                                'role': 'template'}],
                                                    'request_id': 'd4ebfb91-ff9a-4f17-a121-40ebcf5e1d60',
                                                    'request_params': {'best_of': 1,
                                                                       'frequency_penalty': 0,
                                                                       'max_tokens': 1200,
                                                                       'model': 'text-davinci-003',
                                                                       'presence_penalty': 0,
                                                                       'stop': ['#', '---'],
                                                                       'temperature': 0,
                                                                       'top_p': 1},
                                                    'request_values': {'topic': 'dogs'}},
                                        'response': {'api_log_id': 'cmpl-7hcL1QiknQ7v4aeVI1pc7lUk7Us8M',
                                                     'latency': 1.2025699615478516,
                                                     'model': 'text-davinci-003',
                                                     'stop': 'stop',
                                                     'stop_reason': 'stop',
                                                     'token_usage': {'prompt': 8,
                                                                     'response': 26,
                                                                     'total': 34}}}}
        request_values: dict = {'topic': 'dogs'}

    return TestConfig()


# def test_one(request, config):

#     assert config.input_value == "Input Value"

#     request.config.cache.set('values', {
#         'input_value': 'Input Value',
#         'output_value': 'Output Value'
#     })


# def test_two(request, config):

#     assert config.output_value == "Output Value"

#     values = request.config.cache.get('values', None)
#     assert values != None
#     data = {
#         'input_value': config.input_value,
#         'output_value': config.output_value
#     }
#     assert values == data

if __name__ == '__main__':
    agent_response = AgentResponse(**config().test_data)
    print(type(agent_response))
    print(repr(agent_response))
    print(agent_response.model_dump(mode='json'))
