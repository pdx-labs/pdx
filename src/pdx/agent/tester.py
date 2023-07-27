import os
import asyncio
from pdx.agent import Agent
from pdx.utils.rw import read_yaml
from pdx.logger import logger
import click
from pdx.settings import process


def prompt_echo_console(prompt_chain: list):
    for _p in prompt_chain:
        _role: str = _p['role']
        if _role != None:
            click.echo(
                f'{click.style(f"{_role.upper()} PROMPT", fg="yellow")}')
        click.echo(f"{_p['content']}\n")


class AgentTestBuilder:
    def __init__(self, folder_path: str, agent: Agent):
        self._folder_path = folder_path
        self._agent = agent
        self._test_cases = self.build_tests()

    def build_tests(self):
        test_folder_files = os.listdir(
            os.path.join(self._folder_path, "tests"))
        test_files = []
        for _file in test_folder_files:
            if _file.endswith(".yaml") and _file.startswith("test"):
                test_files.append(_file)

        test_cases = {}
        for _file in test_files:
            _test_name = _file.split(".")[0]
            _test_input = read_yaml(os.path.join(
                self._folder_path, "tests", _file))
            test_cases[_test_name] = _test_input

        return test_cases

    async def run_test(self, _test_name, _test_input):
        logger.echo(f"Running: {_test_name}", event="test")
        _r = await self._agent.aexecute(_test_input)
        logger.verbose(f"Test {_test_name}: prompt\n")
        if process.verbose:
            prompt_echo_console(_r.metadata.request.prompt)
        logger.verbose(f"Test {_test_name}: completion\n{_r.data}")

    async def run_tests(self):
        _test_run_list = []
        for _test_name, _test_input in self._test_cases.items():
            _test_run_list.append(self.run_test(_test_name, _test_input))
        _run_output_list = await asyncio.gather(*_test_run_list)
        return _run_output_list

    def execute(self):
        asyncio.run(self.run_tests())
