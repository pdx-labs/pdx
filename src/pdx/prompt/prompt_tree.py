import os
from collections import OrderedDict
from pdx.prompt import Prompt
from pdx.prompt.config import PromptConfig
from pdx.prompt.prompt_session import PromptSession


class WhenOperationConfig:
    def __init__(self, config: dict, operation: str):
        self.operation = operation
        self.pointer = config.get('pointer', config[operation])
        self.prompt_config = config['prompt']
        self.prompt_tree: PromptTree = None

    def execute(self, values: dict, prompt_session: PromptSession = None):
        if values != {}:
            self.prompt_tree.execute(values, prompt_session)


class LoopOperationConfig:
    def __init__(self, config: dict, operation: str):
        self.operation = operation
        self.pointer = config.get('pointer', config[operation])
        self.prompt_config = config['prompt']
        self.prompt_tree: PromptTree = None

    def execute(self, values: dict, prompt_session: PromptSession = None):
        for field in values:
            self.prompt_tree.execute(field, prompt_session)


class SwitchOperationConfig:
    def __init__(self, config: dict, operation: str):
        self.operation = operation
        self.pointer = config.get('pointer', config[operation])
        self.cases_config = config['prompt']
        self.prompt_tree: PromptTree = None

    def execute(self, values: dict, prompt_session: PromptSession = None):
        for case, field in values.items():
            if case in self.prompt_tree:
                self.prompt_tree[case].execute(field, prompt_session)
            elif 'default' in self.prompt_tree:
                self.prompt_tree['default'].execute(
                    field, prompt_session)


class PromptTree:
    def __init__(self, prompt_config: PromptConfig, strict=False):
        self._templates_path = prompt_config.templates_path
        self.prompt_config = prompt_config.config
        # `strict`: If pointers are not present, do not execute them in the tree.
        self._strict = strict
        self.tree = self._build_tree()

    def _build_prompt(self, _p: dict, role: str):
        _prompt_role = role
        _template_name: str = _p[_prompt_role]
        _template_path: str = os.path.join(
            self._templates_path, _template_name)
        _prompt_pointer = _p.get(
            'pointer', _template_name.split('.')[0])
        _prompt = Prompt(
            template_path=_template_path,
            pointer=_prompt_pointer,
            role=_prompt_role
        )

        return _prompt

    def _build_tree(self):
        _tree = OrderedDict()
        for _p in self.prompt_config:
            if 'template' in _p:
                _prompt = self._build_prompt(_p, 'template')
                _tree[_prompt.pointer] = _prompt
            elif 'system' in _p:
                _prompt = self._build_prompt(_p, 'system')
                _tree[_prompt.pointer] = _prompt
            elif 'user' in _p:
                _prompt = self._build_prompt(_p, 'user')
                _tree[_prompt.pointer] = _prompt
            elif 'assistant' in _p:
                _prompt = self._build_prompt(_p, 'assistant')
                _tree[_prompt.pointer] = _prompt
            elif 'when' in _p:
                _config = WhenOperationConfig(_p, operation='when')
                _prompt_config = PromptConfig(
                    _config.prompt_config, self._templates_path)
                _config.prompt_tree = PromptTree(
                    _prompt_config, self._strict)
                _tree[_config.pointer] = _config
            elif 'loop' in _p:
                _config = LoopOperationConfig(_p, operation='loop')
                _prompt_config = PromptConfig(
                    _config.prompt_config, self._templates_path)
                _config.prompt_tree = PromptTree(
                    _prompt_config, self._strict)
                _tree[_config.pointer] = _config
            elif 'switch' in _p:
                _config = SwitchOperationConfig(_p, operation='switch')
                _cases_tree = OrderedDict()
                for case in _config.cases_config:
                    _prompt_config = PromptConfig(
                        _config.cases_config[case], self._templates_path)
                    _cases_tree[case] = PromptTree(
                        _prompt_config, self._strict)
                _config.prompt_tree = _cases_tree
                _tree[_config.pointer] = _config

        return _tree

    def execute(self, request: dict, prompt_session: PromptSession = None):
        _output = False

        if prompt_session is None:
            prompt_session = PromptSession()
            _output = True

        for key, tree_object in self.tree.items():
            if self._strict:
                if key in request:
                    field_values = request.get(key, {})
                    tree_object.execute(values=field_values,
                                        prompt_session=prompt_session)
            else:
                field_values = request.get(key, {})
                tree_object.execute(values=field_values,
                                    prompt_session=prompt_session)

        if _output:
            return prompt_session
