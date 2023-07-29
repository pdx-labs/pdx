import pytest
from pdx.cache.in_memory_cache import InMemoryCache
from pdx.agent.metadata import AgentResponse


class TestConfig:
    test_data_1: dict = {'data': '\n\nQ: What do you call a dog that does magic tricks? \nA: A labracadabrador!',
                         'metadata': {'custom': {},
                                      'pdx': {'version': '0.5.1'},
                                      'request': {'agent_id': {'agent_name': 'agent',
                                                               'git_branch': 'add-caching',
                                                               'git_hash': '631bc68b65d55a4f25835e42ffc62cca9a858475',
                                                               'unique_id': '8d094b03-8542-4e01-bba0-0dc9f8cd805e'},
                                                  'prompt': [{'content': 'Tell me a joke about dogs.',
                                                              'role': 'template'}],
                                                  'request_id': 'ff153a57-db54-46d2-9d64-0ab2727bbe06',
                                                  'request_params': {'best_of': 1,
                                                                     'frequency_penalty': 0,
                                                                     'max_tokens': 1200,
                                                                     'model': 'text-davinci-003',
                                                                     'presence_penalty': 0,
                                                                     'stop': ['#', '---'],
                                                                     'temperature': 0,
                                                                     'top_p': 1},
                                                  'request_values': {'topic': 'dogs'}},
                                      'response': {'api_log_id': 'cmpl-7hf2k7hCx4fQmC15tN5IpVAjIrWET',
                                                   'latency': 2.42621111869812,
                                                   'model': 'text-davinci-003',
                                                   'stop': 'stop',
                                                   'stop_reason': 'stop',
                                                   'token_usage': {'prompt': 8,
                                                                   'response': 26,
                                                                   'total': 34}}}}
    test_data_2: dict = {'data': '\n\nQ: What do cats like to eat for breakfast? \nA: Mice Krispies!',
                         'metadata': {'custom': {},
                                      'pdx': {'version': '0.5.1'},
                                      'request': {'agent_id': {'agent_name': 'agent',
                                                               'git_branch': 'add-caching',
                                                               'git_hash': '631bc68b65d55a4f25835e42ffc62cca9a858475',
                                                               'unique_id': '8d094b03-8542-4e01-bba0-0dc9f8cd805e'},
                                                  'prompt': [{'content': 'Tell me a joke about cats.',
                                                              'role': 'template'}],
                                                  'request_id': 'a873a5a1-541f-4354-8bfc-7a88f1dd6451',
                                                  'request_params': {'best_of': 1,
                                                                     'frequency_penalty': 0,
                                                                     'max_tokens': 1200,
                                                                     'model': 'text-davinci-003',
                                                                     'presence_penalty': 0,
                                                                     'stop': ['#', '---'],
                                                                     'temperature': 0,
                                                                     'top_p': 1},
                                                  'request_values': {'topic': 'cats'}},
                                      'response': {'api_log_id': 'cmpl-7hf2l4AWOnjfTLk50WyFYQj8t7DhH',
                                                   'latency': 1.1315219402313232,
                                                   'model': 'text-davinci-003',
                                                   'stop': 'stop',
                                                   'stop_reason': 'stop',
                                                   'token_usage': {'prompt': 8,
                                                                   'response': 23,
                                                                   'total': 31}}}}
    request_values: dict = {'topic': 'dogs'}


@pytest.fixture
def config():
    return TestConfig()


@pytest.fixture
def cache(config: TestConfig):
    _in_memory_cache = InMemoryCache()

    agent_response_1 = AgentResponse(**config.test_data_1)
    agent_response_2 = AgentResponse(**config.test_data_2)

    _in_memory_cache.update(
        agent_id=agent_response_1.metadata.request.agent_id,
        agent_request=agent_response_1.metadata.request.request_values,
        agent_response=agent_response_1
    )

    _in_memory_cache.update(
        agent_id=agent_response_2.metadata.request.agent_id,
        agent_request=agent_response_2.metadata.request.request_values,
        agent_response=agent_response_2
    )
    return _in_memory_cache


def test_cache_initialization(request, config):

    cache = InMemoryCache()

    assert isinstance(cache, InMemoryCache)
    assert isinstance(cache._cache, dict)
    assert cache._cache == {}


def test_cache_update(request, config: TestConfig, cache: InMemoryCache):
    assert cache._cache != {}
    assert len(cache._cache) == 2


def test_cache_lookup(request, config: TestConfig, cache: InMemoryCache):
    agent_response_1 = AgentResponse(**config.test_data_1)
    _request_1_values = agent_response_1.metadata.request.request_values
    _request_1_agent_id = agent_response_1.metadata.request.agent_id
    _agent_response_1_values = agent_response_1.model_dump(mode='json')

    agent_response_2 = AgentResponse(**config.test_data_2)
    _request_2_values = agent_response_2.metadata.request.request_values
    _request_2_agent_id = agent_response_2.metadata.request.agent_id
    _agent_response_2_values = agent_response_2.model_dump(mode='json')

    _request_1_loop_up = cache.lookup(
        agent_id=_request_1_agent_id,
        agent_request=_request_1_values)

    _request_2_loop_up = cache.lookup(
        agent_id=_request_2_agent_id,
        agent_request=_request_2_values)

    assert cache._cache != {}
    assert len(cache._cache) == 2

    assert _request_1_loop_up == agent_response_1
    assert _request_1_loop_up.model_dump(
        mode='json') == _agent_response_1_values

    assert _request_2_loop_up == agent_response_2
    assert _request_2_loop_up.model_dump(
        mode='json') == _agent_response_2_values
