import os
import json
from jinja2 import Environment, FileSystemLoader, Template, meta
from pdx.utils.rw import read_yaml


class PromptTemplate:
    def __init__(self, template_path: str = None, template_string: str = None, name: str = None):
        if template_string != None:
            self._template_type = 'string'
            self._template_string = template_string
            self._template_name = name
            self._template_id = name
            self._environment = None
            self._template = self.load_native_template()
            self._fields = {}
            self._field_values = {}
        elif template_path != None:
            self._template_type = 'file'
            self._templates_path = os.path.dirname(template_path)            
            self._template_name = os.path.basename(template_path)
            self._template_id = name.split('.')[0]

            self._environment = None
            self._template = self.load_template()
            self._fields = self.parse_fields()
            self._field_values = {}

            _defaults_path = os.path.join(
                self._templates_path, f"{self._template_id}.defaults.yaml")
            if os.path.exists(_defaults_path):
                self.set_field_values(read_yaml(_defaults_path))

    def load_template(self):
        self._environment = Environment(
            loader=FileSystemLoader(self._templates_path))
        template: Template = self._environment.get_template(
            self._template_name)

        return template

    def load_native_template(self):
        self._environment = Environment()
        template: Template = self._environment.from_string(
            self._template_string)

        return template

    def parse_fields(self):
        template_source = self._environment.loader.get_source(
            self._environment, self._template_name)
        parsed_content = self._environment.parse(template_source)
        return meta.find_undeclared_variables(parsed_content)

    def set_field_values(self, field_values: dict):
        for key, value in field_values.items():
            if isinstance(value, dict):
                self._field_values[key] = json.dumps(value)
            else:
                self._field_values[key] = str(value)

    def execute(self, field_values: dict = {}):
        if field_values is None:
            field_values = {}
        _current_field_values = self._field_values
        for key, value in field_values.items():
            if isinstance(value, dict):
                _current_field_values[key] = json.dumps(value)
            else:
                _current_field_values[key] = str(value)

        return self._template.render(_current_field_values)
