import os
from collections import OrderedDict
from pdx.prompt.config import PromptConfig
from pdx.agent.templater import TemplateAgent
from pdx.prompt.prompt_chain import PromptChain


class TemplateConfig:
    def __init__(self, config: dict, tempaltes_path: str, role: str = None):
        self.role = role
        if role is None:
            self.name: str = config['template']
        else:
            self.name: str = config[role]
        self.pointer = config.get('pointer', self.name.split('.')[0])
        self.template_path = os.path.join(tempaltes_path, self.name)
        self.id = self.name.split('.')[0]

        self._template_agent = TemplateAgent(self.template_path, self.name)
        self.template_fields = self._template_agent._fields

    def execute(self, fields: dict, prompt_chain: PromptChain = None):
        if fields is None:
            fields = {}
        prompt = self._template_agent.execute(fields)
        prompt_chain.add(prompt, self.role)


class WhenOperationConfig:
    def __init__(self, config: dict, operation: str):
        self.operation = operation
        self.pointer = config.get('pointer', config[operation])
        self.prompt_config = config['prompt']
        self.prompt_tree = None

    def execute(self, fields: dict, prompt_chain: PromptChain = None):
        if fields != {}:
            self.prompt_tree.execute(fields, prompt_chain)


class LoopOperationConfig:
    def __init__(self, config: dict, operation: str):
        self.operation = operation
        self.pointer = config.get('pointer', config[operation])
        self.prompt_config = config['prompt']
        self.prompt_tree = None

    def execute(self, fields: dict, prompt_chain: PromptChain = None):
        for field in fields:
            self.prompt_tree.execute(field, prompt_chain)


class SwitchOperationConfig:
    def __init__(self, config: dict, operation: str):
        self.operation = operation
        self.pointer = config.get('pointer', config[operation])
        self.cases_config = config['prompt']
        self.prompt_tree = None

    def execute(self, fields: dict, prompt_chain: PromptChain = None):
        for case, field in fields.items():
            if case in self.prompt_tree:
                self.prompt_tree[case].execute(field, prompt_chain)
            elif 'default' in self.prompt_tree:
                self.prompt_tree['default'].execute(
                    field, prompt_chain)


class PromptTree:
    def __init__(self, prompt_config: PromptConfig, strict=False):
        self._templates_path = prompt_config.templates_path
        self.prompt_config = prompt_config.config
        self._strict = strict
        # If pointers are not present, do not execute them in the tree.
        self.tree = self._build_tree()

    def _build_tree(self):
        _tree = OrderedDict()
        for _p in self.prompt_config:
            if 'template' in _p:
                _config = TemplateConfig(_p, self._templates_path)
                _tree[_config.pointer] = _config
            elif 'system' in _p:
                _config = TemplateConfig(
                    _p, self._templates_path, role='system')
                _tree[_config.pointer] = _config
            elif 'user' in _p:
                _config = TemplateConfig(_p, self._templates_path, role='user')
                _tree[_config.pointer] = _config
            elif 'assistant' in _p:
                _config = TemplateConfig(
                    _p, self._templates_path, role='assistant')
                _tree[_config.pointer] = _config
            elif 'when' in _p:
                _config = WhenOperationConfig(_p, operation='when')
                _config.prompt_tree = PromptTree(
                    _p['prompt'], self._templates_path, self._strict)
                _tree[_config.pointer] = _config
            elif 'loop' in _p:
                _config = LoopOperationConfig(_p, operation='loop')
                _config.prompt_tree = PromptTree(
                    _p['prompt'], self._templates_path, self._strict)
                _tree[_config.pointer] = _config
            elif 'switch' in _p:
                _config = SwitchOperationConfig(_p, operation='switch')
                _cases_tree = OrderedDict()
                for case in _config.cases_config:
                    _cases_tree[case] = PromptTree(
                        _config.cases_config[case], self._templates_path, self._strict)
                _config.prompt_tree = _cases_tree
                _tree[_config.pointer] = _config

        return _tree

    def execute(self, request, prompt_chain: PromptChain):
        for key, value in self.tree.items():
            if self._strict:
                if key in request:
                    field_values = request.get(key, {})
                    value.execute(field_values, prompt_chain)
            else:
                field_values = request.get(key, {})
                value.execute(field_values, prompt_chain)
